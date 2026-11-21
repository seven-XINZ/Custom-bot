"""知识库插件：本地检索、联网兜底、文档导入与维护命令。"""

from __future__ import annotations

NAME = "知识库"
VERSION = "1.0.0"
DESCRIPTION = "本地知识库：无模型时自动作答，支持联网搜索与网页导入"
AUTHOR = "Xinz / AI 助手"


def _format_answer(answer, limit: int = 3) -> str:
    text = answer.text.strip()
    sources = [s for s in answer.sources if s.get("url")]
    if sources:
        lines = []
        for item in sources[:limit]:
            title = item.get("title") or item["url"]
            lines.append(f"- {title}：{item['url']}")
        text += "\n\n来源：\n" + "\n".join(lines)
    if answer.cached:
        text += "\n（来自本地缓存，可能已过期）"
    return text


async def setup(ctx):
    kernel = ctx.kernel
    kb = kernel.knowledge
    logger = ctx.logger

    @ctx.on_message
    async def offline_answer(message):
        # 只在没有模型时兜底；有模型时让 AI 心智优先
        if kernel.mind.ready:
            return None
        kb.spawn_auto_answer(message)
        return None

    @ctx.command("ask", aliases=["问知识库", "qa"], description="问本地知识库（没有模型时也能用）",
                 usage="ask 问题", timeout=60)
    async def ask(c):
        question = (c.raw_args or "").strip()
        if not question:
            return "用法：/ask 你的问题"
        answer = await kb.answer(question)
        if answer.ok:
            return _format_answer(answer)
        if kernel.mind.ready:
            try:
                return await kernel.mind.chat(c.message, question)
            except Exception as exc:  # noqa: BLE001
                logger.warning("知识库未命中，转模型失败：%s", exc)
        detail = "；".join(answer.errors[:3]) if answer.errors else "没有找到相关内容"
        return (f"本地知识库没有可靠答案，联网也没查到（{detail}）。\n"
                "可以先用 /kb add 标题 | 内容 补充，或 /kb import 网页链接。")

    @ctx.command("kb", aliases=["知识库"], description="知识库管理：搜索/添加/导入/统计",
                 usage="kb [stats|search|add|import|delete|reindex|web]", timeout=90)
    async def kb_cmd(c):
        raw = (c.raw_args or "").strip()
        if not raw:
            return await _stats(c)
        action, _, rest = raw.partition(" ")
        action = action.lower()
        rest = rest.strip()

        if action in ("stats", "状态", "统计"):
            return await _stats(c)
        if action in ("search", "搜索", "查"):
            return await _search(c, rest)
        if action in ("add", "添加"):
            return await _add(c, rest)
        if action in ("import", "导入"):
            return await _import(c, rest)
        if action in ("delete", "del", "删除"):
            return await _delete(c, rest)
        if action in ("reindex", "重建索引", "索引"):
            return await _reindex(c)
        if action in ("web", "联网"):
            return await _web(c, rest)
        return ("用法：/kb stats、/kb search 关键词、/kb add 标题 | 内容、"
                "/kb import 网页链接、/kb delete 条目ID、/kb reindex、/kb web 关键词")

    async def _stats(c):
        entries = await c.db.all(kb.table)
        docs = sum(1 for e in entries.values() if str(e.get("source", "")).startswith("doc:"))
        web = sum(1 for e in entries.values() if str(e.get("source", "")).startswith("web"))
        manual = len(entries) - docs - web
        return (f"知识库：{len(entries)} 条（文档 {docs} / 网页 {web} / 手动 {manual}）\n"
                f"文档目录：{kb.docs_dir}\n"
                f"联网引擎：{', '.join(kb.providers) or '未配置'}\n"
                f"离线自动回答：{'开' if kb.auto_answer else '关'}；自动联网：{'开' if kb.auto_web else '关'}")

    async def _search(c, query):
        if not query:
            return "用法：/kb search 关键词"
        hits = await kb.search_local(query, limit=8)
        if not hits:
            return "本地没有命中；可以用 /kb web 关键词 先联网看看，或 /kb import 链接入库。"
        lines = [f"找到 {len(hits)} 条："]
        for i, item in enumerate(hits, 1):
            content = str(item.get("content", "")).replace("\n", " ")[:120]
            lines.append(f"{i}. [{item.get('score')}] {item.get('title')}（{item.get('id')}）\n   {content}")
        return "\n".join(lines)

    async def _add(c, rest):
        if not c.is_admin:
            return "添加知识需要管理员权限。"
        if not rest:
            return "用法：/kb add 标题 | 内容"
        title, sep, content = rest.partition("|")
        if not sep:
            title, content = "", rest
        try:
            entry = await kb.add(title.strip() or content.strip()[:40], content.strip(),
                                 tags=["手动"], source="manual")
        except Exception as exc:  # noqa: BLE001
            return f"添加失败：{exc}"
        return f"已添加：{entry['title']}（{entry['id']}，{len(entry['content'])} 字符）"

    async def _import(c, rest):
        if not c.is_admin:
            return "导入网页需要管理员权限。"
        if not rest.startswith(("http://", "https://")):
            return "用法：/kb import https://example.com/page"
        try:
            entry = await kb.import_url(rest)
        except Exception as exc:  # noqa: BLE001
            return f"导入失败：{exc}"
        return f"已导入：{entry['title']}（{entry['id']}，{len(entry['content'])} 字符）"

    async def _delete(c, rest):
        if not c.is_admin:
            return "删除知识需要管理员权限。"
        if not rest:
            return "用法：/kb delete 条目ID（ID 可先 /kb search 查看）"
        if await kb.delete(rest):
            return f"已删除 {rest}。"
        return f"没有找到条目 {rest}。"

    async def _reindex(c):
        if not c.is_admin:
            return "重建索引需要管理员权限。"
        count = await kb.reindex_docs()
        return f"已重建文档索引：{count} 个片段，目录 {kb.docs_dir}。"

    async def _web(c, query):
        if not c.is_admin:
            return "主动联网搜索需要管理员权限。"
        if not query:
            return "用法：/kb web 关键词"
        results, errors = await kb.web_search(query)
        if not results:
            return "联网没有结果。" + ("（" + "；".join(errors[:3]) + "）" if errors else "")
        lines = [f"联网结果 {len(results)} 条："]
        for i, item in enumerate(results[:5], 1):
            lines.append(f"{i}. {item.title}\n   {item.url}\n   {item.snippet[:160]}")
        return "\n".join(lines)
