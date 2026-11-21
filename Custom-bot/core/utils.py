"""日志、时间、文本与文件小工具。

这里只放无状态函数，任何模块都可以直接 import，不产生循环依赖。
"""

from __future__ import annotations

import logging
import logging.handlers
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    level: str = "INFO",
    log_dir: Optional[str] = None,
    file_name: str = "custom-bot.log",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
    console: bool = True,
) -> logging.Logger:
    """初始化根日志：控制台 + 按大小滚动的文件。

    重复调用是安全的——会先清空已有 handler，避免热重载时日志翻倍。
    """
    root = logging.getLogger()
    root.setLevel(getattr(logging, str(level).upper(), logging.INFO))
    for handler in list(root.handlers):
        root.removeHandler(handler)
        try:
            handler.close()
        except Exception:  # noqa: BLE001 - 关闭失败不影响后续
            pass

    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    if console:
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        root.addHandler(stream)

    if log_dir:
        directory = Path(log_dir)
        directory.mkdir(parents=True, exist_ok=True)
        rotating = logging.handlers.RotatingFileHandler(
            directory / file_name,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        rotating.setFormatter(formatter)
        root.addHandler(rotating)

    # aiohttp / websockets 的访问日志太吵，压到 WARNING
    for noisy in ("aiohttp.access", "websockets.server", "websockets.protocol"):
        logging.getLogger(noisy).setLevel(max(logging.WARNING, root.level))
    return root


def parse_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on", "y"}


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def now() -> float:
    return time.time()


def fmt_time(ts: Optional[float] = None) -> str:
    return datetime.fromtimestamp(ts or time.time()).strftime(DATE_FORMAT)


def human_duration(seconds: float) -> str:
    """把秒数写成 3天2小时 / 5分12秒 这种人读的形式。"""
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds}秒"
    if seconds < 3600:
        return f"{seconds // 60}分{seconds % 60}秒"
    if seconds < 86400:
        return f"{seconds // 3600}小时{(seconds % 3600) // 60}分"
    return f"{seconds // 86400}天{(seconds % 86400) // 3600}小时"


def truncate(text: Any, limit: int = 80) -> str:
    value = str(text).replace("\r", " ").replace("\n", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 1] + "…"


_CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def clean_text(text: Any) -> str:
    """去掉不可见控制字符，保留换行与制表符。"""
    return _CTRL_RE.sub("", str(text)).strip()


def atomic_write(path: str | os.PathLike[str], content: str) -> None:
    """先写临时文件再 rename，避免进程被杀时留下半截文件。"""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, target)


def mask_secret(value: Optional[str], keep: int = 4) -> str:
    """密钥脱敏：只保留首尾各 keep 位。"""
    if not value:
        return ""
    text = str(value)
    if len(text) <= keep * 2:
        return "*" * len(text)
    return f"{text[:keep]}…{text[-keep:]}"
