"""OpenAI-compatible API provider (works with OpenAI, Groq, Together, Mistral, etc.) with retry."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.ai.providers import BaseProvider, CompletionChunk, CompletionResult
from src.ai.schemas import Message, ToolCall
from src.config import settings
from src.shared.logging import get_logger

logger = get_logger(__name__)

_RETRY_KWARGS = {
    "stop": stop_after_attempt(settings.AI_MAX_RETRIES),
    "wait": wait_exponential(multiplier=settings.AI_RETRY_DELAY, min=1, max=30),
    "before_sleep": before_sleep_log(logger, logging.WARNING),
    "retry": retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException)),
}


class OpenAICompatibleProvider(BaseProvider):
    """OpenAI API-compatible provider with exponential backoff retry."""

    def __init__(
        self, model: str, api_key: str | None = None, base_url: str | None = None, **kwargs
    ):
        super().__init__(model, **kwargs)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        if not self.api_key:
            logger.warning(f"{self.provider_name} initialized without API key")

    @property
    def provider_name(self) -> str:
        return "openai"

    @retry(**_RETRY_KWARGS)  # type: ignore[call-overload]
    async def _post_chat(self, payload: dict, headers: dict) -> dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload
            )
            response.raise_for_status()
            return response.json()

    async def complete(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> CompletionResult:
        if not self.api_key:
            return CompletionResult(
                content=f"[Mocked {self.provider_name}] Please set API key.",
                model=self.model,
                provider=self.provider_name,
            )

        payload = {
            "model": self.model,
            "messages": [{k: v for k, v in asdict(m).items() if v is not None} for m in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            **self.extra_config,
            **kwargs,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        try:
            data = await self._post_chat(payload, headers)
            choice = data["choices"][0]
            message = choice.get("message", {})

            parsed_tools = None
            if "tool_calls" in message:
                parsed_tools = []
                for tc in message["tool_calls"]:
                    parsed_tools.append(
                        ToolCall(
                            id=tc["id"],
                            type=tc["type"],
                            function={
                                "name": tc["function"]["name"],
                                "arguments": tc["function"]["arguments"],
                            },
                        )
                    )

            return CompletionResult(
                content=message.get("content", "") or "",
                tool_calls=parsed_tools,
                finish_reason=choice.get("finish_reason", "stop"),
                usage=data.get("usage", {}),
                model=self.model,
                provider=self.provider_name,
            )
        except Exception as e:
            logger.error(f"{self.provider_name} completion failed: {e}")
            raise

    async def stream(self, messages: list[Message], tools: list[dict] | None = None, **kwargs):  # noqa: ARG002
        if not self.api_key:
            yield CompletionChunk(content=f"[Mocked {self.provider_name}] Please set API key.")
            return

        payload = {
            "model": self.model,
            "messages": [{k: v for k, v in asdict(m).items() if v is not None} for m in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
            **self.extra_config,
            **kwargs,
        }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                async with client.stream(
                    "POST", f"{self.base_url}/chat/completions", headers=headers, json=payload
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                choice = data["choices"][0]
                                delta = choice.get("delta", {})
                                content = delta.get("content", "")

                                if content:
                                    yield CompletionChunk(
                                        content=content, finish_reason=choice.get("finish_reason")
                                    )
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                logger.error(f"{self.provider_name} streaming failed: {e}")
                raise

    @retry(**_RETRY_KWARGS)  # type: ignore[call-overload]
    async def _post_embed(self, payload: dict, headers: dict) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/embeddings", headers=headers, json=payload
            )
            response.raise_for_status()
            data = response.json()
            return [item["embedding"] for item in data["data"]]

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not self.api_key:
            logger.warning(f"{self.provider_name} embed: no API key — returning zero vectors")
            return [[0.0] * 1536 for _ in texts]

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"input": texts, "model": "text-embedding-3-small"}

        try:
            return await self._post_embed(payload, headers)
        except Exception as e:
            logger.error(f"{self.provider_name} embedding failed: {e}")
            return [[0.0] * 1536 for _ in texts]
