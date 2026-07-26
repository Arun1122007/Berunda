from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from src.ai.providers import create_provider

logger = logging.getLogger("berunda.embedding")


class EmbeddingProvider(ABC):
    """Abstract interface for embedding providers."""

    @abstractmethod
    async def create_embedding(self, text: str) -> list[float]:
        pass

    @abstractmethod
    async def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        pass

    @abstractmethod
    def health_check(self) -> dict:
        pass

    @abstractmethod
    def model_metadata(self) -> dict:
        pass


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider implementation."""

    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self._provider = create_provider("openai", model=self.model)

    async def create_embedding(self, text: str) -> list[float]:
        if not text:
            raise ValueError("Text cannot be empty.")
        embeddings = await self.create_embeddings([text])
        return embeddings[0] if embeddings else []

    async def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        try:
            # We assume self._provider.embed handles chunking/batching/retries internally
            embeddings = await self._provider.embed(texts)

            # Validate output dimension (1536 for text-embedding-3-small)
            if embeddings and len(embeddings[0]) not in (1536, 256, 512, 1024, 3072):
                logger.error(f"EMBEDDING_INVALID_DIMENSION: Received dimension {len(embeddings[0])}")
                raise ValueError("EMBEDDING_INVALID_DIMENSION")

            return embeddings
        except Exception as e:
            logger.error(f"EMBEDDING_PROVIDER_ERROR: {e}")
            raise

    def health_check(self) -> dict:
        return {"status": "ok", "provider": "openai", "model": self.model}

    def model_metadata(self) -> dict:
        return {
            "provider": "openai",
            "model": self.model,
            "dimension": 1536,
        }
