"""Multi-provider automatic fallback chain (Groq -> Nvidia -> OpenRouter -> OpenAI -> Catalyst -> Mock)."""

from __future__ import annotations

from src.ai.providers import BaseProvider, CompletionResult, MockProvider
from src.ai.schemas import Message
from src.shared.logging import get_logger

logger = get_logger(__name__)


class FallbackProvider(BaseProvider):
    """Resilient provider wrapper that automatically falls back across Groq, Nvidia, OpenRouter, OpenAI, Catalyst, and Mock."""

    def __init__(self, **kwargs):
        super().__init__(model="fallback-chain", **kwargs)
        self.chain: list[BaseProvider] = []
        self._init_chain(**kwargs)

    def _init_chain(self, **kwargs):
        from src.ai.providers.catalyst import CatalystProvider
        from src.ai.providers.groq import GroqProvider
        from src.ai.providers.nvidia import NvidiaProvider
        from src.ai.providers.openai import OpenAICompatibleProvider
        from src.ai.providers.openrouter import OpenRouterProvider

        candidates = [
            ("groq", GroqProvider),
            ("nvidia", NvidiaProvider),
            ("openrouter", OpenRouterProvider),
            ("openai", OpenAICompatibleProvider),
            ("catalyst", CatalystProvider),
        ]

        for name, cls in candidates:
            try:
                p = cls(**kwargs)
                if getattr(p, "api_key", None):
                    self.chain.append(p)
                    logger.info(f"FallbackChain: Enrolled provider '{name}' with active API key")
            except Exception as e:
                logger.debug(f"FallbackChain: Provider '{name}' not configured: {e}")

        # Always append MockProvider as absolute safety net
        self.chain.append(MockProvider(model="mock-fallback", **kwargs))

    @property
    def provider_name(self) -> str:
        return "fallback"

    async def complete(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> CompletionResult:
        errors = []
        for provider in self.chain:
            try:
                if provider.provider_name != "mock" and not getattr(provider, "api_key", None):
                    continue
                logger.info(f"FallbackChain: Attempting completion via '{provider.provider_name}'...")
                res = await provider.complete(messages, tools=tools, **kwargs)
                if res and res.content and not res.content.startswith("[Mocked"):
                    return res
                if provider.provider_name == "mock":
                    return res
            except Exception as exc:
                logger.warning(f"FallbackChain: Provider '{provider.provider_name}' failed: {exc}")
                errors.append(f"{provider.provider_name}: {exc}")

        # Final safety net
        mock = MockProvider(model="mock-safety", **kwargs)
        return await mock.complete(messages, tools=tools, **kwargs)

    async def stream(self, messages: list[Message], tools: list[dict] | None = None, **kwargs):
        for provider in self.chain:
            try:
                if provider.provider_name != "mock" and not getattr(provider, "api_key", None):
                    continue
                logger.info(f"FallbackChain: Attempting stream via '{provider.provider_name}'...")
                async for chunk in provider.stream(messages, tools=tools, **kwargs):
                    yield chunk
                return
            except Exception as exc:
                logger.warning(f"FallbackChain: Provider '{provider.provider_name}' stream failed: {exc}")

        mock = MockProvider(model="mock-safety", **kwargs)
        async for chunk in mock.stream(messages, tools=tools, **kwargs):
            yield chunk

    async def embed(self, texts: list[str]) -> list[list[float]]:
        for provider in self.chain:
            try:
                if provider.provider_name != "mock" and not getattr(provider, "api_key", None):
                    continue
                vecs = await provider.embed(texts)
                if vecs and any(any(v != 0.0 for v in vec) for vec in vecs):
                    return vecs
            except Exception as exc:
                logger.warning(f"FallbackChain: Provider '{provider.provider_name}' embed failed: {exc}")

        mock = MockProvider(model="mock-safety")
        return await mock.embed(texts)
