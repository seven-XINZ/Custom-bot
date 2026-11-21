"""示例定时任务：每 30 分钟记一次心跳。

配置里默认是关闭的，打开方式：

    scheduled_tasks:
      heartbeat:
        enabled: true
        name: "心跳"
        script_path: "example_task.py"
        schedule: { trigger: "interval", minutes: 30 }
        timeout_seconds: 60

脚本必须暴露 `run(kernel)`（同步或异步都行）。
"""

from __future__ import annotations

import logging
import time

logger = logging.getLogger("定时任务.心跳")


async def run(kernel) -> str:
    """记录一次心跳，并把计数写进数据库。"""
    count = await kernel.db.update(
        "runtime", "heartbeat_count",
        lambda old: int(old or 0) + 1,
        default=0,
    )
    await kernel.db.set("runtime", "last_heartbeat", {
        "at": time.time(),
        "count": count,
        "uptime": kernel.status()["kernel"]["uptime"],
    })
    logger.info("心跳 #%s，内核已运行 %s", count, kernel.status()["kernel"]["uptime"])
    return f"heartbeat #{count}"
