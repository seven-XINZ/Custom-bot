"""定时自省任务：让心智定期回顾最近对话与运行状态。

在 config.yaml 的 scheduled_tasks 里启用后按 interval 或 cron 运行。
"""


async def run(kernel):
    mind = getattr(kernel, "mind", None)
    if mind is None or not mind.enabled:
        return "心智未启用"
    if not mind.ready:
        return "心智未接通模型，跳过自省"
    return await mind.reflect()
