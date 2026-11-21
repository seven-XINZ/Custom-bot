"""定时任务调度。

配置形如：

    scheduled_tasks:
      daily_report:
        enabled: true
        name: "每日报告"
        script_path: "daily_report.py"
        schedule: { trigger: "cron", hour: 8, minute: 0 }
        timeout_seconds: 600

也支持 interval：

    schedule: { trigger: "interval", minutes: 30 }

脚本放在 `scripts/` 下，暴露 `async def run(kernel)`（或同步 `def run(kernel)`）。
"""

from __future__ import annotations

import asyncio
import importlib.util
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from .utils import fmt_time, human_duration

logger = logging.getLogger("内核.调度")


# ---------------------------------------------------------------------- cron
class CronError(ValueError):
    pass


def _parse_field(expr: str, low: int, high: int) -> set[int]:
    """解析 cron 的单段：*、*/n、a-b、a,b、a-b/n。"""
    expr = str(expr).strip()
    if not expr or expr == "*":
        return set(range(low, high + 1))

    values: set[int] = set()
    for part in expr.split(","):
        part = part.strip()
        step = 1
        if "/" in part:
            part, step_raw = part.split("/", 1)
            try:
                step = int(step_raw)
            except ValueError as exc:
                raise CronError(f"步长非法: {expr}") from exc
            if step <= 0:
                raise CronError(f"步长必须为正: {expr}")
        if part in ("*", ""):
            start, end = low, high
        elif "-" in part:
            a, b = part.split("-", 1)
            try:
                start, end = int(a), int(b)
            except ValueError as exc:
                raise CronError(f"范围非法: {expr}") from exc
        else:
            try:
                start = end = int(part)
            except ValueError as exc:
                raise CronError(f"取值非法: {expr}") from exc
        if start < low or end > high or start > end:
            raise CronError(f"超出范围 {low}-{high}: {expr}")
        values.update(range(start, end + 1, step))
    return values


class CronExpression:
    """标准五段 cron（分 时 日 月 周），周字段 0/7 都表示周日。"""

    def __init__(self, minute="*", hour="*", day="*", month="*", weekday="*"):
        # 支持 CronExpression("*/5 * * * *") 这种整串写法
        if isinstance(minute, str) and len(minute.split()) >= 5 and all(
                x == "*" for x in (hour, day, month, weekday)):
            minute, hour, day, month, weekday = minute.split()[:5]
        self.minute = _parse_field(minute, 0, 59)
        self.hour = _parse_field(hour, 0, 23)
        self.day = _parse_field(day, 1, 31)
        self.month = _parse_field(month, 1, 12)
        raw_weekday = _parse_field(weekday, 0, 7)
        self.weekday = {0 if v == 7 else v for v in raw_weekday}
        self._dom_star = str(day).strip() in ("*", "")
        self._dow_star = str(weekday).strip() in ("*", "")

    def matches(self, dt: datetime) -> bool:
        cron_weekday = (dt.weekday() + 1) % 7  # Python 周一=0 → cron 周日=0
        if dt.minute not in self.minute or dt.hour not in self.hour:
            return False
        if dt.month not in self.month:
            return False
        # 日与周同时受限时取 OR，符合 Vixie cron 习惯
        dom_ok = dt.day in self.day
        dow_ok = cron_weekday in self.weekday
        if not self._dom_star and not self._dow_star:
            return dom_ok or dow_ok
        return dom_ok and dow_ok

    def next_after(self, start: datetime) -> datetime:
        candidate = (start + timedelta(minutes=1)).replace(second=0, microsecond=0)
        limit = candidate + timedelta(days=1500)  # 覆盖闰年 2/29 这类稀疏表达式
        while candidate <= limit:
            if self.matches(candidate):
                return candidate
            candidate += timedelta(minutes=1)
        raise CronError("约 4 年内找不到下一次触发时间，请检查 cron 表达式")


# ---------------------------------------------------------------------- 任务
@dataclass
class ScheduledTask:
    task_id: str
    name: str
    script_path: str
    schedule: Dict[str, Any]
    timeout: float = 600
    enabled: bool = True
    # 运行时状态
    runs: int = 0
    failures: int = 0
    last_run_at: Optional[float] = None
    last_duration: float = 0.0
    last_error: str = ""
    last_result: str = ""
    next_run_at: Optional[float] = None

    @property
    def trigger(self) -> str:
        return str(self.schedule.get("trigger", "interval")).lower()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.task_id,
            "name": self.name,
            "script": self.script_path,
            "trigger": self.trigger,
            "schedule": self.schedule,
            "enabled": self.enabled,
            "runs": self.runs,
            "failures": self.failures,
            "last_run_at": fmt_time(self.last_run_at) if self.last_run_at else None,
            "last_duration": round(self.last_duration, 2),
            "last_error": self.last_error,
            "last_result": self.last_result,
            "next_run_at": fmt_time(self.next_run_at) if self.next_run_at else None,
        }


