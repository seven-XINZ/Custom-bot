"""本地知识库 + 联网检索。

用途：没有接大模型（或模型不可用）时，机器人仍然能回答：

1. 先查本地知识库（手动录入、Markdown 文档索引、历史联网缓存）；
2. 本地没有明显命中时，按配置调用搜索引擎（默认 Bing，可配 SearXNG）；
3. 联网结果会带 TTL 缓存回知识库，下次同样的问题直接本地命中。

所有内容都落在 `kb_entries` 表里，字段包含标题、正文、标签、来源 URL、过期时间与命中次数。
"""

from __future__ import annotations

import asyncio
import hashlib
import html as html_lib
import ipaddress
import logging
import re
import socket
import time
import urllib.parse
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import aiohttp

logger = logging.getLogger("内核.知识库")

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def _as_list(value: Any) -> List[str]:
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    if not value:
        return []
    return [p.strip() for p in re.split(r"[，,;；\n]+", str(value)) if p.strip()]


def _strip_tags(value: str) -> str:
    value = re.sub(r"<script.*?</script>", " ", value, flags=re.S | re.I)
    value = re.sub(r"<style.*?</style>", " ", value, flags=re.S | re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html_lib.unescape(value)).strip()


def _html_to_text(html: str) -> str:
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<(br|p|div|li|h[1-6]|section|article|tr)[^>]*>", "\n", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    text = html_lib.unescape(html)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


_CJK = re.compile(r"[\u4e00-\u9fff]+")
_WORD = re.compile(r"[a-z0-9_]{2,}")


def _terms(text: str) -> List[str]:
    text = (text or "").lower()
    terms = set()
    for word in _WORD.findall(text):
        terms.add(word)
    for seq in _CJK.findall(text):
        if len(seq) <= 2:
            terms.add(seq)
        else:
            terms.add(seq[:12])
            for i in range(len(seq) - 1):
                terms.add(seq[i:i + 2])
    for token in re.split(r"[^\w\u4e00-\u9fff]+", text):
        if token and len(token) >= 2:
            terms.add(token)
    return [t for t in terms if t]


_QUESTION_WORDS = re.compile(
    r"(请问|帮我查|查一下|怎么|如何|为什么|是什么|什么|多少|哪里|哪个|谁|何时|能不能|可以|吗|呢|呀|啊|一下)"
)


def _core_query(text: str) -> str:
    """去掉疑问词，保留真正需要匹配的主题词。"""
    core = _QUESTION_WORDS.sub(" ", text or "")
    core = re.sub(r"\s+", " ", core).strip(" ，,。.!！?？")
    return core or (text or "").strip()


def _looks_like_question(text: str) -> bool:
    if not text:
        return False
    if "?" in text or "？" in text:
        return True
    markers = ("怎么", "如何", "为什么", "是什么", "多少", "哪里", "哪个", "谁",
               "何时", "能不能", "可以", "吗", "呢", "求助", "帮我查")
    return any(marker in text for marker in markers)


@dataclass
class WebResult:
    title: str
    url: str
    snippet: str
    provider: str = ""


@dataclass
class KBAnswer:
    text: str = ""
    sources: List[Dict[str, str]] = field(default_factory=list)
    local: bool = False
    cached: bool = False
    score: float = 0.0
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return bool(self.text)


