"""OpenRouter API provider."""

from __future__ import annotations

import os

from src.ai.providers.openai import OpenAICompatibleProvider


class OpenRouterProvider(OpenAICompatibleProvider):
    """OpenRouter API provider extending OpenAI base."""

    def __init__(
        self,
        model: str = "meta-llama/llama-3.3-70b-instruct",
        api_key: str | None = None,
        base_url: str | None = None,
        **kwargs,
    ):
        api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        base_url = base_url or os.environ.get(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        )
        super().__init__(model=model, api_key=api_key, base_url=base_url, **kwargs)

    @property
    def provider_name(self) -> str:
        return "openrouter"