class Scheduler:
    def __init__(self, kernel, scripts_dir: Path):
        self.kernel = kernel
        self.scripts_dir = Path(scripts_dir)
        self.tasks: Dict[str, ScheduledTask] = {}
        self._runner: Optional[asyncio.Task] = None
        self._stop = asyncio.Event()
        self._running: set[str] = set()

    # ------------------------------------------------------------------ 装载
    def load(self) -> None:
        cfg = self.kernel.config.get("scheduled_tasks", {}) or {}
        for task_id, item in cfg.items():
            if not isinstance(item, dict):
                continue
            schedule = item.get("schedule", {}) or {}
            task = ScheduledTask(
                task_id=str(task_id),
                name=str(item.get("name", task_id)),
                script_path=str(item.get("script_path", "")),
                schedule=dict(schedule),
                timeout=float(item.get("timeout_seconds", 600)),
                enabled=bool(item.get("enabled", False)),
            )
            if not task.script_path:
                logger.warning("定时任务 %s 缺少 script_path，已跳过", task_id)
                continue
            self.tasks[task.task_id] = task
            self._schedule_next(task, initial=True)
        logger.info("已装载 %d 个定时任务（启用 %d 个）", len(self.tasks),
                    sum(1 for t in self.tasks.values() if t.enabled))

    def _interval_seconds(self, schedule: Dict[str, Any]) -> float:
        for unit, factor in (("seconds", 1), ("minutes", 60), ("hours", 3600), ("days", 86400)):
            if unit in schedule:
                try:
                    return max(1.0, float(schedule[unit]) * factor)
                except (TypeError, ValueError):
                    break
        return 3600.0

    def _cron(self, schedule: Dict[str, Any]) -> CronExpression:
        expr = schedule.get("cron") or schedule.get("expression")
        if isinstance(expr, str) and len(expr.split()) >= 5:
            return CronExpression(expr)
        return CronExpression(
            schedule.get("minute", "*"),
            schedule.get("hour", "*"),
            schedule.get("day", "*"),
            schedule.get("month", "*"),
            schedule.get("weekday", schedule.get("week", "*")),
        )

    def _schedule_next(self, task: ScheduledTask, initial: bool = False) -> None:
        if not task.enabled:
            task.next_run_at = None
            return
        if task.trigger == "cron":
            task.next_run_at = self._cron(task.schedule).next_after(datetime.now()).timestamp()
        else:
            base = time.time() if initial else (task.last_run_at or time.time())
            task.next_run_at = base + self._interval_seconds(task.schedule)

    # ------------------------------------------------------------------ 运行
    async def start(self) -> None:
        self.load()
        self._stop.clear()
        self._runner = asyncio.create_task(self._loop(), name="定时任务调度")
        logger.info("调度器已启动")

    async def stop(self) -> None:
        self._stop.set()
        if self._runner:
            self._runner.cancel()
            try:
                await self._runner
            except (asyncio.CancelledError, Exception):  # noqa: BLE001
                pass
            self._runner = None
        logger.info("调度器已停止")

    async def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                await self._tick()
            except Exception as exc:  # noqa: BLE001 - 调度循环不能死
                logger.exception("调度循环出错: %s", exc)
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                continue

    async def _tick(self) -> None:
        now = time.time()
        for task in self.tasks.values():
            if not task.enabled or task.next_run_at is None:
                continue
            if task.next_run_at > now:
                continue
            if task.task_id in self._running:
                continue
            self._schedule_next(task)
            asyncio.create_task(self.run_task(task), name=f"定时任务:{task.task_id}")

    async def run_task(self, task: ScheduledTask) -> Dict[str, Any]:
        """执行一次任务；返回执行摘要，供 WebUI 手动触发时展示。"""
        if task.task_id in self._running:
            return {"ok": False, "error": "任务正在运行"}
        script = self.scripts_dir / task.script_path
        if not script.is_file():
            task.failures += 1
            task.last_error = f"脚本不存在: {task.script_path}"
            logger.error("定时任务 %s 的脚本不存在: %s", task.task_id, script)
            return {"ok": False, "error": task.last_error}

        self._running.add(task.task_id)
        started = time.time()
        try:
            func = self._load_script(task.task_id, script)
            result = func(self.kernel)
            if asyncio.iscoroutine(result):
                result = await asyncio.wait_for(result, timeout=task.timeout)
            task.runs += 1
            task.last_result = str(result or "")
            task.last_error = ""
            summary = {"ok": True, "duration": round(time.time() - started, 2),
                       "result": task.last_result[:200]}
        except asyncio.TimeoutError:
            task.failures += 1
            task.last_error = f"执行超时（{task.timeout:g}s）"
            summary = {"ok": False, "error": task.last_error}
            logger.error("定时任务 %s 超时", task.task_id)
        except Exception as exc:  # noqa: BLE001
            task.failures += 1
            task.last_error = f"{type(exc).__name__}: {exc}"
            summary = {"ok": False, "error": task.last_error}
            logger.exception("定时任务 %s 执行失败: %s", task.task_id, exc)
        finally:
            task.last_duration = time.time() - started
            task.last_run_at = started
            self._running.discard(task.task_id)
            await self.kernel.db.set("tasks", task.task_id, task.to_dict())
        return summary

    def _load_script(self, task_id: str, path: Path):
        spec = importlib.util.spec_from_file_location(f"custom_bot_task_{task_id}", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"无法加载脚本: {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        func = getattr(module, "run", None) or getattr(module, "main", None)
        if not callable(func):
            raise RuntimeError(f"脚本 {path.name} 需要定义 run(kernel) 或 main(kernel)")
        return func

    # ------------------------------------------------------------------ 视图
    def list(self) -> List[Dict[str, Any]]:
        out = []
        for task in self.tasks.values():
            data = task.to_dict()
            data["running"] = task.task_id in self._running
            out.append(data)
        return out
