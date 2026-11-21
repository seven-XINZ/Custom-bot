"""通用反向 WebSocket 适配器。

给自定义客户端 / 中转程序用，不绑定任何平台协议。消息格式：

    客户端 → 服务端
    {"type": "message", "user_id": "u1", "user_name": "阿星", "group_id": "g1",
     "content": "你好", "msg_id": "m1", "metadata": {"k": "v"}}

    服务端 → 客户端
    {"type": "reply", "content": "你好呀", "reply_to": "m1", "internal_id": "…"}

也接受不带 JSON 包装的纯文本，按当前连接的单聊处理。
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from typing import Any, Dict, List, Optional

try:  # websockets >= 13
    from websockets.asyncio.server import ServerConnection, serve
except ImportError:  # pragma: no cover
    from websockets.server import WebSocketServerProtocol as ServerConnection  # type: ignore
    from websockets.server import serve  # type: ignore

from websockets.exceptions import ConnectionClosed

from core.adapters import BaseAdapter
from core.message import Attachment, InternalMessage

logger = logging.getLogger("适配器.ReverseWS")


class ReverseWebSocketAdapter(BaseAdapter):
    """通用反向 WS：外部程序连进来，双向收发 JSON。"""

    kind = "reverse_ws"

    def __init__(self, kernel, adapter_id: str, config: Dict[str, Any]):
        super().__init__(kernel, adapter_id, config)
        self.host: str = str(config.get("host", "0.0.0.0"))
        self.port: int = int(config.get("port", 8766))
        self.path: str = str(config.get("path", "/ws"))
        self.access_token: str = str(config.get("access_token", "") or "")
        self._server: Any = None
        self._clients: Dict[str, ServerConnection] = {}

    # ------------------------------------------------------------------ 生命周期
    async def setup(self) -> None:
        await super().setup()
        self.logger.debug("通用反向 WS 将监听 ws://%s:%s%s", self.host, self.port, self.path)

    async def start(self) -> None:
        await super().start()
        if self._server is not None:
            return
        try:
            self._server = await serve(
                self._connection_handler, self.host, self.port,
                ping_interval=30, ping_timeout=20,
            )
            self.is_running = True
            self.status_extra(listen=f"ws://{self.host}:{self.port}{self.path}")
            self.logger.info("通用反向 WS 已启动: ws://%s:%s%s", self.host, self.port, self.path)
        except OSError as exc:
            self.is_running = False
            self._count_error(exc)
            self.logger.error("通用反向 WS 启动失败: %s", exc)
        except Exception as exc:  # noqa: BLE001
            self.is_running = False
            self._count_error(exc)
            self.logger.exception("通用反向 WS 启动异常: %s", exc)

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            try:
                await asyncio.wait_for(self._server.wait_closed(), timeout=5)
            except asyncio.TimeoutError:
                pass
            self._server = None
        for connection_id, ws in list(self._clients.items()):
            try:
                await ws.close(code=1001, reason="server shutdown")
            except Exception:  # noqa: BLE001
                pass
        self._clients.clear()
        await super().stop()

    # ------------------------------------------------------------------ 连接
    async def _connection_handler(self, websocket: ServerConnection, path: Optional[str] = None):
        request = getattr(websocket, "request", None)
        if path is None:
            path = getattr(request, "path", self.path) if request else self.path
        if self.path and path != self.path:
            await websocket.close(code=1008, reason="invalid path")
            return
        if self.access_token:
            headers = getattr(request, "headers", {}) if request else {}
            auth = headers.get("Authorization", "") if hasattr(headers, "get") else ""
            if auth != f"Bearer {self.access_token}":
                await websocket.close(code=1008, reason="auth failed")
                return

        connection_id = uuid.uuid4().hex[:10]
        self._clients[connection_id] = websocket
        self.status_extra(clients=len(self._clients))
        self.logger.info("通用 WS 客户端接入: %s（当前 %d 个）", connection_id, len(self._clients))

        try:
            async for raw in websocket:
                await self._handle_raw(connection_id, raw)
        except ConnectionClosed:
            self.logger.info("通用 WS 客户端断开: %s", connection_id)
        except Exception as exc:  # noqa: BLE001
            self._count_error(exc)
            self.logger.exception("通用 WS 连接 %s 出错: %s", connection_id, exc)
        finally:
            self._clients.pop(connection_id, None)
            self.status_extra(clients=len(self._clients))

    async def _handle_raw(self, connection_id: str, raw: Any) -> None:
        text = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        payload: Any
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {"type": "message", "content": text}

        if not isinstance(payload, dict):
            return
        kind = str(payload.get("type", "message"))

        if kind == "ping":
            await self._send_json(connection_id, {"type": "pong", "ts": time.time()})
            return
        if kind == "ack":
            return
        if kind != "message":
            return

        attachments: List[Attachment] = []
        for item in payload.get("attachments", []) or []:
            if isinstance(item, dict):
                fields = {k: v for k, v in item.items() if k in Attachment.__dataclass_fields__}
                attachments.append(Attachment(**fields))

        message = InternalMessage(
            adapter_id=self.adapter_id,
            protocol=self.protocol_name,
            connection_id=connection_id,
            session_id=str(payload.get("session_id") or "") or None,
            user_id=str(payload.get("user_id") or "anonymous"),
            user_name=str(payload.get("user_name") or ""),
            group_id=str(payload.get("group_id")) if payload.get("group_id") else None,
            group_name=str(payload.get("group_name") or "") or None,
            msg_id=str(payload.get("msg_id") or uuid.uuid4().hex[:8]),
            msg_type=str(payload.get("msg_type") or "text"),
            text_content=str(payload.get("content") or ""),
            attachments=attachments,
            parsed_data=payload,
            raw_data=text,
            metadata=dict(payload.get("metadata") or {}),
            timestamp=float(payload.get("timestamp") or time.time()),
        )
        await self._push_to_kernel(message)

    # ------------------------------------------------------------------ 发送
    async def send(self, message: InternalMessage) -> bool:
        target = message.connection_id if message.connection_id in self._clients else None
        if not target and len(self._clients) == 1:
            target = next(iter(self._clients))
        if not target:
            self.logger.warning("通用 WS 发送失败：找不到目标连接")
            return False

        payload = {
            "type": "reply",
            "content": message.text_content,
            "reply_to": message.metadata.get("reply_to_msg_id") or message.msg_id,
            "internal_id": message.internal_id,
            "user_id": message.user_id,
            "group_id": message.group_id,
            "attachments": [a.to_dict() for a in message.attachments],
            "metadata": message.metadata,
            "ts": time.time(),
        }
        return await self._send_json(target, payload)

    async def _send_json(self, connection_id: str, payload: Dict[str, Any]) -> bool:
        ws = self._clients.get(connection_id)
        if not ws:
            return False
        try:
            await ws.send(json.dumps(payload, ensure_ascii=False))
            return True
        except ConnectionClosed:
            self._clients.pop(connection_id, None)
            return False
        except Exception as exc:  # noqa: BLE001
            self._count_error(exc)
            self.logger.exception("通用 WS 发送失败: %s", exc)
            return False

    def get_status(self) -> Dict[str, Any]:
        status = super().get_status()
        status.update({
            "listen": f"ws://{self.host}:{self.port}{self.path}",
            "clients": len(self._clients),
            "token": bool(self.access_token),
        })
        return status
