"""OpenAI 兼容的大模型客户端。

只依赖 aiohttp，支持任意 `base_url` + `/chat/completions` 的服务：
OpenAI、DeepSeek、火山方舟（Ark）、Moonshot、本地 vLLM / Ollama 网关等。

API Key 读取顺序：`brain.api_key` → 环境变量（默认 `CUSTOM_BOT_LLM_KEY`）。
不会把 Key 写进日志或状态接口。
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

import aiohttp


class LLMError(RuntimeError):
    """模型调用失败（网络、鉴权、限流、响应格式等）。"""


class LLMClient:
    def __init__(self, config, logger: Optional[logging.Logger] = None):
        self.enabled: bool = bool(config.get("brain.enabled", True))
        self.base_url: str = str(config.get("brain.base_url", "") or "").rstrip("/")
        self.model: str = str(config.get("brain.model", "") or "")
        api_key = str(config.get("brain.api_key", "") or "")
        if not api_key:
            env_name = str(config.get("brain.api_key_env", "CUSTOM_BOT_LLM_KEY") or "CUSTOM_BOT_LLM_KEY")
            api_key = os.environ.get(env_name, "")
        self.api_key: str = api_key
        self.temperature: float = float(config.get("brain.temperature", 0.7))
        self.max_tokens: int = int(config.get("brain.max_tokens", 800))
        self.timeout: float = float(config.get("brain.timeout", 60))
        self.retries: int = max(0, int(config.get("brain.retries", 1)))
        self.logger = logger or logging.getLogger("内核.LLM")
        self._session: Optional[aiohttp.ClientSession] = None
        self.stats: Dict[str, Any] = {
            "calls": 0,
            "errors": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "last_error": "",
            "last_latency": 0.0,
            "last_call_at": 0.0,
        }

    # ------------------------------------------------------------------ 状态
    @property
    def ready(self) -> bool:
        return bool(self.enabled and self.base_url and self.model and self.api_key)

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "ready": self.ready,
            "base_url": self.base_url,
            "model": self.model,
            "has_key": bool(self.api_key),
            **self.stats,
        }

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers=self._headers(),
            )
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    # ------------------------------------------------------------------ 调用
    async def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        if not self.ready:
            raise LLMError("大脑未配置：请在 config.yaml 的 brain 段填写 base_url / model / api_key")
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
            "max_tokens": self.max_tokens if max_tokens is None else max_tokens,
            "stream": False,
        }
        if response_format:
            payload["response_format"] = response_format

        last_error = ""
        for attempt in range(self.retries + 1):
            started = time.time()
            try:
                session = await self._ensure_session()
                async with session.post(f"{self.base_url}/chat/completions", json=payload) as resp:
                    text = await resp.text()
                    if resp.status == 429 or resp.status >= 500:
                        last_error = f"HTTP {resp.status}: {text[:200]}"
                        if attempt < self.retries:
                            await asyncio.sleep(1.5 * (attempt + 1))
                            continue
                        raise LLMError(last_error)
                    if resp.status in (401, 403):
                        raise LLMError(f"鉴权失败（HTTP {resp.status}），请检查 api_key")
                    if resp.status != 200:
                        raise LLMError(f"HTTP {resp.status}: {text[:200]}")

                    try:
                        data = json.loads(text)
                    except json.JSONDecodeError as exc:
                        raise LLMError(f"模型返回非 JSON：{text[:120]}") from exc

                content = self._extract_content(data)
                usage = data.get("usage") or {}
                self.stats["calls"] += 1
                self.stats["prompt_tokens"] += int(usage.get("prompt_tokens", 0) or 0)
                self.stats["completion_tokens"] += int(usage.get("completion_tokens", 0) or 0)
                self.stats["last_latency"] = round(time.time() - started, 3)
                self.stats["last_call_at"] = time.time()
                if not content.strip():
                    raise LLMError("模型返回空内容")
                return content

            except asyncio.TimeoutError as exc:
                last_error = f"请求超时（{self.timeout:g}s）"
                if attempt < self.retries:
                    await asyncio.sleep(1.0)
                    continue
                self.stats["errors"] += 1
                self.stats["last_error"] = last_error
                raise LLMError(last_error) from exc
            except aiohttp.ClientError as exc:
                last_error = f"网络错误：{exc}"
                if attempt < self.retries:
                    await asyncio.sleep(1.5 * (attempt + 1))
                    continue
                self.stats["errors"] += 1
                self.stats["last_error"] = last_error
                raise LLMError(last_error) from exc
            except LLMError as exc:
                self.stats["errors"] += 1
                self.stats["last_error"] = str(exc)
                raise

        raise LLMError(last_error or "未知错误")

    @staticmethod
    def _extract_content(data: Dict[str, Any]) -> str:
        choices = data.get("choices") or []
        if not choices:
            raise LLMError(f"响应里没有 choices：{str(data)[:120]}")
        choice = choices[0] or {}
        message = choice.get("message") or {}
        content = message.get("content")
        if content is None:
            content = choice.get("text") or ""
        if isinstance(content, list):  # 多模态分段
            content = "".join(
                part.get("text", "") for part in content if isinstance(part, dict)
            )
        return str(content)
