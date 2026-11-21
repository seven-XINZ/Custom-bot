"""长期记忆：事实、聊天片段与检索。

存储复用内核的 JSON 数据库，每个表一个文件：

- `memory_facts`：稳定事实（偏好、身份、约定），键含归属人
- `memory_episodes`：最近的对话片段，用于反思与上下文
- 通过 `MemoryStore.render()` 生成可直接塞进系统提示的摘要
"""

from __future__ import annotations

import re
import time
import uuid
from typing import Any, Dict, List, Optional

_FACT_TABLE = "memory_facts"
_EPISODE_TABLE = "memory_episodes"


class MemoryStore:
    def __init__(self, db, logger=None, max_facts: int = 2000, max_episodes: int = 500):
        self.db = db
        self.logger = logger
        self.max_facts = max_facts
        self.max_episodes = max_episodes

    # ------------------------------------------------------------------ 事实
    async def remember(self, key: str, value: str, *, owner: str = "",
                       tags: Optional[List[str]] = None, source: str = "",
                       confidence: float = 1.0) -> Dict[str, Any]:
        key = (key or "").strip()[:80]
        value = (value or "").strip()[:500]
        if not key or not value:
            raise ValueError("记忆的 key 与 value 都不能为空")
        storage_key = f"{owner}:{key}" if owner else key
        facts = await self.db.all(_FACT_TABLE)
        existing = facts.get(storage_key) or {}
        record = {
            "key": storage_key,
            "label": key,
            "owner": owner,
            "value": value,
            "tags": list(tags or []),
            "source": source or "manual",
            "confidence": max(0.0, min(1.0, float(confidence))),
            "created_at": existing.get("created_at") or time.time(),
            "updated_at": time.time(),
        }
        await self.db.set(_FACT_TABLE, storage_key, record)
        await self._prune_facts()
        return record

    async def forget(self, key: str, owner: str = "") -> bool:
        storage_key = f"{owner}:{key}" if owner else key
        return await self.db.delete(_FACT_TABLE, storage_key)

    async def get(self, key: str, owner: str = "") -> Optional[Dict[str, Any]]:
        storage_key = f"{owner}:{key}" if owner else key
        return await self.db.get(_FACT_TABLE, storage_key)

    async def all_facts(self) -> Dict[str, Any]:
        return await self.db.all(_FACT_TABLE)

    async def recall(self, query: str, *, owner: str = "", limit: int = 6) -> List[Dict[str, Any]]:
        facts = list((await self.all_facts()).values())
        if owner:
            facts = [f for f in facts if f.get("owner") in ("", owner)]
        query = (query or "").strip().lower()
        if not query:
            facts.sort(key=lambda f: f.get("updated_at", 0), reverse=True)
            return facts[:limit]

        tokens = [t for t in re.split(r"[\s,，。;；:：/|]+", query) if t]
        if not tokens:
            tokens = [query]

        scored = []
        for fact in facts:
            haystack = " ".join([
                str(fact.get("label", "")), str(fact.get("value", "")),
                " ".join(fact.get("tags", []) or []),
            ]).lower()
            score = 0.0
            if query in haystack:
                score += 6
            for token in tokens:
                if len(token) >= 2 and token in haystack:
                    score += 3
                elif len(token) == 1 and token in haystack:
                    score += 1
            if score:
                # 越新越靠前，但只做很小的加成，避免压过匹配度
                score += min(1.0, max(0.0, (fact.get("updated_at", 0) or 0) - 1_600_000_000) / 1e10)
                scored.append((score, fact))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [fact for _, fact in scored[:limit]]

    async def _prune_facts(self) -> None:
        facts = await self.db.all(_FACT_TABLE)
        if len(facts) <= self.max_facts:
            return
        ordered = sorted(facts.items(), key=lambda kv: kv[1].get("updated_at", 0))
        for key, _ in ordered[: len(facts) - self.max_facts]:
            await self.db.delete(_FACT_TABLE, key)

    # ------------------------------------------------------------------ 片段
    async def add_episode(self, user_id: str, user_text: str, assistant_text: str,
                          *, session: str = "", user_name: str = "") -> None:
        key = f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:6]}"
        await self.db.set(_EPISODE_TABLE, key, {
            "user_id": user_id,
            "user_name": user_name,
            "session": session,
            "user_text": (user_text or "")[:600],
            "assistant_text": (assistant_text or "")[:600],
            "created_at": time.time(),
        })
        await self._prune_episodes()

    async def recent_episodes(self, limit: int = 10) -> List[Dict[str, Any]]:
        data = await self.db.all(_EPISODE_TABLE)
        ordered = sorted(data.values(), key=lambda e: e.get("created_at", 0), reverse=True)
        return ordered[:limit]

    async def _prune_episodes(self) -> None:
        data = await self.db.all(_EPISODE_TABLE)
        if len(data) <= self.max_episodes:
            return
        ordered = sorted(data.items(), key=lambda kv: kv[1].get("created_at", 0))
        for key, _ in ordered[: len(data) - self.max_episodes]:
            await self.db.delete(_EPISODE_TABLE, key)

    # ------------------------------------------------------------------ 渲染
    async def render(self, query: str = "", *, owner: str = "", limit: int = 8) -> str:
        facts = await self.recall(query, owner=owner, limit=limit) if query else \
            await self.recall("", owner=owner, limit=limit)
        if not facts:
            return ""
        lines = []
        for fact in facts:
            label = fact.get("label") or fact.get("key", "")
            lines.append(f"- {label}：{fact.get('value', '')}")
        return "\n".join(lines)

    async def counts(self) -> Dict[str, int]:
        return {
            "facts": len(await self.db.all(_FACT_TABLE)),
            "episodes": len(await self.db.all(_EPISODE_TABLE)),
        }
