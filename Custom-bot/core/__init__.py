"""Custom-bot 框架内核。

对外只需要三个名字：

    from core import RobotKernel, load_config
    kernel = RobotKernel(load_config("config/config.yaml"))
    await kernel.run()

其余模块（message / adapters / handlers / scheduler / webui）在需要时再单独导入。
"""

from .config import Config, load_config
from .message import Attachment, InternalMessage

__all__ = ["Config", "load_config", "RobotKernel", "Attachment", "InternalMessage"]


def __getattr__(name: str):
    # 延迟导入 RobotKernel，避免 core/__init__ → kernel → webui → aiohttp 的启动期强依赖
    if name == "RobotKernel":
        from .kernel import RobotKernel

        return RobotKernel
    raise AttributeError(name)
