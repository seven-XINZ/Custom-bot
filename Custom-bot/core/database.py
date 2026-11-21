"""轻量 JSON 数据库。

原配置里的 `provider: tinydb` 保留兼容，但实现不依赖 TinyDB：
每个表一个 JSON 文件，读进内存后加 asyncio 锁写入，落盘用临时文件 + rename。
机器人这种量级（配置、用户画像、消息流水）完全够用，也方便直接看文件排障。
"""

from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .utils import atomic_write


class JsonDatabase:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        self._dirty: Dict[str, bool] = {}

    # ------------------------------------------------------------------ 内部
    def _lock(self, table: str) -> asyncio.Lock:
        if table not in self._locks:
            self._locks[table] = asyncio.Lock()
        return self._locks[table]

    def _path(self, table: str) -> Path:
        safe = "".join(ch for ch in table if ch.isalnum() or ch in "-_")
        if not safe:
            raise ValueError(f"非法表名: {table!r}")
        return self.base_dir / f"{safe}.json"

    def _load(self, table: str) -> Dict[str, Any]:
        if table in self._cache:
            return self._cache[table]
        path = self._path(table)
        data: Dict[str, Any] = {}
        if path.is_file():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                data = payload.get("data", payload) if isinstance(payload, dict) else {}
            except (json.JSONDecodeError, OSError):
                data = {}
        self._cache[table] = data
        return data

    def _flush(self, table: str) -> None:
        data = self._cache.get(table, {})
        atomic_write(
            self._path(table),
            json.dumps({"table": table, "updated_at": time.time(), "data": data},
                       ensure_ascii=False, indent=2),
        )
        self._dirty[table] = False

    # ------------------------------------------------------------------ 读写
    async def get(self, table: str, key: str, default: Any = None) -> Any:
        async with self._lock(table):
            return self._load(table).get(str(key), default)

    async def set(self, table: str, key: str, value: Any) -> None:
        async with self._lock(table):
            self._load(table)[str(key)] = value
            self._flush(table)

    async def delete(self, table: str, key: str) -> bool:
        async with self._lock(table):
            data = self._load(table)
            if str(key) not in data:
                return False
            del data[str(key)]
            self._flush(table)
            return True

    async def all(self, table: str) -> Dict[str, Any]:
        async with self._lock(table):
            return dict(self._load(table))

    async def update(self, table: str, key: str, updater: Callable[[Any], Any],
                     default: Any = None) -> Any:
        """读改写一次完成，避免并发覆盖。"""
        async with self._lock(table):
            data = self._load(table)
            current = data.get(str(key), default)
            value = updater(current)
            data[str(key)] = value
            self._flush(table)
            return value

    async def append(self, table: str, item: Any, key: str = "items",
                     limit: int = 200) -> List[Any]:
        """追加型表：消息流水、日志摘要这种只增不改的数据。"""
        async with self._lock(table):
            data = self._load(table)
            items = data.get(key)
            if not isinstance(items, list):
                items = []
            items.append(item)
            if limit > 0 and len(items) > limit:
                items = items[-limit:]
            data[key] = items
            self._flush(table)
            return items

    async def items(self, table: str, key: str = "items") -> List[Any]:
        async with self._lock(table):
            value = self._load(table).get(key)
            return list(value) if isinstance(value, list) else []

    async def close(self) -> None:
        """退出前把脏表刷一遍。"""
        for table, dirty in list(self._dirty.items()):
            if dirty:
                async with self._lock(table):
                    self._flush(table)
