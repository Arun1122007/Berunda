"""
LLM provider abstraction — base class, registry, and concrete implementations.

The provider layer decouples the AI module from any specific LLM backend.
Each provider implements the ``BaseProvider`` interface and registers itself
with the ``ProviderRegistry``.

Exports:
    BaseProvider: Abstract base class for all LLM providers.
    ProviderRegistry: Singleton registry mapping provider names to classes.
    CatalystProvider: Provider for Zoho Catalyst QuickML endpoints.
    OpenAICompatibleProvider: Provider for OpenAI-compatible APIs.
"""

from berunda.ai.providers.base import BaseProvider
from berunda.ai.providers.registry import ProviderRegistry
from berunda.ai.providers.catalyst import CatalystProvider
from berunda.ai.providers.openai_compat import OpenAICompatibleProvider


def get_provider(name: str | None = None) -> BaseProvider:
    """Get a configured provider instance by name.

    Args:
        name: Provider name (``catalyst``, ``openai``). If ``None``, uses
              the default provider from config.

    Returns:
        An initialized provider instance with loaded configuration.
    """
    return ProviderRegistry.get(name)


__all__ = [
    "BaseProvider",
    "ProviderRegistry",
    "CatalystProvider",
    "OpenAICompatibleProvider",
    "get_provider",
]
