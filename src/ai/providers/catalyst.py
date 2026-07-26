from __future__ import annotations

import json
import logging
import os
import uuid
from typing import Any

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
from src.exceptions import AIServiceError

logger = logging.getLogger(__name__)

_CATALYST_RETRY = {
    "stop": stop_after_attempt(settings.AI_MAX_RETRIES),
    "wait": wait_exponential(multiplier=settings.AI_RETRY_DELAY, min=1, max=30),
    "before_sleep": before_sleep_log(logger, logging.WARNING),
    "retry": retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError)),
}


def _map_error(response: httpx.Response) -> AIServiceError:
    status = response.status_code
    detail = {}
    try:
        detail = response.json()
    except Exception:
        detail = {"body": response.text[:500]}

    if status == 401:
        return AIServiceError("Catalyst authentication failed — check API key", detail=detail)
    if status == 404:
        return AIServiceError("Catalyst function endpoint not found", detail=detail)
    if status == 429:
        return AIServiceError("Catalyst rate limit exceeded", detail=detail)
    if status >= 500:
        return AIServiceError("Catalyst server error", detail=detail)
    return AIServiceError(f"Catalyst request failed (HTTP {status})", detail=detail)


def _init_sdk() -> Any | None:
    try:
        import zcatalyst_sdk

        if os.environ.get("CATALYST_PROJECT_ID") and os.environ.get("CATALYST_API_KEY"):
            from zcatalyst_sdk.credentials import CredentialHeader

            creds = CredentialHeader(
                os.environ["CATALYST_PROJECT_ID"],
                os.environ.get("CATALYST_PROJECT_DOMAIN", ""),
                os.environ["CATALYST_API_KEY"],
                os.environ.get("CATALYST_ENVIRONMENT_ID", ""),
            )
            app = zcatalyst_sdk.initialize_app(credential=creds)
            logger.info("zcatalyst_sdk initialized with credentials")
            return app
        app = zcatalyst_sdk.initialize()
        logger.info("zcatalyst_sdk initialized (in-function mode)")
        return app
    except Exception as exc:
        logger.warning("zcatalyst_sdk not available: %s — falling back to HTTP", exc)
        return None


