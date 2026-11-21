"""AI 心智插件：对话、记忆、人格、自省与代码提案。"""

from __future__ import annotations

import re
import time

from core.mind import BudgetExceeded, MindNotReady

NAME = "AI 心智"
VERSION = "1.0.0"
DESCRIPTION = "有记忆、有人格、会自省、能提插件/代码提案的对话内核"
AUTHOR = "seven-XINZ + AI"


async def setup(ctx):
    kernel = ctx.kernel
    mind = kernel.mind
    logger = ctx.logger

    # ---------------------------------------------------------------- 自动对话
    @ctx.on_message
    async def _on_any_message(message):
        if not mind.enabled:
            return
        text = (message.text_content or "").strip()
        if not text or kernel.handlers.parse(text):
            return
        mind.spawn_auto_reply(message)
        mind.schedule_learn(message)

    # ---------------------------------------------------------------- 对话
    @ctx.command("chat", aliases=["聊", "问"], description="和 AI 对话",
                 usage="chat <内容>", timeout=120)
    async def chat_cmd(c):
        text = (c.raw_args or "").strip()
        if not text:
            return "用法：/chat <内容>"
        try:
            return await mind.chat(c.message, text)
        except (MindNotReady, BudgetExceeded) as exc:
            return str(exc)
        except Exception as exc:  # noqa: BLE001
            logger.exception("对话失败：%s", exc)
            return "大脑暂时没有响应，稍后再试。"

    @ctx.command("brain", aliases=["心智"], description="查看 AI 心智状态",
                 usage="brain", timeout=30)
    async def brain_cmd(c):
        counts = await mind.memory.counts()
        lines = [
            f"状态：{'就绪' if mind.ready else '未就绪'}（{mind.client.model or '未配置模型'}）",
            f"人格：{mind.persona.get('name')}",
            f"今日调用：{mind._calls_today}/{mind.max_calls_per_day}",
            f"记忆：{counts['facts']} 条事实、{counts['episodes']} 段对话",
            f"待审提案：{sum(1 for p in mind.list_proposals(50) if p.get('status') == 'pending')}",
        ]
        if not mind.ready:
            lines.append("提示：在 config.yaml 的 brain 段填 base_url / model / api_key。")
        return lines

    # ---------------------------------------------------------------- 记忆
    @ctx.command("remember", aliases=["记住"], description="记住一条事实",
                 usage="remember 口味 = 微辣", timeout=30)
    async def remember_cmd(c):
        raw = (c.raw_args or "").strip()
        if not raw:
            return "用法：/remember 键 = 值（例如：/remember 口味 = 微辣）"
        match = re.match(r"(.+?)\s*(?:=|：|:)\s*(.+)", raw, re.S)
        if match:
            key, value = match.group(1).strip(), match.group(2).strip()
        else:
            parts = raw.split(None, 1)
            key, value = parts[0], (parts[1] if len(parts) > 1 else "")
        if not value:
            return "要记住什么？格式：/remember 键 = 值"
        await mind.memory.remember(key, value, owner=c.user_id or "",
                                   tags=["手动"], source=f"user:{c.user_id}")
        return f"记住了：{key} → {value}"

    @ctx.command("recall", aliases=["回忆"], description="检索长期记忆",
                 usage="recall <关键词>", timeout=30)
    async def recall_cmd(c):
        query = (c.raw_args or "").strip()
        if not query:
            return "要回忆什么？例如：/recall 口味"
        facts = await mind.memory.recall(query, owner=c.user_id or "", limit=6)
        if not facts:
            return "没有找到相关记忆。"
        return [f"- {f.get('label')}：{f.get('value')}" for f in facts]

    @ctx.command("forget", aliases=["忘掉"], description="删除一条记忆",
                 usage="forget <键>", timeout=30)
    async def forget_cmd(c):
        key = (c.raw_args or "").strip()
        if not key:
            return "用法：/forget <键>"
        if await mind.memory.forget(key, owner=c.user_id or ""):
            return f"已忘掉「{key}」。"
        if c.is_admin and await mind.memory.forget(key, owner=""):
            return f"已忘掉全局记忆「{key}」。"
        return "没找到这条记忆。"

    # ---------------------------------------------------------------- 人格
    @ctx.command("persona", aliases=["人格"], description="查看或修改人格设定",
                 usage="persona | persona set 键 值 | persona reset",
                 admin_only=True, timeout=30)
    async def persona_cmd(c):
        action = (c.args[0].lower() if c.args else "")
        if not action:
            info = mind.persona.describe()
            lines = [f"名字：{info.get('name')}"]
            if info.get("self_intro"):
                lines.append(f"自述：{info.get('self_intro')}")
            lines.append("性格：" + "、".join(info.get("traits") or []))
            lines.append("风格：" + str(info.get("style") or ""))
            lines.append("边界：" + "；".join(info.get("boundaries") or []))
            lines.append("改法：/persona set style 更简短一点")
            return lines
        if action == "reset":
            await mind.persona.reset(kernel.db)
            return "人格已恢复为配置默认值。"
        if action == "set":
            if len(c.args) < 3:
                return "用法：/persona set <字段> <值>（字段：name/self_intro/traits/style/boundaries）"
            key = c.args[1].lower()
            value = c.raw_args.split(None, 2)[2] if len(c.raw_args.split(None, 2)) > 2 else ""
            try:
                await mind.persona.set(kernel.db, key, value)
            except ValueError as exc:
                return str(exc)
            return f"已更新人格字段 {key}。"
        return "未知操作，可用：set / reset"

    # ---------------------------------------------------------------- 自省
    @ctx.command("reflect", aliases=["自省"], description="立即做一次自我反思",
                 admin_only=True, usage="reflect", timeout=120)
    async def reflect_cmd(c):
        try:
            return await mind.reflect()
        except (MindNotReady, BudgetExceeded) as exc:
            return str(exc)
        except Exception as exc:  # noqa: BLE001
            logger.exception("自省失败：%s", exc)
            return "自省失败，详见日志。"

    @ctx.command("journal", aliases=["日记"], description="查看最近的自省记录",
                 admin_only=True, usage="journal [条数]", timeout=30)
    async def journal_cmd(c):
        limit = int(c.args[0]) if c.args and c.args[0].isdigit() else 5
        entries = await mind.journal(limit)
        if not entries:
            return "还没有自省记录，发 /reflect 试试。"
        return [f"[{time.strftime('%m-%d %H:%M', time.localtime(e['created_at']))}] "
                f"{e.get('text', '')}" for e in entries]

    @ctx.command("feedback", aliases=["反馈"], description="给回复风格提意见",
                 usage="feedback 太啰嗦了", timeout=30)
    async def feedback_cmd(c):
        text = (c.raw_args or "").strip()
        if not text:
            return "用法：/feedback 你的意见"
        await mind.memory.remember(f"反馈-{int(time.time())}", text,
                                   tags=["反馈", "风格"], source=f"user:{c.user_id}")
        return "收到，这条会进入长期记忆，用来调整我的表达。"

    # ---------------------------------------------------------------- 提案
    @ctx.command("propose", aliases=["提案"], description="让 AI 写一个插件或改现有插件",
                 admin_only=True, usage="propose [--target 插件名] 需求", timeout=180)
    async def propose_cmd(c):
        raw = (c.raw_args or "").strip()
        target = ""
        match = re.search(r"--target(?:=|\s+)(\S+)", raw)
        if match:
            target = match.group(1)
            raw = (raw[:match.start()] + raw[match.end():]).strip()
        if not raw:
            return "用法：/propose 做一个骰子插件，命令 /roll 2d6"
        try:
            meta = await mind.propose(raw, target)
        except (MindNotReady, BudgetExceeded, ValueError) as exc:
            return str(exc)
        except Exception as exc:  # noqa: BLE001
            logger.exception("生成提案失败：%s", exc)
            return "生成提案失败，详见日志。"
        lines = [
            f"提案 {meta['id']} 已生成：{meta['kind']} / {meta['plugin_name']}",
            f"需求：{meta['requirement']}",
            f"目录：{mind.proposal_dir / meta['id']}/",
            f"应用：/approve {meta['id']}    放弃：/reject {meta['id']}",
        ]
        if meta.get("status") == "applied":
            lines.append("（auto_apply 已开启，提案已直接应用）")
        return lines

    @ctx.command("proposals", description="列出 AI 生成的插件提案",
                 admin_only=True, usage="proposals", timeout=30)
    async def proposals_cmd(c):
        items = mind.list_proposals(10)
        if not items:
            return "还没有提案。用 /propose <需求> 让 AI 写一个。"
        return [f"[{p.get('status')}] {p.get('id')} · {p.get('plugin_name')} · {p.get('summary')}"
                for p in items]

    @ctx.command("approve", description="应用一个提案",
                 admin_only=True, usage="approve <提案ID>", timeout=60)
    async def approve_cmd(c):
        pid = (c.args[0] if c.args else "").strip()
        if not pid:
            return "用法：/approve <提案ID>（/proposals 查看）"
        try:
            meta = await mind.approve(pid)
        except ValueError as exc:
            return str(exc)
        except Exception as exc:  # noqa: BLE001
            logger.exception("应用提案失败：%s", exc)
            return f"应用失败：{exc}"
        if meta.get("kind") == "patch":
            return (f"已应用提案 {pid}：{meta.get('plugin_name')}。"
                    f"改动前已备份，可用 /rollback {meta.get('plugin_name')} 还原。")
        return f"已应用提案 {pid}：{meta.get('plugin_name')}。已加载为生成插件。"

    @ctx.command("reject", description="放弃一个提案",
                 admin_only=True, usage="reject <提案ID>", timeout=30)
    async def reject_cmd(c):
        pid = (c.args[0] if c.args else "").strip()
        if not pid:
            return "用法：/reject <提案ID>"
        try:
            mind.reject(pid)
        except ValueError as exc:
            return str(exc)
        return f"已放弃提案 {pid}。"

    @ctx.command("rollback", aliases=["回滚"], description="把插件还原到最近一次备份",
                 admin_only=True, usage="rollback <插件名>", timeout=60)
    async def rollback_cmd(c):
        name = (c.raw_args or "").strip()
        if not name:
            return "用法：/rollback <插件名>"
        try:
            path = await mind.rollback(name)
        except ValueError as exc:
            return str(exc)
        except Exception as exc:  # noqa: BLE001
            logger.exception("回滚失败：%s", exc)
            return f"回滚失败：{exc}"
        return f"已还原「{name}」，备份：{path}"