class KnowledgeBase:
    def __init__(self, kernel):
        cfg = kernel.config
        self.kernel = kernel
        self.enabled: bool = bool(cfg.get("knowledge.enabled", True))
        self.table: str = str(cfg.get("knowledge.table", "kb_entries") or "kb_entries")
        self.max_entries: int = max(1, int(cfg.get("knowledge.max_entries", 5000)))
        self.max_entry_chars: int = int(cfg.get("knowledge.max_entry_chars", 4000))
        self.max_answer_chars: int = int(cfg.get("knowledge.max_answer_chars", 1200))
        self.docs_dir: Path = kernel._resolve(str(cfg.get("knowledge.docs_dir", "knowledge")))
        self.index_docs_on_start: bool = bool(cfg.get("knowledge.index_docs_on_start", True))

        self.providers: List[str] = _as_list(cfg.get("knowledge.search.providers", ["bing"]))
        self.searxng_url: str = str(cfg.get("knowledge.search.searxng_url", "") or "").rstrip("/")
        self.search_timeout: float = float(cfg.get("knowledge.search.timeout", 12))
        self.max_results: int = max(1, int(cfg.get("knowledge.search.max_results", 5)))
        self.cache_ttl: float = float(cfg.get("knowledge.web.cache_ttl_seconds", 86400))
        self.max_page_bytes: int = int(cfg.get("knowledge.web.max_page_bytes", 2 * 1024 * 1024))
        self.allow_private_urls: bool = bool(cfg.get("knowledge.web.allow_private_urls", False))

        self.auto_answer: bool = bool(cfg.get("knowledge.offline.auto_answer", True))
        self.auto_web: bool = bool(cfg.get("knowledge.offline.auto_web", True))
        self.min_score: float = float(cfg.get("knowledge.offline.min_score", 3.0))
        self.min_coverage: float = float(cfg.get("knowledge.offline.min_coverage", 0.6))
        self.cooldown: float = float(cfg.get("knowledge.offline.cooldown_seconds", 60))
        self.trigger_names: List[str] = (_as_list(cfg.get("knowledge.trigger_names", []))
                                         or list(kernel.mind.trigger_names))

        self._session: Optional[aiohttp.ClientSession] = None
        self._last_answer: Dict[str, float] = {}
        self._tasks: set[asyncio.Task] = set()
        self._count: int = 0

    # ------------------------------------------------------------------ 生命周期
    async def setup(self) -> None:
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        await self._refresh_count()
        if self.enabled and self.index_docs_on_start:
            try:
                await self.reindex_docs()
            except Exception as exc:  # noqa: BLE001
                logger.warning("启动时索引文档失败：%s", exc)
        logger.info("知识库就绪：%d 条，搜索引擎 %s", self._count, ", ".join(self.providers) or "未配置")

    async def close(self) -> None:
        for task in list(self._tasks):
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    @staticmethod
    def looks_like_question(text: str) -> bool:
        return _looks_like_question(text)

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "entries": self._count,
            "docs_dir": str(self.docs_dir),
            "providers": self.providers,
            "auto_answer": self.auto_answer,
            "auto_web": self.auto_web,
        }

    async def _refresh_count(self) -> None:
        try:
            self._count = len(await self.kernel.db.all(self.table))
        except Exception:  # noqa: BLE001
            self._count = 0

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.search_timeout),
                headers={"User-Agent": _UA},
            )
        return self._session

    # ------------------------------------------------------------------ 写入
    async def add(self, title: str, content: str, *, tags: Optional[List[str]] = None,
                  source: str = "manual", url: str = "", ttl: Optional[float] = None,
                  entry_id: str = "") -> Dict[str, Any]:
        title = re.sub(r"\s+", " ", (title or "").strip())[:120]
        content = (content or "").strip()
        if not content:
            raise ValueError("知识内容不能为空")
        if len(content) > self.max_entry_chars:
            content = content[: self.max_entry_chars]

        now = time.time()
        entries = await self.kernel.db.all(self.table)

        # 同一 URL 的网页内容默认做覆盖更新，避免重复查询堆积
        if url and not entry_id:
            for key, item in entries.items():
                if item.get("url") == url:
                    entry = dict(item)
                    entry.update({
                        "title": title or entry.get("title", ""),
                        "content": content,
                        "tags": list(set((entry.get("tags") or []) + list(tags or [])))[:12],
                        "updated_at": now,
                        "expires_at": now + ttl if ttl else None,
                        "source": source,
                    })
                    await self.kernel.db.set(self.table, key, entry)
                    await self._refresh_count()
                    return entry

        key = entry_id or f"kb-{uuid.uuid4().hex[:10]}"
        entry = {
            "id": key,
            "title": title or content[:40],
            "content": content,
            "tags": list(tags or [])[:12],
            "source": source,
            "url": url,
            "created_at": now,
            "updated_at": now,
            "expires_at": (now + ttl) if ttl else None,
            "hits": 0,
            "last_hit_at": None,
        }
        await self.kernel.db.set(self.table, key, entry)
        await self._prune()
        await self._refresh_count()
        return entry

    async def delete(self, entry_id: str) -> bool:
        entry_id = (entry_id or "").strip()
        ok = await self.kernel.db.delete(self.table, entry_id)
        await self._refresh_count()
        return ok

    async def _prune(self) -> None:
        entries = await self.kernel.db.all(self.table)
        if len(entries) <= self.max_entries:
            return
        now = time.time()

        def rank(item: Dict[str, Any]) -> tuple:
            expired = 1 if item.get("expires_at") and item["expires_at"] < now else 0
            is_doc = 1 if str(item.get("source", "")).startswith("doc:") else 0
            return (expired, is_doc, item.get("hits", 0), item.get("updated_at", 0))

        ordered = sorted(entries.items(), key=lambda kv: rank(kv[1]))
        for key, _ in ordered[: len(entries) - self.max_entries]:
            await self.kernel.db.delete(self.table, key)

    # ------------------------------------------------------------------ 检索
    async def search_local(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        entries = list((await self.kernel.db.all(self.table)).values())
        now = time.time()
        query = (query or "").strip()
        core = _core_query(query)
        qlower = core.lower()
        terms = _terms(core)
        if not qlower:
            return []

        scored: List[Dict[str, Any]] = []
        for item in entries:
            entry = dict(item)
            entry["expired"] = bool(entry.get("expires_at") and entry["expires_at"] < now)
            title = str(entry.get("title", "")).lower()
            content = str(entry.get("content", "")).lower()
            tag_text = " ".join(entry.get("tags") or []).lower()

            score = 0.0
            matched = 0
            if qlower:
                if qlower in title:
                    score += 6
                elif qlower in content:
                    score += 3
                for term in terms:
                    weight = 1.6 if len(term) >= 3 else 1.0
                    title_hits = title.count(term)
                    tag_hits = tag_text.count(term)
                    content_hits = content.count(term)
                    if title_hits:
                        score += weight * 3
                    if tag_hits:
                        score += weight * 2
                    if content_hits:
                        score += weight * min(content_hits, 3)
                    if title_hits or tag_hits or content_hits:
                        matched += 1
                if score <= 0:
                    continue

            # 新内容略加权；过期内容降权
            age = now - float(entry.get("updated_at", 0) or 0)
            score += max(0.0, 1.0 - age / (30 * 86400))
            if entry["expired"]:
                score *= 0.7
            entry["score"] = round(score, 2)
            entry["coverage"] = round(matched / len(terms), 2) if terms else 1.0
            scored.append(entry)

        scored.sort(key=lambda e: (e["score"], e.get("updated_at", 0)), reverse=True)
        result = scored[:limit]
        await self._mark_hits(result)
        return result

    async def _mark_hits(self, entries: List[Dict[str, Any]]) -> None:
        for entry in entries:
            key = entry.get("id")
            if not key:
                continue
            try:
                await self.kernel.db.update(
                    self.table, key,
                    lambda item: {**{k: v for k, v in item.items() if k not in ("score", "coverage", "expired")},
                                  "hits": int(item.get("hits", 0)) + 1,
                                  "last_hit_at": time.time()},
                    default={k: v for k, v in entry.items() if k not in ("score", "coverage", "expired")},
                )
            except Exception:  # noqa: BLE001
                pass

    # ------------------------------------------------------------------ 联网
    async def _safe_url(self, url: str) -> None:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("只允许 http/https 链接")
        if self.allow_private_urls:
            return
        host = parsed.hostname.lower()
        if host == "localhost" or host.endswith(".local"):
            raise ValueError("禁止访问本机/内网地址")
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        try:
            infos = await asyncio.get_running_loop().getaddrinfo(host, port, type=socket.SOCK_STREAM)
        except socket.gaierror as exc:
            raise ValueError(f"域名无法解析：{host}") from exc
        for info in infos:
            ip = ipaddress.ip_address(info[4][0])
            if getattr(ip, "ipv4_mapped", None):
                ip = ip.ipv4_mapped
            if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                    or ip.is_multicast or ip.is_unspecified):
                raise ValueError("禁止访问内网/保留地址")

    async def _read_limited(self, resp: aiohttp.ClientResponse) -> bytes:
        chunks = []
        total = 0
        async for chunk in resp.content.iter_chunked(65536):
            total += len(chunk)
            if total > self.max_page_bytes:
                raise ValueError(f"页面超过大小上限（{self.max_page_bytes} 字节）")
            chunks.append(chunk)
        return b"".join(chunks)

    async def fetch_url(self, url: str) -> Tuple[str, str]:
        """抓取网页，返回 (标题, 正文)。重定向逐跳校验，避免被引到内网。"""
        current = (url or "").strip()
        if not current:
            raise ValueError("链接为空")
        session = await self._ensure_session()
        raw = b""
        ctype = ""
        for hop in range(4):
            await self._safe_url(current)
            async with session.get(current, allow_redirects=False) as resp:
                if resp.status in (301, 302, 303, 307, 308):
                    location = resp.headers.get("Location")
                    if not location:
                        raise ValueError("重定向缺少 Location")
                    current = urllib.parse.urljoin(current, location)
                    if hop == 3:
                        raise ValueError("重定向次数过多")
                    continue
                if resp.status >= 400:
                    raise ValueError(f"抓取失败：HTTP {resp.status}")
                ctype = (resp.headers.get("Content-Type", "") or "").lower()
                if not any(t in ctype for t in ("text/html", "text/plain", "application/json", "text/markdown")):
                    raise ValueError(f"不支持的内容类型：{ctype or '未知'}")
                raw = await self._read_limited(resp)
                break
        else:
            raise ValueError("重定向次数过多")

        charset = None
        if raw:
            meta = re.search(rb'<meta[^>]+charset=["\']?([a-zA-Z0-9_-]+)', raw[:4096], re.I)
            if meta:
                charset = meta.group(1).decode("ascii", "ignore")
        try:
            text = raw.decode(charset or "utf-8", "replace")
        except LookupError:
            text = raw.decode("utf-8", "replace")
        if "html" in ctype:
            title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
            title = _strip_tags(title_match.group(1)) if title_match else ""
            body = _html_to_text(text)
        else:
            title = urllib.parse.urlparse(url).netloc
            body = text
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        if not title:
            title = urllib.parse.urlparse(url).netloc
        return title[:120], body[: self.max_entry_chars]

    async def import_url(self, url: str) -> Dict[str, Any]:
        title, body = await self.fetch_url(url)
        if len(body) < 30:
            raise ValueError("页面正文太短，可能被反爬拦截")
        return await self.add(title, body, tags=["网页导入"], source="web-import", url=url)

    async def web_search(self, query: str, limit: Optional[int] = None) -> Tuple[List[WebResult], List[str]]:
        query = (query or "").strip()[:200]
        limit = limit or self.max_results
        errors: List[str] = []
        if not query:
            return [], ["查询为空"]
        for provider in self.providers:
            func = getattr(self, f"_search_{provider.lower()}", None)
            if func is None:
                errors.append(f"{provider}: 未知的搜索引擎")
                continue
            try:
                results = await asyncio.wait_for(func(query, limit), timeout=self.search_timeout)
                if results:
                    return results[:limit], errors
                errors.append(f"{provider}: 没有结果")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{provider}: {exc}")
                logger.warning("搜索 %s 失败（%s）：%s", provider, query, exc)
        return [], errors

    async def _search_bing(self, query: str, limit: int) -> List[WebResult]:
        session = await self._ensure_session()
        params = {"q": query, "count": str(limit), "setlang": "zh-CN"}
        async with session.get("https://cn.bing.com/search", params=params,
                               allow_redirects=True, max_redirects=3) as resp:
            if resp.status >= 400:
                raise ValueError(f"HTTP {resp.status}")
            html = (await self._read_limited(resp)).decode("utf-8", "replace")
        results = []
        for block in re.findall(r'<li class="b_algo".*?</li>', html, re.S):
            match = re.search(r'<h2[^>]*>.*?<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block, re.S)
            if not match:
                continue
            url = html_lib.unescape(match.group(1))
            if not url.startswith("http"):
                continue
            title = _strip_tags(match.group(2))
            snippet = ""
            for pattern in (r'<p[^>]*>(.*?)</p>', r'<div[^>]*class="b_caption"[^>]*>(.*?)</div>'):
                sm = re.search(pattern, block, re.S)
                if sm:
                    snippet = _strip_tags(sm.group(1))
                    if snippet:
                        break
            results.append(WebResult(title=title or url, url=url, snippet=snippet, provider="bing"))
        return results

    async def _search_duckduckgo(self, query: str, limit: int) -> List[WebResult]:
        session = await self._ensure_session()
        async with session.get("https://html.duckduckgo.com/html/", params={"q": query},
                               allow_redirects=True, max_redirects=3) as resp:
            if resp.status >= 400:
                raise ValueError(f"HTTP {resp.status}")
            html = (await self._read_limited(resp)).decode("utf-8", "replace")
        results = []
        anchors = re.findall(r'<a[^>]*class="result__a"[^>]*>.*?</a>', html, re.S)
        snippets = re.findall(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', html, re.S)
        for i, anchor in enumerate(anchors[:limit]):
            href_match = re.search(r'href="([^"]+)"', anchor)
            if not href_match:
                continue
            url = html_lib.unescape(href_match.group(1))
            parsed = urllib.parse.urlparse(url)
            if "duckduckgo.com" in parsed.netloc:
                query_params = urllib.parse.parse_qs(parsed.query)
                if "uddg" in query_params:
                    url = urllib.parse.unquote(query_params["uddg"][0])
            title = _strip_tags(anchor)
            snippet = _strip_tags(snippets[i]) if i < len(snippets) else ""
            results.append(WebResult(title=title or url, url=url, snippet=snippet, provider="duckduckgo"))
        return results

    async def _search_searxng(self, query: str, limit: int) -> List[WebResult]:
        if not self.searxng_url:
            raise ValueError("searxng_url 未配置")
        session = await self._ensure_session()
        endpoint = self.searxng_url if self.searxng_url.endswith("/search") else f"{self.searxng_url}/search"
        async with session.get(endpoint, params={"q": query, "format": "json"}) as resp:
            if resp.status >= 400:
                raise ValueError(f"HTTP {resp.status}")
            data = await resp.json(content_type=None)
        results = []
        for item in (data.get("results") or [])[:limit]:
            url = str(item.get("url") or "")
            if not url:
                continue
            results.append(WebResult(
                title=str(item.get("title") or url),
                url=url,
                snippet=str(item.get("content") or "")[:500],
                provider="searxng",
            ))
        return results

    # ------------------------------------------------------------------ 问答
    async def answer(self, query: str, *, allow_web: bool = True) -> KBAnswer:
        if not self.enabled:
            return KBAnswer(errors=["知识库未启用"])
        query = (query or "").strip()
        if not query:
            return KBAnswer(errors=["查询为空"])

        local = await self.search_local(query, limit=5)
        fresh = [e for e in local if not e.get("expired")]
        best = fresh[0] if fresh else (local[0] if local else None)
        if (best and best.get("score", 0) >= self.min_score
                and best.get("coverage", 0) >= self.min_coverage):
            entry = best
            text = f"【{entry.get('title')}】\n{entry.get('content', '')[: self.max_answer_chars]}"
            if entry.get("expired"):
                text += "\n（缓存可能已过期）"
            return KBAnswer(
                text=text,
                sources=[{"title": entry.get("title", ""), "url": entry.get("url", ""),
                          "provider": "local"}],
                local=True, cached=bool(entry.get("expired")), score=entry.get("score", 0),
            )

        errors: List[str] = []
        results: List[WebResult] = []
        if allow_web:
            results, errors = await self.web_search(query)
            if results:
                for item in results[:3]:
                    if len(item.snippet) < 20:
                        continue
                    try:
                        await self.add(item.title, item.snippet, tags=[query[:40]],
                                       source=f"web:{item.provider}", url=item.url,
                                       ttl=self.cache_ttl)
                    except Exception:  # noqa: BLE001
                        pass
                lines = []
                for i, item in enumerate(results[:3], 1):
                    lines.append(f"{i}. {item.title}\n{item.snippet[:400]}")
                return KBAnswer(
                    text="\n\n".join(lines),
                    sources=[{"title": r.title, "url": r.url, "provider": r.provider}
                             for r in results[:3]],
                    local=False, cached=False, errors=errors,
                )

        if best and best.get("expired") and best.get("score", 0) > 0:
            entry = best
            return KBAnswer(
                text=f"【{entry.get('title')}】\n{entry.get('content', '')[: self.max_answer_chars]}\n（缓存可能已过期）",
                sources=[{"title": entry.get("title", ""), "url": entry.get("url", ""),
                          "provider": "local"}],
                local=True, cached=True, score=entry.get("score", 0), errors=errors,
            )
        return KBAnswer(errors=errors or ["没有找到相关内容"])

    async def context(self, query: str, limit: int = 3, max_chars: int = 600) -> str:
        """给大模型用的知识上下文。"""
        if not self.enabled:
            return ""
        hits = [e for e in await self.search_local(query, limit=limit) if not e.get("expired")]
        if not hits:
            return ""
        lines = []
        for entry in hits:
            lines.append(f"[{entry.get('title')}] {entry.get('content', '')[:max_chars]}")
        return "\n\n".join(lines)

    # ------------------------------------------------------------------ 文档索引
    def _chunk_text(self, text: str, size: int = 1200) -> List[str]:
        chunks: List[str] = []
        current = ""
        for block in re.split(r"\n\s*\n", text):
            block = block.strip()
            if not block:
                continue
            if current and len(current) + len(block) + 2 > size:
                chunks.append(current)
                current = block
            else:
                current = (current + "\n\n" + block).strip() if current else block
        if current:
            chunks.append(current)
        return chunks

    async def reindex_docs(self) -> int:
        docs = await self.kernel.db.all(self.table)
        for key, item in docs.items():
            if str(item.get("source", "")).startswith("doc:"):
                await self.kernel.db.delete(self.table, key)

        files = []
        for suffix in ("*.md", "*.markdown", "*.txt"):
            files.extend(sorted(self.docs_dir.rglob(suffix)))
        count = 0
        for path in files[:200]:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if len(text.strip()) < 20:
                continue
            rel = str(path.relative_to(self.docs_dir))
            for index, chunk in enumerate(self._chunk_text(text)):
                heading = ""
                for line in chunk.splitlines():
                    if line.strip().startswith("#"):
                        heading = line.strip().lstrip("#").strip()
                        break
                title = heading or f"{path.stem} 第{index + 1}段"
                doc_id = "doc-" + hashlib.sha1(f"{rel}|{index}".encode("utf-8")).hexdigest()[:12]
                await self.add(title, chunk, tags=["文档", path.stem],
                               source=f"doc:{rel}", entry_id=doc_id)
                count += 1
        await self._refresh_count()
        logger.info("已索引 %d 个文档片段（%d 个文件）", count, len(files))
        return count

    # ------------------------------------------------------------------ 离线自动答
    def should_auto_answer(self, message) -> bool:
        if not self.enabled or not self.auto_answer:
            return False
        if self.kernel.mind.ready:  # 有模型时交给心智
            return False
        if message.is_event or message.msg_type not in ("text", ""):
            return False
        text = (message.text_content or "").strip()
        if len(text) < 4:
            return False
        if any(text.startswith(p) for p in self.kernel.handlers.prefixes if p):
            return False
        if self.kernel.handlers.parse(text):
            return False
        if message.is_group:
            mentioned = bool(message.metadata.get("mentioned_bot"))
            named = any(name and name in text[:40] for name in self.trigger_names)
            if not (mentioned or named):
                return False
        user = message.user_id or "?"
        if time.time() - self._last_answer.get(user, 0) < self.cooldown:
            return False
        return True

    def spawn_auto_answer(self, message) -> bool:
        if not self.should_auto_answer(message):
            return False
        self._last_answer[message.user_id or "?"] = time.time()
        task = asyncio.create_task(self._auto_answer(message), name="kb_auto_answer")
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return True

    async def _auto_answer(self, message) -> None:
        text = (message.text_content or "").strip()
        allow_web = self.auto_web and _looks_like_question(text)
        try:
            answer = await self.answer(text, allow_web=allow_web)
        except Exception as exc:  # noqa: BLE001
            logger.exception("知识库自动回答失败：%s", exc)
            return
        if not answer.ok:
            return
        reply = ("〔知识库〕" if answer.local else "〔联网〕") + answer.text
        sources = [s for s in answer.sources if s.get("url")]
        if sources:
            reply += "\n来源：" + "；".join(s["url"] for s in sources[:3])
        await self.kernel.reply(message, reply[:1800])
