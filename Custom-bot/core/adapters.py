"""适配器基类。

约定：适配器只做协议翻译——把平台事件变成 `InternalMessage` 交给内核，
把内核给的 `InternalMessage` 变成平台 API 调用。业务逻辑一律放在插件里。
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional

from .message import InternalMessage
from .utils import fmt_time, human_duration

if TYPE_CHECKING:  # pragma: no cover - 仅类型检查用，避免循环导入
    from .kernel import RobotKernel


class BaseAdapter(ABC):
    """所有协议适配器的共同父类。"""

    kind: str = "base"

    def __init__(self, kernel: "RobotKernel", adapter_id: str, config: Dict[str, Any]):
        self.kernel = kernel
        self.adapter_id = str(adapter_id)
        self.config: Dict[str, Any] = dict(config or {})
        self.protocol_name: str = str(self.config.get("protocol_name") or self.adapter_id)
        self.logger = logging.getLogger(f"适配器.{self.adapter_id}")
        self.is_running = False
        self.created_at = time.time()
        self.started_at: Optional[float] = None
        self.last_error: Optional[str] = None
        self.stats: Dict[str, int] = {"received": 0, "sent": 0, "errors": 0}
        self._meta: Dict[str, Any] = {}

    # ------------------------------------------------------------------ 生命周期
    async def setup(self) -> None:
        """准备阶段：只做无副作用的初始化，不监听端口。"""
        self.logger.debug("适配器 '%s' 完成 setup（协议 %s）", self.adapter_id, self.protocol_name)

    async def start(self) -> None:
        """启动。子类应调用 `await super().start()` 再开始监听。"""
        self.is_running = True
        self.started_at = time.time()
        self.logger.info("适配器 '%s' 已启动（协议 %s）", self.adapter_id, self.protocol_name)

    async def stop(self) -> None:
        """停止。子类应调用 `await super().stop()` 收尾。"""
        self.is_running = False
        self.logger.info("适配器 '%s' 已停止", self.adapter_id)

    # ------------------------------------------------------------------ 收发
    @abstractmethod
    async def send(self, message: InternalMessage) -> bool:
        """把一条出站消息发给平台。返回是否成功。"""

    async def _push_to_kernel(self, message: InternalMessage) -> None:
        """适配器收到消息后统一走这里，便于统计与异常隔离。"""
        self.stats["received"] += 1
        try:
            await self.kernel.handle_message(message)
        except Exception as exc:  # noqa: BLE001 - 单条消息失败不能拖垮连接
            self.stats["errors"] += 1
            self.last_error = f"{type(exc).__name__}: {exc}"
            self.logger.exception("把消息交给内核时出错: %s", exc)

    def _count_sent(self) -> None:
        self.stats["sent"] += 1

    def _count_error(self, error: Any) -> None:
        self.stats["errors"] += 1
        self.last_error = str(error) if error else "unknown"

    # ------------------------------------------------------------------ 状态
    def get_status(self) -> Dict[str, Any]:
        uptime = time.time() - (self.started_at or self.created_at)
        return {
            "id": self.adapter_id,
            "kind": self.kind,
            "class": f"{type(self).__module__}.{type(self).__name__}",
            "protocol": self.protocol_name,
            "running": self.is_running,
            "uptime": human_duration(uptime) if self.is_running else "—",
            "started_at": fmt_time(self.started_at) if self.started_at else None,
            "stats": dict(self.stats),
            "last_error": self.last_error,
            **self._meta,
        }

    def status_extra(self, **values: Any) -> None:
        """子类登记要出现在 /api/status 里的额外字段。"""
        self._meta.update(values)

    def __repr__(self) -> str:  # pragma: no cover - 调试用
        return f"<{type(self).__name__} id={self.adapter_id} running={self.is_running}>"
