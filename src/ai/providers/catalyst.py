from __future__ import annotations

import logging
import os

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.ai.providers import BaseProvider, CompletionChunk, CompletionResult, ProviderRegistry
from src.config import settings

_CATALYST_RETRY = {
    "stop": stop_after_attempt(settings.AI_MAX_RETRIES),
    "wait": wait_exponential(multiplier=settings.AI_RETRY_DELAY, min=1, max=30),
    "before_sleep": before_sleep_log(logging.getLogger(__name__), logging.WARNING),
    "retry": retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException)),
}


class CatalystProvider(BaseProvider):
    """Zoho Catalyst QuickML provider."""

    def __init__(
        self,
        model: str,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        project_id: str | None = None,
        api_key: str | None = None,
        **kwargs,
    ):
        super().__init__(model, temperature, max_tokens, **kwargs)
        self.project_id = project_id or os.environ.get("CATALYST_PROJECT_ID", "")
        self.api_key = api_key or os.environ.get("CATALYST_API_KEY", "")
        self._client = None

    @property
    def provider_name(self) -> str:
        return "catalyst"

    def _get_base_url(self) -> str:
        return f"https://catalyst.zoho.com/baas/v1/project/{self.project_id}"

    def _get_client(self):
        if self._client is None:
            try:
                import httpx

                self._client = httpx.AsyncClient(
                    base_url=self._get_base_url(),
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout=60.0,
                )
            except ImportError:
                raise RuntimeError("httpx not installed. Install with: pip install httpx")
        return self._client

    @retry(**_CATALYST_RETRY)
    async def _post_chat(self, payload: dict) -> dict:
        client = self._get_client()
        response = await client.post("/functions/llm-chat/execute", json=payload)
        response.raise_for_status()
        return response.json()

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs,  # noqa: ARG002
    ) -> CompletionResult:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        data = await self._post_chat(payload)

        # Catalyst-specific response format
        choice = data["data"] if "data" in data else data.get("choices", [{}])[0]

        tool_calls = choice.get("message", {}).get("tool_calls")
        formatted_tools = None
        if tool_calls:
            formatted_tools = [
                {
                    "id": tc["id"],
                    "name": tc["function"]["name"],
                    "arguments": tc["function"]["arguments"],
                }
                for tc in tool_calls
            ]

        return CompletionResult(
            content=choice.get("message", {}).get("content", ""),
            tool_calls=formatted_tools,
            finish_reason=choice.get("finish_reason", "stop"),
            usage=choice.get("usage"),
            model=self.model,
            provider=self.provider_name,
        )

    async def stream(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs,  # noqa: ARG002
    ):
        client = self._get_client()
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        async with client.stream("POST", "/functions/llm-chat/execute", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        import json

                        data = json.loads(data_str)
                        delta = data["choices"][0].get("delta", {})
                        if delta.get("content"):
                            yield CompletionChunk(content=delta["content"])
                    except Exception:
                        pass

    async def embed(self, texts: list[str]) -> list[list[float]]:
        client = self._get_client()
        payload = {"model": self.model, "input": texts}
        response = await client.post("/functions/llm-embed/execute", json=payload)
        response.raise_for_status()
        data = response.json()
        return [item["embedding"] for item in data.get("data", [])]

    async def close(self):
        if self._client:
            await self._client.aclose()


# Register provider
ProviderRegistry.register("catalyst", CatalystProvider)
