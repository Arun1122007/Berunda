from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseReranker(ABC):
    """Abstract base class for rerankers."""

    @abstractmethod
    async def rerank(
        self,
        query: str,
        documents: list[dict[str, Any]],
        top_k: int,
    ) -> list[dict[str, Any]]:
        """Rerank documents by relevance to query."""
        pass


class CrossEncoderReranker(BaseReranker):
    """Cross-encoder based reranker using sentence-transformers."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    async def rerank(
        self,
        query: str,
        documents: list[dict[str, Any]],
        top_k: int,
    ) -> list[dict[str, Any]]:
        if not documents:
            return []

        if self._model is None:
            from sentence_transformers import CrossEncoder

            self._model = CrossEncoder(self.model_name)

        pairs = [(query, doc.get("text", "")) for doc in documents]
        scores = self._model.predict(pairs)

        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)

        documents.sort(key=lambda d: d.get("rerank_score", 0), reverse=True)
        return documents[:top_k]


class LLMBasedReranker(BaseReranker):
    """LLM-based reranker using a provider."""

    def __init__(self, provider: Any):
        self.provider = provider

    async def rerank(
        self,
        query: str,
        documents: list[dict[str, Any]],
        top_k: int,
    ) -> list[dict[str, Any]]:
        if not documents:
            return []

        # Use LLM to score relevance
        prompt = f"Query: {query}\n\nRate the relevance of each document (0-1):\n"
        for i, doc in enumerate(documents):
            prompt += f"{i + 1}. {doc.get('text', '')[:500]}\n"

        # Would call provider here - simplified for now
        return documents[:top_k]


def create_reranker(reranker_type: str = "cross_encoder", **kwargs) -> BaseReranker:
    """Factory for rerankers."""
    if reranker_type == "cross_encoder":
        return CrossEncoderReranker(**kwargs)
    if reranker_type == "llm":
        return LLMBasedReranker(**kwargs)
    raise ValueError(f"Unknown reranker type: {reranker_type}")
