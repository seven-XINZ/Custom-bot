"""框架内部消息模型。

所有适配器把各自协议翻译成 `InternalMessage`，内核与插件只认这一种结构；
回复消息同样用 `InternalMessage`，由内核找到原适配器发出去。
"""

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class Attachment:
    """一份附件。四个位置字段至少填一个，具体由适配器解释。"""

    type: str = "file"  # image / audio / video / file
    path: Optional[str] = None
    url: Optional[str] = None
    file_id: Optional[str] = None
    base64: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class InternalMessage:
    """一条进站或出站消息。"""

    adapter_id: str
    protocol: str = ""
    # 会话定位
    connection_id: Optional[str] = None
    session_id: Optional[str] = None
    # 发送者
    user_id: Optional[str] = None
    user_name: str = ""
    # 群（私聊为 None）
    group_id: Optional[str] = None
    group_name: Optional[str] = None
    # 消息本体
    msg_id: Optional[str] = None
    msg_type: str = "text"
    text_content: str = ""
    attachments: List[Attachment] = field(default_factory=list)
    # 原始数据，排障用
    parsed_data: Any = None
    raw_data: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    # 框架字段
    timestamp: float = field(default_factory=time.time)
    internal_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    direction: str = "in"  # in / out
    reply_to: Optional[str] = None

    # ---------------------------------------------------------------- 便捷判断
    @property
    def is_group(self) -> bool:
        return bool(self.group_id) and str(self.group_id) != "0"

    @property
    def is_private(self) -> bool:
        return not self.is_group

    @property
    def is_event(self) -> bool:
        return self.msg_type in {"event", "notice", "meta"}

    @property
    def session_key(self) -> str:
        """同一会话的消息共享一个 key，用于会话级状态。"""
        return f"{self.adapter_id}:{self.group_id or self.user_id or 'unknown'}"

    def brief(self) -> str:
        where = f"群{self.group_id}" if self.is_group else "私聊"
        return f"[{self.adapter_id}/{where}] {self.user_name or self.user_id}: {self.text_content[:60]}"

    # ---------------------------------------------------------------- 回复构造
    def make_reply(
        self,
        text: str = "",
        attachments: Optional[List[Attachment]] = None,
        msg_type: str = "text",
        **metadata: Any,
    ) -> "InternalMessage":
        """生成一条指向同一会话的回复消息，不修改原消息。"""
        meta: Dict[str, Any] = {"reply_to_msg_id": self.msg_id}
        meta.update(metadata)
        return InternalMessage(
            adapter_id=self.adapter_id,
            protocol=self.protocol,
            connection_id=self.connection_id,
            session_id=self.session_id,
            user_id=self.user_id,
            user_name=self.user_name,
            group_id=self.group_id,
            group_name=self.group_name,
            msg_type=msg_type,
            text_content=text,
            attachments=list(attachments or []),
            metadata=meta,
            direction="out",
            reply_to=self.internal_id,
        )

    # ---------------------------------------------------------------- 序列化
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["attachments"] = [a.to_dict() if isinstance(a, Attachment) else a for a in self.attachments]
        # 原始数据可能包含不可 JSON 序列化的对象
        data["parsed_data"] = _jsonable(self.parsed_data)
        data["raw_data"] = _jsonable(self.raw_data)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InternalMessage":
        attachments = [
            a if isinstance(a, Attachment) else Attachment(**a)
            for a in (data.get("attachments") or [])
            if isinstance(a, dict)
        ]
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in known and k != "attachments"}
        filtered["attachments"] = attachments
        return cls(**filtered)


def _jsonable(value: Any) -> Any:
    """把 bytes / 自定义对象降级成可 JSON 化的形式。"""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, bytes):
        return {"__bytes__": True, "length": len(value)}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    return repr(value)
