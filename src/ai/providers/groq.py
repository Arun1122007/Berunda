"""Groq API provider."""

from __future__ import annotations

import os

from src.ai.providers.openai import OpenAICompatibleProvider


class GroqProvider(OpenAICompatibleProvider):
    """Groq API provider extending OpenAI base."""

    def __init__(
        self, model: str = "llama-3.3-70b-versatile", api_key: str | None = None, **kwargs
    ):
        api_key = api_key or os.environ.get("GROQ_API_KEY")
        base_url = "https://api.groq.com/openai/v1"
        super().__init__(model=model, api_key=api_key, base_url=base_url, **kwargs)

    @property
    def provider_name(self) -> str:
        return "groq"
