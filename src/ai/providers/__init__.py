"""LLM provider abstractions and registry."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from src.ai.schemas import Message, ToolCall


@dataclass
class CompletionChunk:
    content: str
    finish_reason: str | None = None
    tool_calls: list[ToolCall] | None = None


@dataclass
class CompletionResult:
    content: str
    tool_calls: list[ToolCall] | None = None
    finish_reason: str = "stop"
    usage: dict[str, int] | None = None
    model: str = ""
    provider: str = ""


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(
        self,
        model: str,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_config = kwargs

    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> CompletionResult:
        """Generate a completion (non-streaming)."""
        raise NotImplementedError

    @abstractmethod
    async def stream(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ):
        """Stream a completion."""
        yield

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider identifier."""
        pass

    def format_tools(self, tools: list[dict]) -> list[dict]:
        """Format tools for this provider's API."""
        return tools


class ProviderRegistry:
    """Registry for LLM providers."""

    _providers: ClassVar[dict[str, type[BaseProvider]]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[BaseProvider]):
        cls._providers[name] = provider_class

    @classmethod
    def get(cls, name: str) -> type[BaseProvider] | None:
        return cls._providers.get(name)

    @classmethod
    def create(cls, name: str, **kwargs) -> BaseProvider:
        provider_class = cls.get(name)
        if not provider_class:
            raise ValueError(f"Unknown provider: {name}")
        return provider_class(**kwargs)

    @classmethod
    def list_providers(cls) -> list[str]:
        return list(cls._providers.keys())


class CatalystProvider(BaseProvider):
    """Zoho Catalyst QuickML provider."""

    @property
    def provider_name(self) -> str:
        return "catalyst"

    async def complete(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> CompletionResult:
        last_msg = messages[-1].content if messages else ""
        return CompletionResult(
            content=f"[Catalyst] Response for: {last_msg[:100]}...",
            model=self.model,
            provider=self.provider_name,
        )

    async def stream(self, messages: list[Message], **kwargs):
        result = await self.complete(messages, **kwargs)
        yield CompletionChunk(content=result.content)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 1536 for _ in texts]


class OpenAICompatibleProvider(BaseProvider):
    """OpenAI API-compatible provider (Azure, Together, etc.)."""

    @property
    def provider_name(self) -> str:
        return "openai_compatible"

    async def complete(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> CompletionResult:
        last_msg = messages[-1].content if messages else ""
        return CompletionResult(
            content=f"[OpenAI-compatible] Response for: {last_msg[:100]}...",
            model=self.model,
            provider=self.provider_name,
        )

    async def stream(self, messages: list[Message], **kwargs):
        result = await self.complete(messages, **kwargs)
        yield CompletionChunk(content=result.content)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 1536 for _ in texts]


class MockProvider(BaseProvider):
    """Mock provider for testing without API keys."""

    @property
    def provider_name(self) -> str:
        return "mock"

    async def complete(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> CompletionResult:
        last_msg = messages[-1].content if messages else ""
        return CompletionResult(
            content=f"[MOCK] Generated response for query: {last_msg[:200]}",
            model=self.model,
            provider=self.provider_name,
            usage={"prompt_tokens": 50, "completion_tokens": 100},
        )

    async def stream(self, messages: list[Message], **kwargs):
        result = await self.complete(messages, **kwargs)
        for word in result.content.split():
            yield CompletionChunk(content=word + " ")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        import hashlib

        import numpy as np

        vectors = []
        for text in texts:
            hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
            np.random.seed(hash_val % (2**32))
            vec = np.random.normal(0, 1, 1536).astype(float)
            vec = vec / np.linalg.norm(vec)
            vectors.append(vec.tolist())
        return vectors


def create_provider(provider_type: str = "mock", **kwargs) -> BaseProvider:
    """Factory for providers."""
    # Ensure they are imported (to avoid circular imports if needed, though they are in submodules)
    from src.ai.providers.catalyst import CatalystProvider
    from src.ai.providers.groq import GroqProvider
    from src.ai.providers.openai import OpenAICompatibleProvider

    providers = {
        "catalyst": CatalystProvider,
        "openai": OpenAICompatibleProvider,
        "groq": GroqProvider,
        "mock": MockProvider,
    }
    if provider_type not in providers:
        raise ValueError(f"Unknown provider type: {provider_type}")
    return providers[provider_type](**kwargs)
