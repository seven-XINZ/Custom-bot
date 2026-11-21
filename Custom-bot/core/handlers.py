"""插件与命令调度。

插件是一个普通 Python 模块，暴露：

    NAME = "基础命令"
    VERSION = "1.0"
    DESCRIPTION = "…"

    async def setup(ctx: PluginContext):
        @ctx.command("ping", description="连通性测试")
        async def ping(c: CommandContext):
            return "pong"

命令处理器可以返回字符串（内核自动回复）、字符串列表（多条）、或 None（不回复）。
"""

from __future__ import annotations

import asyncio
import importlib
import inspect
import logging
import shlex
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

from .message import InternalMessage
from .utils import fmt_time, truncate

logger = logging.getLogger("内核.处理器")

HandlerFn = Callable[["CommandContext"], Any]


@dataclass(slots=True)
class Command:
    name: str
    handler: HandlerFn
    plugin: str
    aliases: tuple[str, ...] = ()
    description: str = ""
    usage: str = ""
    admin_only: bool = False
    hidden: bool = False
    timeout: float = 0.0

    @property
    def all_names(self) -> tuple[str, ...]:
        return (self.name, *self.aliases)


@dataclass
class PluginRuntime:
    """一个已加载插件的运行时快照。"""

    name: str
    module_name: str
    path: Path
    description: str = ""
    version: str = ""
    author: str = ""
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    commands: List[Command] = field(default_factory=list)
    listeners: List[HandlerFn] = field(default_factory=list)
    calls: int = 0
    errors: int = 0
    last_error: str = ""
    last_call_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "module": self.module_name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "enabled": self.enabled,
            "commands": [c.name for c in self.commands],
            "calls": self.calls,
            "errors": self.errors,
            "last_error": self.last_error,
            "last_call_at": fmt_time(self.last_call_at) if self.last_call_at else None,
        }


class PluginContext:
    """交给插件的注册入口。"""

    def __init__(self, manager: "HandlerManager", runtime: PluginRuntime):
        self.manager = manager
        self.kernel = manager.kernel
        self.name = runtime.name
        self.runtime = runtime
        self.config: Dict[str, Any] = runtime.config
        self.logger = logging.getLogger(f"插件.{runtime.name}")

    def command(
        self,
        name: str,
        *,
        aliases: Iterable[str] = (),
        description: str = "",
        usage: str = "",
        admin_only: bool = False,
        hidden: bool = False,
        timeout: float = 0.0,
    ) -> Callable[[HandlerFn], HandlerFn]:
        def decorator(func: HandlerFn) -> HandlerFn:
            self.manager.register_command(
                self.runtime,
                Command(
                    name=name.strip(),
                    handler=func,
                    plugin=self.runtime.name,
                    aliases=tuple(a.strip() for a in aliases if a.strip()),
                    description=description,
                    usage=usage,
                    admin_only=admin_only,
                    hidden=hidden,
                    timeout=timeout,
                ),
            )
            return func

        return decorator

    def on_message(self, func: HandlerFn) -> HandlerFn:
        """注册非命令监听器：所有进站消息都会经过它（可返回 None）。"""
        self.runtime.listeners.append(func)
        return func


class CommandContext:
    """一次命令执行的全部上下文。"""

    def __init__(self, kernel, plugin: PluginContext, command: Command,
                 message: InternalMessage, args: List[str], raw_args: str):
        self.kernel = kernel
        self.plugin = plugin
        self.command = command
        self.message = message
        self.args = args
        self.raw_args = raw_args

    async def reply(self, text: str = "", **metadata: Any) -> bool:
        return await self.kernel.reply(self.message, text, **metadata)

    async def send(self, text: str, *, to: Optional[str] = None) -> bool:
        """发到当前会话；`to` 目前只支持 "admin"（发给所有管理员私聊）。"""
        if to == "admin":
            return await self.kernel.send_to_admins(text)
        return await self.kernel.reply(self.message, text)

    @property
    def is_admin(self) -> bool:
        return self.kernel.is_admin(self.message)

    @property
    def config(self) -> Dict[str, Any]:
        return self.plugin.config

    @property
    def db(self):
        return self.kernel.db

    @property
    def text(self) -> str:
        return self.message.text_content

    @property
    def user_id(self) -> Optional[str]:
        return self.message.user_id


