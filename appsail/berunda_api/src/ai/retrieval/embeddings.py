from __future__ import annotations

from abc import ABC, abstractmethod

from src.ai.providers import BaseProvider


class BaseEmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the embedding dimension."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier."""
        pass


class ProviderEmbeddingWrapper(BaseEmbeddingProvider):
    """Wrap an LLM provider's embed method as an embedding provider."""

    def __init__(self, provider: BaseProvider):
        self.provider = provider

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return await self.provider.embed(texts)

    @property
    def dimension(self) -> int:
        # Default dimension - would need to be configured per provider
        return 1536

    @property
    def model_name(self) -> str:
        return getattr(self.provider, "model", "unknown")


class TFIDFEmbeddingProvider(BaseEmbeddingProvider):
    """TF-IDF based embeddings for development (no external API needed)."""

    def __init__(self, max_features: int = 5000):
        from sklearn.feature_extraction.text import TfidfVectorizer

        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words="english",
            ngram_range=(1, 2),
        )
        self._fitted = False
        self._vocab: dict[str, int] = {}

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not self._fitted:
            self.vectorizer.fit(texts)
            self._vocab = self.vectorizer.vocabulary_
            self._fitted = True
        vectors = self.vectorizer.transform(texts)
        return vectors.toarray().tolist()

    @property
    def dimension(self) -> int:
        return self.vectorizer.get_params()["max_features"] or 5000

    @property
    def model_name(self) -> str:
        return "tfidf-sklearn"


def create_embedding_provider(provider_type: str = "tfidf", **kwargs) -> BaseEmbeddingProvider:
    """Factory function to create embedding providers."""
    if provider_type == "tfidf":
        return TFIDFEmbeddingProvider(**kwargs)
    if provider_type == "provider":
        # Would need an actual LLM provider instance
        raise NotImplementedError("Use TFIDFEmbeddingProvider for development")
    raise ValueError(f"Unknown embedding provider type: {provider_type}")
