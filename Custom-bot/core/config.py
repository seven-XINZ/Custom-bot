"""配置加载与校验。

配置整体是一个嵌套 dict，额外提供 `get("kernel.log_level")` 这种点路径读取，
避免调用方到处写 `cfg["kernel"]["log_level"]` 还要自己兜底默认值。
"""

from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import yaml

DEFAULTS: Dict[str, Any] = {
    "kernel": {
        "log_level": "INFO",
        "admins": [],
        "version": "1.0.0",
        "command_prefixes": ["/", "!"],
        "max_concurrent": 16,
        "message_retention": 200,
        "plugin_timeout": 15,
        "shutdown_timeout": 10,
    },
    "webui": {
        "enabled": True,
        "host": "0.0.0.0",
        "port": 9090,
        "stats_interval": 5,
        "title": "Custom-bot 控制台",
        "auth": {"username": "", "password": ""},
    },
    "database": {"provider": "json", "path": "data/db"},
    "logging": {
        "level": "INFO",
        "dir": "data/logs",
        "file": "custom-bot.log",
        "max_bytes": 5 * 1024 * 1024,
        "backup_count": 5,
        "console": True,
    },
    "adapters": {},
    "handlers": {},
    "scheduled_tasks": {},
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """递归合并，override 覆盖 base；两边都是 dict 时继续下钻。"""
    out = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


class Config:
    """只读配置视图，带点路径读取与少量校验。"""

    def __init__(self, data: Dict[str, Any], path: Optional[Path] = None):
        self._data = data
        self.path = path

    # ------------------------------------------------------------------ 读取
    def get(self, dotted: str, default: Any = None) -> Any:
        node: Any = self._data
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node if node is not None else default

    def section(self, name: str) -> Dict[str, Any]:
        value = self._data.get(name)
        return value if isinstance(value, dict) else {}

    def require(self, dotted: str) -> Any:
        value = self.get(dotted)
        if value is None:
            raise ValueError(f"配置缺少必填项: {dotted}")
        return value

    @property
    def raw(self) -> Dict[str, Any]:
        return self._data

    def iter_adapters(self) -> Iterable[tuple[str, Dict[str, Any]]]:
        for adapter_id, item in self.section("adapters").items():
            if isinstance(item, dict):
                yield str(adapter_id), item

    def iter_handlers(self) -> Iterable[tuple[str, Dict[str, Any]]]:
        for plugin_id, item in self.section("handlers").items():
            if isinstance(item, dict):
                yield str(plugin_id), item

    # ------------------------------------------------------------------ 校验
    def validate(self) -> list[str]:
        """返回问题列表；空列表表示可以启动。"""
        problems: list[str] = []
        for adapter_id, item in self.iter_adapters():
            if not item.get("class"):
                problems.append(f"adapters.{adapter_id} 缺少 class")
            if not isinstance(item.get("config", {}), dict):
                problems.append(f"adapters.{adapter_id}.config 必须是字典")
        if not isinstance(self.get("kernel.admins", []), list):
            problems.append("kernel.admins 必须是列表")
        port = self.get("webui.port", 9090)
        if not isinstance(port, int) or not (0 < port < 65536):
            problems.append("webui.port 必须是 1-65535 的整数")
        kb = self.section("knowledge")
        if kb.get("enabled", True):
            providers = (kb.get("search", {}) or {}).get("providers", ["bing"])
            if not isinstance(providers, list) or not providers:
                problems.append("knowledge.search.providers 必须是非空列表")
            elif "searxng" in [str(p).lower() for p in providers] \
                    and not (kb.get("search", {}) or {}).get("searxng_url"):
                problems.append("启用 searxng 时必须填写 knowledge.search.searxng_url")
            coverage = (kb.get("offline", {}) or {}).get("min_coverage", 0.6)
            try:
                coverage = float(coverage)
            except (TypeError, ValueError):
                coverage = -1
            if not (0 <= coverage <= 1):
                problems.append("knowledge.offline.min_coverage 必须在 0-1 之间")
        return problems


def load_config(path: str | os.PathLike[str]) -> Config:
    """读取 YAML 并与默认值合并；文件不存在时抛 FileNotFoundError。"""
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise FileNotFoundError(f"配置文件不存在: {file_path}")
    with file_path.open("r", encoding="utf-8") as fp:
        loaded = yaml.safe_load(fp) or {}
    if not isinstance(loaded, dict):
        raise ValueError("配置文件顶层必须是映射（key: value）")
    merged = _deep_merge(DEFAULTS, loaded)
    return Config(merged, file_path)
