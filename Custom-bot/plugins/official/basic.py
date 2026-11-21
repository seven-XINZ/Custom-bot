"""官方基础命令插件。

覆盖日常运维要用的几条：帮助、ping、版本、状态、插件列表，
以及管理员专用的重载 / 启停 / 广播。
"""

from __future__ import annotations

import time
from typing import Any, Dict, List

from core.handlers import CommandContext, PluginContext

NAME = "基础命令"
VERSION = "1.1"
DESCRIPTION = "帮助、版本、状态、插件管理"
AUTHOR = "Xinz"

# 帮助里不展示的内部命令
INTERNAL = {"echo"}


async def setup(ctx: PluginContext):
    manager = ctx.manager
    plugin_cfg = ctx.config or {}
    extra_admins = {str(a) for a in (plugin_cfg.get("admins") or []) if str(a).strip()}

    @ctx.command("help", aliases=["帮助", "菜单"], description="查看命令列表或某条命令的用法",
                 usage="帮助 [命令]")
    async def help_command(c: CommandContext):
        commands = manager.list_commands()
        if c.args:
            target = c.args[0].lower()
            for item in commands:
                names = [item["name"], *item["aliases"]]
                if target in [n.lower() for n in names]:
                    lines = [f"{item['name']} — {item['description'] or '无说明'}"]
                    if item["usage"]:
                        lines.append(f"用法：{item['usage']}")
                    if item["aliases"]:
                        lines.append("别名：" + "、".join(item["aliases"]))
                    if item["admin_only"]:
                        lines.append("权限：仅管理员")
                    lines.append(f"所属插件：{item['plugin']}")
                    return lines
            return f"没找到命令「{c.args[0]}」，发「帮助」看全部。"

        visible = [x for x in commands if not x["hidden"] and x["name"] not in INTERNAL]
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for item in visible:
            grouped.setdefault(item["plugin"], []).append(item)
        lines = ["可用命令："]
        for plugin_name, items in sorted(grouped.items()):
            lines.append("· " + plugin_name + "：" + "、".join(i["name"] for i in items))
        lines.append("发「帮助 命令名」看具体用法。")
        return lines

    @ctx.command("ping", description="连通性测试", usage="ping")
    async def ping(c: CommandContext):
        started = time.perf_counter()
        await c.reply(f"pong（{(time.perf_counter() - started) * 1000:.0f}ms）")
        return None

    @ctx.command("version", aliases=["版本"], description="查看框架版本与运行时长")
    async def version(c: CommandContext):
        data = c.kernel.status()
        return [
            f"Custom-bot {data['kernel']['version']}",
            f"已运行 {data['kernel']['uptime']}",
            f"适配器 {data['adapter_summary']['running']}/{data['adapter_summary']['total']} 运行",
            f"插件 {data['plugin_summary']['enabled']}/{data['plugin_summary']['total']} 启用",
            f"已处理 {data['messages_handled']} 条消息",
        ]

    @ctx.command("status", aliases=["状态"], description="查看适配器与插件当前状态")
    async def status(c: CommandContext):
        data = c.kernel.status()
        lines = [f"内核 {data['kernel']['version']}，运行 {data['kernel']['uptime']}"]
        for adapter in data["adapters"]:
            mark = "运行" if adapter["running"] else "停止"
            lines.append(f"[{mark}] {adapter['id']}（{adapter['protocol']}）"
                         f"收 {adapter['stats']['received']} / 发 {adapter['stats']['sent']}")
        disabled = [p["name"] for p in data["plugins"] if not p["enabled"]]
        if disabled:
            lines.append("已停用插件：" + "、".join(disabled))
        return lines

    @ctx.command("plugins", aliases=["插件"], description="列出插件与命令数量")
    async def plugins(c: CommandContext):
        lines = []
        for item in c.kernel.handlers.list_plugins():
            state = "启用" if item["enabled"] else "停用"
            lines.append(f"[{state}] {item['name']} v{item['version'] or '?'} — "
                         f"{len(item['commands'])} 条命令，调用 {item['calls']} 次")
        return lines or ["还没有加载任何插件。"]

    @ctx.command("id", description="查看自己的用户 ID / 群 ID（配置管理员时用）")
    async def whoami(c: CommandContext):
        lines = [f"user_id: {c.user_id or '未知'}"]
        if c.message.group_id:
            lines.append(f"group_id: {c.message.group_id}")
        lines.append(f"适配器: {c.message.adapter_id} / 协议: {c.message.protocol or '未标注'}")
        lines.append("是管理员" if c.is_admin else "不是管理员")
        return lines

    @ctx.command("echo", description="原样回显参数（调试用）", hidden=True)
    async def echo(c: CommandContext):
        return c.raw_args or "（空）"

    # ------------------------------------------------------------------ 管理员
    @ctx.command("reload", aliases=["重载"], description="热重载指定插件",
                 usage="重载 <插件名>", admin_only=True)
    async def reload_plugin(c: CommandContext):
        if not c.args:
            return "用法：重载 <插件名>"
        name = c.args[0]
        try:
            runtime = await c.kernel.handlers.reload_plugin(name)
        except KeyError:
            return f"没有名为「{name}」的插件。发「插件」看列表。"
        except Exception as exc:  # noqa: BLE001
            return f"重载失败：{type(exc).__name__}: {exc}"
        return f"已重载「{runtime.name}」，当前 {len(runtime.commands)} 条命令。"

    @ctx.command("enable", aliases=["启用"], description="启用插件",
                 usage="启用 <插件名>", admin_only=True)
    async def enable_plugin(c: CommandContext):
        if not c.args:
            return "用法：启用 <插件名>"
        try:
            await c.kernel.handlers.set_enabled(c.args[0], True)
        except KeyError:
            return f"没有名为「{c.args[0]}」的插件。"
        return f"已启用「{c.args[0]}」。"

    @ctx.command("disable", aliases=["停用"], description="停用插件",
                 usage="停用 <插件名>", admin_only=True)
    async def disable_plugin(c: CommandContext):
        if not c.args:
            return "用法：停用 <插件名>"
        try:
            await c.kernel.handlers.set_enabled(c.args[0], False)
        except KeyError:
            return f"没有名为「{c.args[0]}」的插件。"
        return f"已停用「{c.args[0]}」。"

    @ctx.command("broadcast", aliases=["广播"], description="给所有管理员私聊发通知",
                 usage="广播 <内容>", admin_only=True)
    async def broadcast(c: CommandContext):
        text = c.raw_args.strip()
        if not text:
            return "用法：广播 <内容>"
        sent = await c.kernel.send_to_admins(f"[广播] {c.message.user_name or c.user_id}: {text}")
        return "已发给管理员。" if sent else "没有可用适配器，发送失败。"

    if extra_admins:
        ctx.logger.debug("插件级管理员: %s", "、".join(sorted(extra_admins)))
