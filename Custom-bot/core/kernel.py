"""内核：装配适配器、插件、数据库、调度与 WebUI，并负责消息分流。

生命周期：

    kernel = RobotKernel(load_config("config/config.yaml"))
    await kernel.start()     # 适配器监听 + 调度 + WebUI
    await kernel.wait()      # 阻塞到 Ctrl-C / SIGTERM
    await kernel.stop()
"""

from __future__ import annotations

import asyncio
import importlib
import logging
import signal
import time
from collections import deque
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional

from .adapters import BaseAdapter
from .config import Config
from .database import JsonDatabase
from .handlers import HandlerManager
from .message import Attachment, InternalMessage
from .mind import Mind
from .scheduler import Scheduler
from .utils import fmt_time, human_duration, truncate
from .webui import WebUI

logger = logging.getLogger("内核")


class RobotKernel:
    def __init__(self, config: Config):
        self.config = config
        self.root: Path = (config.path.parent.parent if config.path else Path.cwd()).resolve()
        self.version: str = str(config.get("kernel.version", "1.0.0"))
        self.log_level: str = str(config.get("kernel.log_level", "INFO"))
        self.admins: set[str] = {str(a) for a in (config.get("kernel.admins", []) or [])}
        self.adapters: Dict[str, BaseAdapter] = {}
        self.db = JsonDatabase(self._resolve(config.get("database.path", "data/db")))
        self.handlers = HandlerManager(self, self._resolve("plugins"))
        self.scheduler = Scheduler(self, self._resolve("scripts"))
        self.webui = WebUI(self)
        self.mind = Mind(self)
        self.start_time = time.time()
        self.messages_handled = 0
        self.commands_handled = 0
        self.errors = 0
        self._stop_event = asyncio.Event()
        self._semaphore = asyncio.Semaphore(int(config.get("kernel.max_concurrent", 16)))
        self._recent: Deque[Dict[str, Any]] = deque(
            maxlen=int(config.get("kernel.message_retention", 200))
        )

    # ------------------------------------------------------------------ 路径
    def _resolve(self, relative: str | Path) -> Path:
        path = Path(relative)
        return path if path.is_absolute() else (self.root / path)

    # ------------------------------------------------------------------ 装配
    async def setup(self) -> None:
        problems = self.config.validate()
        for problem in problems:
            logger.warning("配置问题: %s", problem)
        await self._load_adapters()
        await self.mind.setup()
        await self.handlers.load_all()
        logger.info("内核装配完成：%d 个适配器、%d 个插件", len(self.adapters), len(self.handlers.plugins))

    def _load_adapter_class(self, dotted: str):
        module_name, _, cls_name = dotted.rpartition(".")
        if not module_name or not cls_name:
            raise ValueError(f"适配器 class 路径不合法: {dotted}")
        module = importlib.import_module(module_name)
        return getattr(module, cls_name)

    async def _load_adapters(self) -> None:
        for adapter_id, item in self.config.iter_adapters():
            if not item.get("enabled", False):
                logger.info("适配器 %s 未启用，跳过", adapter_id)
                continue
            try:
                cls = self._load_adapter_class(str(item["class"]))
                adapter: BaseAdapter = cls(self, adapter_id, item.get("config", {}) or {})
                await adapter.setup()
                self.adapters[adapter_id] = adapter
            except Exception as exc:  # noqa: BLE001 - 一个适配器坏掉不影响其它
                logger.exception("装配适配器 %s 失败: %s", adapter_id, exc)

    # ------------------------------------------------------------------ 启动
    async def start(self) -> None:
        tasks = [self._start_adapter(adapter) for adapter in self.adapters.values()]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        await self.scheduler.start()
        try:
            await self.webui.start()
        except OSError as exc:
            logger.error("WebUI 启动失败（端口 %s 可能被占用）: %s", self.config.get("webui.port"), exc)
        logger.info("Custom-bot 已就绪，版本 %s", self.version)

    async def _start_adapter(self, adapter: BaseAdapter) -> None:
        try:
            await adapter.start()
        except Exception as exc:  # noqa: BLE001
            adapter._count_error(exc)
            logger.exception("适配器 %s 启动失败: %s", adapter.adapter_id, exc)

    async def run(self) -> None:
        await self.setup()
        await self.start()
        self._install_signal_handlers()
        await self._stop_event.wait()
        await self.stop()

    def _install_signal_handlers(self) -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self.request_stop)
            except (NotImplementedError, RuntimeError, ValueError):
                # Windows 的 ProactorEventLoop 不支持，退化为 KeyboardInterrupt
                pass

    def request_stop(self) -> None:
        if not self._stop_event.is_set():
            logger.info("收到退出信号，正在关闭…")
            self._stop_event.set()

    async def wait(self) -> None:
        await self._stop_event.wait()

    async def stop(self) -> None:
        timeout = float(self.config.get("kernel.shutdown_timeout", 10))
        for adapter in list(self.adapters.values()):
            try:
                await asyncio.wait_for(adapter.stop(), timeout=timeout)
            except Exception as exc:  # noqa: BLE001
                logger.warning("停止适配器 %s 时出错: %s", adapter.adapter_id, exc)
        try:
            await asyncio.wait_for(self.scheduler.stop(), timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            logger.warning("停止调度器时出错: %s", exc)
        try:
            await asyncio.wait_for(self.webui.stop(), timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            logger.warning("停止 WebUI 时出错: %s", exc)
        try:
            await asyncio.wait_for(self.mind.close(), timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            logger.warning("停止心智时出错: %s", exc)
        await self.db.close()
        logger.info("Custom-bot 已退出（运行 %s）", human_duration(time.time() - self.start_time))

    # ------------------------------------------------------------------ 消息
    async def handle_message(self, message: InternalMessage) -> None:
        """适配器收到的消息统一进这里。"""
        self.messages_handled += 1
        self._recent.append({
            "time": fmt_time(message.timestamp),
            "adapter": message.adapter_id,
            "session": "群 " + str(message.group_id) if message.is_group else "私聊",
            "user": message.user_name or message.user_id or "?",
            "text": truncate(message.text_content, 120),
            "type": message.msg_type,
        })

        if message.is_event:
            logger.debug("事件消息: %s %s", message.msg_type, message.metadata.get("onebot_event", ""))
            await self.handlers.dispatch(message)
            return

        logger.info("收到消息 %s", message.brief())
        async with self._semaphore:
            handled = await self.handlers.dispatch(message)
        if handled:
            self.commands_handled += 1

    async def reply(self, message: InternalMessage, text: str = "", **metadata: Any) -> bool:
        if not text:
            return False
        return await self.send(message.make_reply(text, **metadata))

    async def send(self, message: InternalMessage) -> bool:
        adapter = self.adapters.get(message.adapter_id)
        if not adapter:
            logger.warning("找不到适配器 %s，消息无处可发", message.adapter_id)
            return False
        try:
            ok = await adapter.send(message)
        except Exception as exc:  # noqa: BLE001
            self.errors += 1
            logger.exception("适配器 %s 发送失败: %s", message.adapter_id, exc)
            return False
        if ok:
            adapter._count_sent()
        return bool(ok)

    async def send_to_admins(self, text: str) -> bool:
        """按第一个可用适配器，给所有管理员发私聊。"""
        adapter = next((a for a in self.adapters.values() if a.is_running), None)
        if not adapter:
            logger.warning("没有运行中的适配器，无法通知管理员")
            return False
        sent = False
        for admin in sorted(self.admins):
            msg = InternalMessage(
                adapter_id=adapter.adapter_id,
                protocol=adapter.protocol_name,
                user_id=admin,
                msg_type="text",
                text_content=text,
                direction="out",
                metadata={"admin_broadcast": True},
            )
            sent = await self.send(msg) or sent
        return sent

    def is_admin(self, message: InternalMessage) -> bool:
        if "*" in self.admins:
            return True
        return bool(message.user_id and str(message.user_id) in self.admins)

    # ------------------------------------------------------------------ 状态
    def status(self) -> Dict[str, Any]:
        adapters = [a.get_status() for a in self.adapters.values()]
        plugins = self.handlers.list_plugins()
        return {
            "kernel": {
                "version": self.version,
                "uptime": human_duration(time.time() - self.start_time),
                "started_at": fmt_time(self.start_time),
                "log_level": self.log_level,
                "root": str(self.root),
            },
            "adapters": adapters,
            "adapter_summary": {
                "total": len(adapters),
                "running": sum(1 for a in adapters if a.get("running")),
            },
            "plugins": plugins,
            "plugin_summary": {
                "total": len(plugins),
                "enabled": sum(1 for p in plugins if p.get("enabled")),
            },
            "tasks": self.scheduler.list(),
            "messages_handled": self.messages_handled,
            "commands_handled": self.commands_handled,
            "errors": self.errors,
            "recent_messages": list(self._recent)[-20:],
            "mind": self.mind.status(),
            "webui": {"running": self.webui.is_running(), "port": self.webui.port},
        }