class CatalystProvider(BaseProvider):
    def __init__(
        self,
        model: str,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        project_id: str | None = None,
        api_key: str | None = None,
        function_base: str | None = None,
        request_timeout: float = 30.0,
        **kwargs,
    ):
        super().__init__(model, temperature, max_tokens, **kwargs)
        self.project_id = project_id or os.environ.get("CATALYST_PROJECT_ID", "")
        self.api_key = api_key or os.environ.get("CATALYST_API_KEY", "")
        self.function_base = function_base or os.environ.get(
            "CATALYST_FUNCTION_BASE",
            f"https://catalyst.zoho.com/baas/v1/project/{self.project_id}",
        )
        self.request_timeout = request_timeout
        self._client: httpx.AsyncClient | None = None
        self._sdk_app = _init_sdk()

    @property
    def provider_name(self) -> str:
        return "catalyst"

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.function_base,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=self.request_timeout,
            )
        return self._client

    async def health_check(self) -> dict[str, Any]:
        if self._sdk_app:
            try:
                from zcatalyst_sdk import CatalystApp
                _: CatalystApp = self._sdk_app
                return {"status": "ok", "detail": "zcatalyst_sdk connected"}
            except Exception as exc:
                return {"status": "unreachable", "detail": str(exc)}
        client = self._get_client()
        try:
            resp = await client.get("/api/v1/health", timeout=10.0)
            resp.raise_for_status()
            return {"status": "ok", "detail": resp.json()}
        except httpx.HTTPError as exc:
            return {"status": "unreachable", "detail": str(exc)}

    def _build_payload(self, messages: list[dict], stream: bool = False, tools: list[dict] | None = None) -> dict:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": stream,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        return payload

    async def _sdk_complete(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        if not self._sdk_app:
            raise AIServiceError("zcatalyst_sdk not initialized")
        try:
            funcs = self._sdk_app.get_functions()
            result = funcs.execute("llm-chat", {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "tools": tools,
            })
            return result
        except Exception as exc:
            raise AIServiceError(f"Catalyst SDK function execution failed: {exc}") from exc

    async def _sdk_embed(self, texts: list[str]) -> list[list[float]]:
        if not self._sdk_app:
            raise AIServiceError("zcatalyst_sdk not initialized")
        try:
            funcs = self._sdk_app.get_functions()
            result = funcs.execute("llm-embed", {
                "model": self.model,
                "input": texts,
            })
            return result.get("data", [])
        except Exception as exc:
            raise AIServiceError(f"Catalyst SDK embedding failed: {exc}") from exc

    @retry(**_CATALYST_RETRY)
    async def _post_chat(self, payload: dict, correlation_id: str | None = None) -> dict:
        client = self._get_client()
        headers = {}
        if correlation_id:
            headers["X-Correlation-ID"] = correlation_id

        response = await client.post("/api/v1/chat", json=payload, headers=headers)
        if response.is_error:
            raise _map_error(response)
        return response.json()

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> CompletionResult:
        correlation_id = kwargs.pop("correlation_id", str(uuid.uuid4()))

        if self._sdk_app:
            data = await self._sdk_complete(messages, tools=tools)
        else:
            payload = self._build_payload(messages, stream=False, tools=tools)
            data = await self._post_chat(payload, correlation_id=correlation_id)

        choice = data.get("choices", [{}])[0]
        tool_calls = choice.get("message", {}).get("tool_calls")
        formatted_tools = None
        if tool_calls:
            formatted_tools = [
                {"id": tc["id"], "name": tc["function"]["name"], "arguments": tc["function"]["arguments"]}
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
        **kwargs,
    ):
        correlation_id = kwargs.pop("correlation_id", str(uuid.uuid4()))

        if self._sdk_app:
            data = await self._sdk_complete(messages, tools=tools)
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if content:
                yield CompletionChunk(content=content)
            return

        payload = self._build_payload(messages, stream=True, tools=tools)
        client = self._get_client()
        headers = {"X-Correlation-ID": correlation_id}

        async with client.stream("POST", "/api/v1/chat", json=payload, headers=headers) as response:
            if response.is_error:
                raise _map_error(response)
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        delta = data.get("choices", [{}])[0].get("delta", {})
                        if delta.get("content"):
                            yield CompletionChunk(content=delta["content"])
                    except Exception:
                        pass

    @retry(**_CATALYST_RETRY)
    async def embed(self, texts: list[str]) -> list[list[float]]:
        if self._sdk_app:
            return await self._sdk_embed(texts)

        correlation_id = str(uuid.uuid4())
        client = self._get_client()
        payload = {"model": self.model, "input": texts}
        headers = {"X-Correlation-ID": correlation_id}

        response = await client.post("/api/v1/embed", json=payload, headers=headers)
        if response.is_error:
            raise _map_error(response)
        data = response.json()
        return [item["embedding"] for item in data.get("data", [])]

    async def extract_entities_ner(self, text: str) -> dict[str, Any]:
        if not self._sdk_app:
            raise AIServiceError("NER extraction requires zcatalyst_sdk")
        try:
            zia = self._sdk_app.get_zia()
            result = zia.get_NER_prediction([text])
            return result
        except Exception as exc:
            raise AIServiceError(f"Catalyst NER extraction failed: {exc}") from exc

    async def analyze_sentiment(self, text: str) -> list[dict[str, Any]]:
        if not self._sdk_app:
            raise AIServiceError("Sentiment analysis requires zcatalyst_sdk")
        try:
            zia = self._sdk_app.get_zia()
            result = zia.get_sentiment_analysis([text])
            return result
        except Exception as exc:
            raise AIServiceError(f"Catalyst sentiment analysis failed: {exc}") from exc

    async def close(self):
        if self._client:
            await self._client.aclose()


ProviderRegistry.register("catalyst", CatalystProvider)
