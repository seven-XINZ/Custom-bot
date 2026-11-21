"""QQ 适配器（OneBot v11 反向 WebSocket）。

机器人框架作为 WS 服务端，QQ 客户端（NapCat / LLOneBot / Lagrange 等）连上来，
按 OneBot v11 上报事件、接受 `send_msg` / `delete_msg` 等 API 调用。

兼容 websockets 13+（新 asyncio 实现）与 10~12（handler 带 path 参数）。
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
except ImportError:  # pragma: no cover - 兼容旧版
    from websockets.server import WebSocketServerProtocol as ServerConnection  # type: ignore
    from websockets.server import serve  # type: ignore

from websockets.exceptions import ConnectionClosed

from core.adapters import BaseAdapter
from core.message import Attachment, InternalMessage

logger = logging.getLogger("适配器.QQAdapter")

# OneBot 消息段 → 内部附件类型
_SEGMENT_TYPES = {
    "image": "image",
    "record": "audio",
    "voice": "audio",
    "video": "video",
    "file": "file",
}


class QQAdapter(BaseAdapter):
    """OneBot v11 反向 WebSocket 适配器。"""

    kind = "qq"

    def __init__(self, kernel, adapter_id: str, config: Dict[str, Any]):
        super().__init__(kernel, adapter_id, config)
        self.host: str = str(config.get("host", "0.0.0.0"))
        self.port: int = int(config.get("port", 8765))
        self.event_path: str = str(config.get("path", "/onebot/v11/event"))
        self.access_token: str = str(config.get("access_token", "") or "")
        self.api_timeout: float = float(config.get("api_timeout", 30))
        self._server: Any = None
        self._server_task: Optional[asyncio.Task] = None
        self._clients: Dict[str, ServerConnection] = {}
        self._echo_futures: Dict[str, asyncio.Future] = {}
        self._queues: Dict[str, asyncio.Queue] = {}
        self._workers: Dict[str, asyncio.Task] = {}
        self._self_id: Optional[str] = None

    # ------------------------------------------------------------------ 生命周期
    async def setup(self) -> None:
        await super().setup()
        self.logger.debug("QQ 反向 WS 将监听 ws://%s:%s%s", self.host, self.port, self.event_path)

    async def start(self) -> None:
        await super().start()
        if self._server is not None:
            self.logger.warning("QQ 反向 WS 服务已在运行")
            return
        try:
            self._server = await serve(
                self._connection_handler,
                self.host,
                self.port,
                ping_interval=30,
                ping_timeout=20,
                max_size=8 * 1024 * 1024,
            )
            self.is_running = True
            self.status_extra(listen=f"ws://{self.host}:{self.port}{self.event_path}")
            self.logger.info("QQ 反向 WS 已启动: ws://%s:%s%s", self.host, self.port, self.event_path)
            self._server_task = asyncio.create_task(self._server.wait_closed(),
                                                   name=f"QQ_RWS_{self.adapter_id}")
        except OSError as exc:
            self.is_running = False
            self._count_error(exc)
            self.logger.error("QQ 反向 WS 启动失败（%s:%s）: %s", self.host, self.port, exc)
        except Exception as exc:  # noqa: BLE001
            self.is_running = False
            self._count_error(exc)
            self.logger.exception("QQ 反向 WS 启动异常: %s", exc)

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            try:
                await asyncio.wait_for(self._server.wait_closed(), timeout=5)
            except asyncio.TimeoutError:
                self.logger.warning("等待 QQ WS 关闭超时")
        self._server = None
        if self._server_task:
            self._server_task.cancel()
            self._server_task = None
        for connection_id, ws in list(self._clients.items()):
            try:
                await ws.close(code=1001, reason="server shutdown")
            except Exception:  # noqa: BLE001
                pass
            self._clients.pop(connection_id, None)
        for future in list(self._echo_futures.values()):
            if not future.done():
                future.cancel()
        self._echo_futures.clear()
        for worker in list(self._workers.values()):
            worker.cancel()
        self._workers.clear()
        self._queues.clear()
        await super().stop()

    # ------------------------------------------------------------------ 连接
    async def _connection_handler(self, websocket: ServerConnection, path: Optional[str] = None):
        # 新版 websockets 不传 path，需要从握手请求里取
        request = getattr(websocket, "request", None)
        if path is None:
            path = getattr(request, "path", "/") if request else "/"
        remote = getattr(websocket, "remote_address", None) or ("?", 0)
        connection_id = f"{remote[0]}:{remote[1]}"

        if path != self.event_path:
            self.logger.warning("拒绝连接：路径 %r 与期望 %r 不符", path, self.event_path)
            await websocket.close(code=1008, reason="invalid path")
            return

        if self.access_token:
            headers = getattr(request, "headers", {}) if request else {}
            auth = headers.get("Authorization", "") if hasattr(headers, "get") else ""
            if auth != f"Bearer {self.access_token}":
                self.logger.warning("拒绝连接：Access Token 不匹配（收到 %r）", auth)
                await websocket.close(code=1008, reason="auth failed")
                return

        self._clients[connection_id] = websocket
        self.status_extra(clients=len(self._clients))
        self.logger.info("QQ 客户端已连接: %s（当前 %d 个）", connection_id, len(self._clients))

        # 收包协程只负责读：回执立即唤醒 future，业务事件丢进队列由独立 worker 处理，
        # 否则「处理消息 → 回复 → 等待回执」会卡住同一个接收循环，造成自锁。
        queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
        self._queues[connection_id] = queue
        worker = asyncio.create_task(self._event_worker(connection_id, queue),
                                     name=f"QQ_events_{connection_id}")
        self._workers[connection_id] = worker

        try:
            async for raw in websocket:
                self._handle_raw(connection_id, raw)
        except ConnectionClosed:
            self.logger.info("QQ 客户端断开: %s", connection_id)
        except Exception as exc:  # noqa: BLE001
            self._count_error(exc)
            self.logger.exception("处理 QQ 连接 %s 出错: %s", connection_id, exc)
        finally:
            try:
                queue.put_nowait(None)
            except asyncio.QueueFull:
                worker.cancel()
            try:
                await asyncio.wait_for(worker, timeout=5)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                worker.cancel()
            except Exception:  # noqa: BLE001
                self.logger.exception("QQ 事件 worker 退出异常")
            self._queues.pop(connection_id, None)
            self._workers.pop(connection_id, None)
            self._clients.pop(connection_id, None)
            self.status_extra(clients=len(self._clients))
            self.logger.info("已移除 QQ 连接 %s（剩余 %d）", connection_id, len(self._clients))

    async def _event_worker(self, connection_id: str, queue: asyncio.Queue) -> None:
        """顺序消费本连接的业务事件，与收包解耦。"""
        while True:
            event = await queue.get()
            if event is None:
                return
            try:
                await self._process_event(connection_id, event)
            except Exception as exc:  # noqa: BLE001
                self._count_error(exc)
                self.logger.exception("处理 QQ 事件出错: %s", exc)

    def _handle_raw(self, connection_id: str, raw: Any) -> None:
        try:
            event = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            self.logger.warning("收到非 JSON 数据: %s", str(raw)[:120])
            return
        if not isinstance(event, dict):
            return

        # API 调用的回执必须在收包协程里立刻处理
        if "echo" in event:
            future = self._echo_futures.pop(str(event["echo"]), None)
            if future and not future.done():
                future.set_result(event)
            return

        queue = self._queues.get(connection_id)
        if queue is None:
            return
        try:
            queue.put_nowait(event)
        except asyncio.QueueFull:
            self.logger.warning("QQ 事件队列已满，丢弃 %s 事件", event.get("post_type"))

    async def _process_event(self, connection_id: str, event: Dict[str, Any]) -> None:
        post_type = event.get("post_type")
        if not post_type:
            return
        if post_type == "meta_event":
            if event.get("meta_event_type") == "lifecycle":
                self._self_id = str(event.get("self_id", ""))
                self.status_extra(self_id=self._self_id)
            return

        if post_type == "message":
            await self._push_to_kernel(self._parse_message(connection_id, event))
            return

        if post_type in {"notice", "request"}:
            await self._push_to_kernel(self._parse_event(connection_id, event))

    # ------------------------------------------------------------------ 解析
    def _parse_message(self, connection_id: str, event: Dict[str, Any]) -> InternalMessage:
        message_type = str(event.get("message_type", "private"))
        group_id = str(event.get("group_id", "")) if message_type == "group" else None
        user_id = str(event.get("sender", {}).get("user_id") or event.get("user_id") or "")
        user_name = str(event.get("sender", {}).get("card")
                        or event.get("sender", {}).get("nickname") or "")
        text, attachments = self._parse_segments(event.get("message"), event.get("raw_message", ""))
        self_id = str(event.get("self_id") or self._self_id or "")
        metadata: Dict[str, Any] = {
            "onebot_post_type": "message",
            "onebot_message_type": message_type,
            "onebot_sub_type": event.get("sub_type"),
            "self_id": self_id,
        }
        # 记录是否 @ 了机器人，供 AI 心智判断群聊要不要接话
        segments = event.get("message")
        if isinstance(segments, list):
            at_ids = [
                str(seg.get("data", {}).get("qq", ""))
                for seg in segments
                if isinstance(seg, dict) and seg.get("type") == "at"
            ]
            metadata["mentioned_bot"] = any(qq in {self_id, "all"} for qq in at_ids if qq)

        return InternalMessage(
            adapter_id=self.adapter_id,
            protocol=self.protocol_name,
            connection_id=connection_id,
            user_id=user_id or None,
            user_name=user_name,
            group_id=group_id,
            group_name=f"群{group_id}" if group_id else None,
            msg_id=str(event.get("message_id", "")) or None,
            msg_type="text",
            text_content=text,
            attachments=attachments,
            parsed_data=event,
            raw_data=event,
            metadata=metadata,
            timestamp=float(event.get("time") or time.time()),
        )

    def _parse_event(self, connection_id: str, event: Dict[str, Any]) -> InternalMessage:
        group_id = event.get("group_id")
        return InternalMessage(
            adapter_id=self.adapter_id,
            protocol=self.protocol_name,
            connection_id=connection_id,
            user_id=str(event.get("user_id")) if event.get("user_id") else None,
            group_id=str(group_id) if group_id else None,
            msg_id=str(event.get("message_id")) if event.get("message_id") else None,
            msg_type="event",
            text_content="",
            parsed_data=event,
            raw_data=event,
            metadata={
                "onebot_post_type": event.get("post_type"),
                "onebot_event": event.get("notice_type") or event.get("request_type"),
                "sub_type": event.get("sub_type"),
            },
            timestamp=float(event.get("time") or time.time()),
        )

    def _parse_segments(self, message: Any, raw_message: str) -> tuple[str, List[Attachment]]:
        """OneBot 数组格式与 CQ 码字符串都转成「纯文本 + 附件」。"""
        attachments: List[Attachment] = []
        if isinstance(message, list):
            parts: List[str] = []
            for segment in message:
                if not isinstance(segment, dict):
                    continue
                seg_type = str(segment.get("type", "text"))
                data = segment.get("data", {}) or {}
                if seg_type == "text":
                    parts.append(str(data.get("text", "")))
                elif seg_type in _SEGMENT_TYPES:
                    attachments.append(Attachment(
                        type=_SEGMENT_TYPES[seg_type],
                        file_id=str(data.get("file") or data.get("file_id") or "") or None,
                        url=str(data.get("url") or "") or None,
                        name=str(data.get("file") or "") or None,
                        extra={"onebot": data},
                    ))
            return "".join(parts).strip(), attachments

        text = str(message) if isinstance(message, str) else str(raw_message or "")
        # 简单剥离 CQ 码，图片等无法在本轮解析成真实地址
        if "CQ:" in text:
            stripped = []
            rest = text
            while "[" in rest and "CQ:" in rest:
                start = rest.find("[CQ:")
                end = rest.find("]", start)
                if end == -1:
                    break
                stripped.append(rest[:start])
                rest = rest[end + 1:]
            stripped.append(rest)
            text = "".join(stripped).strip()
        return text or str(raw_message or "").strip(), attachments

    # ------------------------------------------------------------------ 发送
    async def send(self, message: InternalMessage) -> bool:
        connection_id = self._pick_connection(message)
        if not connection_id:
            return False

        action, params = self._build_action(message)
        if not action:
            return False

        echo = uuid.uuid4().hex
        future: asyncio.Future = asyncio.get_running_loop().create_future()
        self._echo_futures[echo] = future
        payload = {"action": action, "params": params, "echo": echo}

        if not await self._send_raw(connection_id, payload):
            self._echo_futures.pop(echo, None)
            return False

        try:
            response = await asyncio.wait_for(future, timeout=self.api_timeout)
        except asyncio.TimeoutError:
            self._echo_futures.pop(echo, None)
            self._count_error("api timeout")
            self.logger.error("API %s 等待回执超时（echo=%s）", action, echo)
            return False
        finally:
            self._echo_futures.pop(echo, None)

        if isinstance(response, dict) and response.get("status") == "ok":
            return True
        error = (response or {}).get("msg") or (response or {}).get("wording") or "unknown"
        self._count_error(error)
        self.logger.error("API %s 失败: %s (retcode=%s)", action, error, (response or {}).get("retcode"))
        return False

    def _pick_connection(self, message: InternalMessage) -> Optional[str]:
        if message.connection_id and message.connection_id in self._clients:
            return message.connection_id
        if len(self._clients) == 1:
            return next(iter(self._clients))
        if not self._clients:
            self.logger.warning("没有 QQ 客户端连接，消息无法发送")
            return None
        self.logger.warning("有 %d 个 QQ 连接但未指定 connection_id", len(self._clients))
        return None

    def _build_action(self, message: InternalMessage) -> tuple[Optional[str], Dict[str, Any]]:
        meta = message.metadata or {}
        # 允许插件直接指定 OneBot action（撤回、禁言、戳一戳等）
        if meta.get("onebot_action"):
            return str(meta["onebot_action"]), dict(meta.get("onebot_params", {}))

        if message.msg_type == "action_delete":
            target = meta.get("target_msg_ids") or []
            if not target:
                self.logger.warning("撤回失败：缺少 target_msg_ids")
                return None, {}
            try:
                return "delete_msg", {"message_id": int(target[0])}
            except (TypeError, ValueError):
                return None, {}

        params: Dict[str, Any] = {}
        if message.is_group:
            params["message_type"] = "group"
            params["group_id"] = _as_int(message.group_id)
        elif message.user_id:
            params["message_type"] = "private"
            params["user_id"] = _as_int(message.user_id)
        else:
            self.logger.warning("发送失败：缺少 group_id / user_id")
            return None, {}

        segments: List[Dict[str, Any]] = []
        if message.text_content:
            segments.append({"type": "text", "data": {"text": message.text_content}})
        for attachment in message.attachments:
            segment = self._attachment_segment(attachment)
            if segment:
                segments.append(segment)
        if not segments:
            return None, {}
        params["message"] = segments
        return "send_msg", params

    def _attachment_segment(self, attachment: Attachment) -> Optional[Dict[str, Any]]:
        location = attachment.path or attachment.url or attachment.file_id
        if attachment.type == "image":
            if attachment.base64:
                return {"type": "image", "data": {"file": attachment.base64}}
            if location:
                return {"type": "image", "data": {"file": location}}
        if attachment.type in {"audio", "voice"} and location:
            return {"type": "record", "data": {"file": location}}
        if attachment.type == "video" and location:
            return {"type": "video", "data": {"file": location}}
        if attachment.type == "file" and location:
            return {"type": "file", "data": {"file": location}}
        return None

    async def _send_raw(self, connection_id: str, payload: Dict[str, Any]) -> bool:
        ws = self._clients.get(connection_id)
        if not ws:
            return False
        try:
            await ws.send(json.dumps(payload, ensure_ascii=False))
            self.logger.debug("→ %s %s", connection_id, payload.get("action"))
            return True
        except ConnectionClosed:
            self._clients.pop(connection_id, None)
            self.logger.warning("发送时连接已关闭: %s", connection_id)
            return False
        except Exception as exc:  # noqa: BLE001
            self._count_error(exc)
            self.logger.exception("向 %s 发送失败: %s", connection_id, exc)
            return False

    # ------------------------------------------------------------------ 状态
    def get_status(self) -> Dict[str, Any]:
        status = super().get_status()
        status.update({
            "listen": f"ws://{self.host}:{self.port}{self.event_path}",
            "clients": len(self._clients),
            "self_id": self._self_id,
            "token": bool(self.access_token),
        })
        return status


def _as_int(value: Any) -> Any:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return value