class HandlerManager:
    def __init__(self, kernel, plugins_dir: Path):
        self.kernel = kernel
        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, PluginRuntime] = {}
        self._commands: Dict[str, Command] = {}
        self.prefixes: tuple[str, ...] = tuple(
            kernel.config.get("kernel.command_prefixes", ["/"]) or [""]
        )

    # ------------------------------------------------------------------ 注册
    def register_command(self, runtime: PluginRuntime, command: Command) -> None:
        key = command.name.lower()
        if key in self._commands:
            other = self._commands[key]
            logger.warning("命令 %s 已被插件 %s 注册，%s 的版本被忽略", command.name, other.plugin, runtime.name)
            return
        self._commands[key] = command
        for alias in command.aliases:
            alias_key = alias.lower()
            if alias_key not in self._commands:
                self._commands[alias_key] = command
        runtime.commands.append(command)

    # ------------------------------------------------------------------ 发现
    def discover(self) -> List[Path]:
        if not self.plugins_dir.is_dir():
            return []
        found: List[Path] = []
        for path in sorted(self.plugins_dir.rglob("*.py")):
            rel = path.relative_to(self.plugins_dir)
            if any(part.startswith("_") for part in rel.parts):
                continue
            if path.name == "__init__.py":
                continue
            found.append(path)
        return found

    def _module_name(self, path: Path) -> str:
        rel = path.relative_to(self.plugins_dir).with_suffix("")
        parts = ["plugins", *rel.parts]
        return ".".join(parts)

    async def load_all(self) -> None:
        for path in self.discover():
            try:
                await self.load_plugin(path)
            except Exception as exc:  # noqa: BLE001 - 单个插件坏掉不阻塞启动
                logger.exception("加载插件 %s 失败: %s", path, exc)

    def _handler_cfg(self, name: str) -> Dict[str, Any]:
        cfg = self.kernel.config.get("handlers", {}) or {}
        item = cfg.get(name)
        return item if isinstance(item, dict) else {}

    async def _enabled_state(self, name: str, default: bool) -> bool:
        override = await self.kernel.db.get("plugins", name)
        if isinstance(override, dict) and "enabled" in override:
            return bool(override["enabled"])
        return default

    async def load_plugin(self, path: Path) -> Optional[PluginRuntime]:
        module_name = self._module_name(path)
        module = importlib.import_module(module_name)
        if not hasattr(module, "setup"):
            logger.warning("插件 %s 没有 setup(ctx)，跳过", module_name)
            return None

        name = str(getattr(module, "NAME", path.stem))
        cfg = self._handler_cfg(name)
        default_enabled = bool(cfg.get("enabled", True))
        enabled = await self._enabled_state(name, default_enabled)

        runtime = PluginRuntime(
            name=name,
            module_name=module_name,
            path=path,
            description=str(getattr(module, "DESCRIPTION", "")),
            version=str(getattr(module, "VERSION", "")),
            author=str(getattr(module, "AUTHOR", "")),
            config=dict(cfg.get("config", {}) or {}),
            enabled=enabled,
        )
        # 未启用的插件也要注册命令，只是 dispatch 时跳过；这样 WebUI 能看到它有什么命令
        ctx = PluginContext(self, runtime)
        await _maybe_await(module.setup(ctx))
        self.plugins[name] = runtime
        logger.info("插件已加载: %s（%d 条命令，%s）", name, len(runtime.commands),
                    "启用" if enabled else "停用")
        return runtime

    async def reload_plugin(self, name: str) -> PluginRuntime:
        runtime = self.plugins.get(name)
        if not runtime:
            raise KeyError(f"没有名为 {name} 的插件")
        for cmd in runtime.commands:
            self._commands.pop(cmd.name.lower(), None)
            for alias in cmd.aliases:
                self._commands.pop(alias.lower(), None)
        for key, cmd in list(self._commands.items()):
            if cmd.plugin == name:
                self._commands.pop(key, None)
        module = importlib.import_module(runtime.module_name)
        module = importlib.reload(module)
        return await self.load_plugin(runtime.path)

    async def set_enabled(self, name: str, enabled: bool) -> bool:
        runtime = self.plugins.get(name)
        if not runtime:
            raise KeyError(f"没有名为 {name} 的插件")
        runtime.enabled = bool(enabled)
        await self.kernel.db.set("plugins", name, {"enabled": bool(enabled), "updated_at": time.time()})
        logger.info("插件 %s 已%s", name, "启用" if enabled else "停用")
        return runtime.enabled

    # ------------------------------------------------------------------ 匹配
    def parse(self, text: str) -> Optional[tuple[Command, List[str], str]]:
        stripped = (text or "").strip()
        if not stripped:
            return None
        body = stripped
        used_prefix = ""
        for prefix in self.prefixes:
            if prefix and stripped.startswith(prefix):
                body = stripped[len(prefix):].lstrip()
                used_prefix = prefix
                break
        if not body:
            return None
        first, _, rest = body.partition(" ")
        command = self._commands.get(first.lower())
        if command is None and used_prefix:
            return None
        if command is None:
            # 无前缀时只认完全等于命令名的整句，避免普通聊天误触发
            command = self._commands.get(stripped.lower())
            if command is None:
                return None
            rest = ""
        args = _split_args(rest)
        return command, args, rest.strip()

    async def dispatch(self, message: InternalMessage) -> bool:
        # 1) 非命令监听器：事件消息也能进来
        any_listener = False
        for runtime in self.plugins.values():
            if not runtime.enabled or not runtime.listeners:
                continue
            for listener in runtime.listeners:
                any_listener = True
                try:
                    await _maybe_await(listener(message))
                except Exception as exc:  # noqa: BLE001
                    runtime.errors += 1
                    runtime.last_error = str(exc)
                    logger.exception("插件 %s 的消息监听器出错: %s", runtime.name, exc)

        if message.is_event:
            return any_listener

        # 2) 命令
        parsed = self.parse(message.text_content)
        if not parsed:
            return any_listener
        command, args, raw_args = parsed
        runtime = self.plugins.get(command.plugin)
        if not runtime or not runtime.enabled:
            # 插件被停用后，它的 enable 指令也跟着失效，会造成「只能靠 WebUI 恢复」的死角。
            # 因此这几个管理动作在内核层保留兜底实现。
            if await self._builtin_admin(command, message, args, raw_args):
                return True
            return any_listener
        if command.admin_only and not self.kernel.is_admin(message):
            await self.kernel.reply(message, "这条命令需要管理员权限。")
            return True

        plugin_ctx = PluginContext(self, runtime)
        ctx = CommandContext(self.kernel, plugin_ctx, command, message, args, raw_args)
        timeout = command.timeout or float(self.kernel.config.get("kernel.plugin_timeout", 15))
        runtime.calls += 1
        runtime.last_call_at = time.time()
        try:
            result = await asyncio.wait_for(_maybe_await(command.handler(ctx)), timeout=timeout)
            await self._deliver(result, message)
        except asyncio.TimeoutError:
            runtime.errors += 1
            runtime.last_error = "timeout"
            await self.kernel.reply(message, f"命令 {command.name} 执行超时（{timeout:g}s）。")
        except Exception as exc:  # noqa: BLE001 - 插件异常不能打挂内核
            runtime.errors += 1
            runtime.last_error = f"{type(exc).__name__}: {exc}"
            logger.exception("命令 %s 执行失败: %s", command.name, exc)
            await self.kernel.reply(message, f"命令 {command.name} 执行出错，已记录日志。")
        return True

    _BUILTIN_ADMIN_NAMES = {"enable", "disable", "reload", "启用", "停用", "重载"}

    async def _builtin_admin(self, command: Command, message: InternalMessage,
                             args: List[str], raw_args: str) -> bool:
        """插件停用后的管理命令兜底（仅在插件不可用时触发）。"""
        name = command.name.lower()
        if name not in self._BUILTIN_ADMIN_NAMES:
            return False
        if not self.kernel.is_admin(message):
            return False
        target = args[0] if args else ""
        if not target:
            await self.kernel.reply(message, f"用法：{command.name} <插件名>")
            return True

        if name in {"reload", "重载"}:
            try:
                runtime = await self.reload_plugin(target)
            except Exception as exc:  # noqa: BLE001
                await self.kernel.reply(message, f"重载「{target}」失败：{exc}")
                return True
            await self.kernel.reply(
                message, f"已重载「{runtime.name}」，当前 {len(runtime.commands)} 条命令。")
            return True

        enabled = name in {"enable", "启用"}
        ok = await self.set_enabled(target, enabled)
        if not ok:
            await self.kernel.reply(message, f"没有找到插件「{target}」。")
        else:
            await self.kernel.reply(message, "已启用「%s」。" % target if enabled else "已停用「%s」。" % target)
        return True

    async def _deliver(self, result: Any, message: InternalMessage) -> None:
        if result is None:
            return
        if isinstance(result, str):
            await self.kernel.reply(message, result)
            return
        if isinstance(result, (list, tuple)):
            for line in result:
                if line:
                    await self.kernel.reply(message, str(line))
            return
        if isinstance(result, dict) and "text" in result:
            await self.kernel.reply(message, str(result["text"]))

    # ------------------------------------------------------------------ 视图
    def list_plugins(self) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in self.plugins.values()]

    def list_commands(self) -> List[Dict[str, Any]]:
        seen: Dict[int, Command] = {}
        for cmd in self._commands.values():
            seen[id(cmd)] = cmd
        out = []
        for cmd in seen.values():
            runtime = self.plugins.get(cmd.plugin)
            out.append({
                "name": cmd.name,
                "aliases": list(cmd.aliases),
                "plugin": cmd.plugin,
                "description": cmd.description,
                "usage": cmd.usage,
                "admin_only": cmd.admin_only,
                "hidden": cmd.hidden,
                "enabled": bool(runtime and runtime.enabled),
            })
        return sorted(out, key=lambda x: (x["plugin"], x["name"]))


def _split_args(text: str) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value
