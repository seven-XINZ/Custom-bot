#!/usr/bin/env python3
"""Custom-bot 启动入口。

    python main.py                      # 读 config/config.yaml
    python main.py --config other.yaml
    python main.py --check-config       # 只校验配置，不启动
    python main.py --log-level DEBUG
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

# 保证从任何目录启动都能 import core / Adapter / plugins
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core import load_config  # noqa: E402
from core.kernel import RobotKernel  # noqa: E402
from core.utils import setup_logging  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="custom-bot", description="多平台聊天机器人框架")
    parser.add_argument("-c", "--config", default=str(ROOT / "config" / "config.yaml"),
                        help="配置文件路径（默认 config/config.yaml）")
    parser.add_argument("--log-level", default=None, help="覆盖配置里的日志级别")
    parser.add_argument("--check-config", action="store_true", help="只校验配置后退出")
    parser.add_argument("--version", action="store_true", help="打印版本后退出")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    try:
        config = load_config(args.config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[配置错误] {exc}", file=sys.stderr)
        return 2

    if args.version:
        print(f"Custom-bot {config.get('kernel.version', '1.0.0')}")
        return 0

    if args.check_config:
        problems = config.validate()
        if problems:
            print("配置存在问题：")
            for item in problems:
                print(f"  - {item}")
            return 1
        print("配置校验通过。")
        print(f"  适配器: {len(list(config.iter_adapters()))} 个")
        print(f"  插件配置: {len(list(config.iter_handlers()))} 个")
        print(f"  WebUI: {config.get('webui.host')}:{config.get('webui.port')}")
        model = str(config.get("brain.model", "") or "")
        key = str(config.get("brain.api_key", "") or "")
        if not key:
            key = os.environ.get(str(config.get("brain.api_key_env", "CUSTOM_BOT_LLM_KEY")), "")
        print(f"  心智: {config.get('persona.name', '小栖')} / {model or '未配置模型'}"
              f"（{'已配置 Key' if key else '缺少 Key，AI 功能不可用'}）")
        return 0

    setup_logging(
        level=args.log_level or str(config.get("logging.level", config.get("kernel.log_level", "INFO"))),
        log_dir=str(config.get("logging.dir", "data/logs")),
        file_name=str(config.get("logging.file", "custom-bot.log")),
        max_bytes=int(config.get("logging.max_bytes", 5 * 1024 * 1024)),
        backup_count=int(config.get("logging.backup_count", 5)),
        console=bool(config.get("logging.console", True)),
    )

    kernel = RobotKernel(config)
    try:
        asyncio.run(kernel.run())
    except KeyboardInterrupt:
        print("\n已中断。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
