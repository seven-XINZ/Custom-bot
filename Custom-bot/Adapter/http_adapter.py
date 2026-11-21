"""HTTP Webhook 适配器。

两个方向：

- 入站：外部系统 POST 到 `http://host:port<path>`，body 为 JSON 或纯文本，
  适配器转成 `InternalMessage` 交给内核。
- 出站：内核回复时 POST 到 `message.metadata["target_url"]`；没指定就用配置里的
  `callback_url`。适合 CI 通知、监控告警、IFTTT 这类一次性事件源。

可选 `access_token`：入站请求需带 `X-Token: <token>` 或 `Authorization: Bearer <token>`。
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from typing import Any, Dict, Optional

import aiohttp
from aiohttp import web

from core.adapters import BaseAdapter
from core.message import Attachment, InternalMessage

logger = logging.getLogger("适配器.HttpAdapter")


class HttpAdapter(BaseAdapter):
    kind = "http"

    def __init__(self, kernel, adapter_id: str, config: Dict[str, Any]):
        super().__init__(kernel, adapter_id, config)
        self.host: str = str(config.get("host", "0.0.0.0"))
        self.port: int = int(config.get("port", 8088))
        self.webhook_path: str = str(config.get("path", "/webhook"))
        self.health_path: str = str(config.get("health_path", "/health"))
        self.access_token: str = str(config.get("access_token", "") or "")
        self.callback_url: str = str(config.get("callback_url", "") or "")
        self._app: Optional[web.Application] = None
        self._runner: Optional[web.AppRunner] = None
        self._site: Optional[web.TCPSite] = None
        self._session: Optional[aiohttp.ClientSession] = None

    # ------------------------------------------------------------------ 生命周期
    async def setup(self) -> None:
        await super().setup()
        self._app = web.Application(logger=logger)
        self._app.router.add_post(self.webhook_path, self._handle_webhook)
        self._app.router.add_get(self.health_path, self._handle_health)
        self._app.router.add_get(self.webhook_path, self._handle_health)
        self.logger.debug("HTTP 路由已就绪: POST %s", self.webhook_path)

    async def start(self) -> None:
        await super().start()
        if not self._app:
            await self.setup()
        if self._site and self._site.is_serving():
            return
        try:
            self._runner = web.AppRunner(self._app, access_log=None)
            await self._runner.setup()
            self._site = web.TCPSite(self._runner, self.host, self.port)
            await self._site.start()
            self.is_running = True
            self.status_extra(listen=f"http://{self.host}:{self.port}{self.webhook_path}")
            self.logger.info("HTTP 适配器已启动: http://%s:%s%s", self.host, self.port, self.webhook_path)
        except OSError as exc:
            self.is_running = False
            self._count_error(exc)
            self.logger.error("HTTP 适配器启动失败（%s:%s）: %s", self.host, self.port, exc)

    async def stop(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None
        if self._site:
            await self._site.stop()
            self._site = None
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
        self._app = None
        await super().stop()

    # ------------------------------------------------------------------ 入站
    def _authorized(self, request: web.Request) -> bool:
        if not self.access_token:
            return True
        token = request.headers.get("X-Token", "")
        auth = request.headers.get("Authorization", "")
        return token == self.access_token or auth == f"Bearer {self.access_token}"

    async def _handle_health(self, request: web.Request) -> web.Response:
        return web.json_response({"ok": True, "adapter": self.adapter_id,
                                  "running": self.is_running, "ts": time.time()})

    async def _handle_webhook(self, request: web.Request) -> web.Response:
        if not self._authorized(request):
            return web.json_response({"ok": False, "error": "unauthorized"}, status=401)

        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:10]
        body_bytes = await request.read()
        content_type = (request.content_type or "").lower()
        payload: Any = None
        text = ""
        attachments: list[Attachment] = []

        if body_bytes:
            if content_type == "application/json" or body_bytes[:1] in (b"{", b"["):
                try:
                    payload = json.loads(body_bytes.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    text = body_bytes.decode("utf-8", "replace")
            elif content_type.startswith("text/") or not content_type:
                text = body_bytes.decode("utf-8", "replace")
            else:
                self.logger.warning("收到二进制 webhook（%s，%d 字节），只记录元数据",
                                    content_type, len(body_bytes))

        if isinstance(payload, dict):
            text = str(payload.get("message") or payload.get("content") or payload.get("text") or text)
            for item in payload.get("attachments", []) or []:
                if isinstance(item, dict):
                    fields = {k: v for k, v in item.items() if k in Attachment.__dataclass_fields__}
                    attachments.append(Attachment(**fields))

        message = InternalMessage(
            adapter_id=self.adapter_id,
            protocol=self.protocol_name,
            connection_id=request.remote or "http",
            session_id=request_id,
            user_id=str((payload or {}).get("user_id") or request.remote or "http") if isinstance(payload, dict) else (request.remote or "http"),
            user_name=str((payload or {}).get("user_name") or "") if isinstance(payload, dict) else "",
            group_id=str((payload or {}).get("group_id")) if isinstance(payload, dict) and (payload or {}).get("group_id") else None,
            msg_id=str((payload or {}).get("msg_id") or request_id),
            msg_type="text",
            text_content=text.strip(),
            attachments=attachments,
            parsed_data=payload,
            raw_data=body_bytes,
            metadata={
                "remote_ip": request.remote,
                "http_path": request.path,
                "headers": dict(request.headers),
                "query": dict(request.query),
                "target_url": request.headers.get("X-Callback-URL") or self.callback_url,
                "request_id": request_id,
            },
            timestamp=time.time(),
        )
        # Webhook 语义上是「投递即返回」：收到就回 202，处理与出站回调放后台，
        # 免得调用方等命令执行 + 回调超时而误判失败。
        asyncio.create_task(self._background_push(message), name=f"http_push_{request_id}")
        return web.json_response({"ok": True, "request_id": request_id}, status=202)

    async def _background_push(self, message: InternalMessage) -> None:
        try:
            await self._push_to_kernel(message)
        except Exception as exc:  # noqa: BLE001
            self._count_error(exc)
            self.logger.exception("HTTP webhook 后台处理失败: %s", exc)

    # ------------------------------------------------------------------ 出站
    async def send(self, message: InternalMessage) -> bool:
        target_url = str(message.metadata.get("target_url") or self.callback_url)
        if not target_url:
            self.logger.warning("HTTP 发送失败：没有 target_url / callback_url")
            return False

        body = {
            "reply_to": message.metadata.get("reply_to_msg_id") or message.reply_to,
            "internal_id": message.internal_id,
            "user_id": message.user_id,
            "group_id": message.group_id,
            "content": message.text_content,
            "attachments": [a.to_dict() for a in message.attachments],
            "ts": time.time(),
        }
        headers = {"Content-Type": "application/json; charset=utf-8"}
        token = str(message.metadata.get("callback_token") or "")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            if self._session is None or self._session.closed:
                self._session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))
            async with self._session.post(target_url, json=body, headers=headers) as response:
                if 200 <= response.status < 300:
                    return True
                text = await response.text(errors="replace")
                self._count_error(f"HTTP {response.status}")
                self.logger.error("HTTP 出站失败（%s）: %s", response.status, text[:200])
                return False
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            self._count_error(exc)
            self.logger.error("HTTP 出站异常: %s", exc)
            return False

    def get_status(self) -> Dict[str, Any]:
        status = super().get_status()
        status.update({
            "listen": f"http://{self.host}:{self.port}{self.webhook_path}",
            "callback": bool(self.callback_url),
            "token": bool(self.access_token),
        })
        return status
