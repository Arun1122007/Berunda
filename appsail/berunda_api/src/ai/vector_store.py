from __future__ import annotations

from abc import ABC, abstractmethod


class VectorStore(ABC):
    """Abstract interface for a vector store."""

    @abstractmethod
    async def upsert(self, records: list[dict]):
        """Upsert a list of vector records.

        records format:
        [
            {
                "id": str,
                "vector": list[float],
                "metadata": dict
            }, ...
        ]
        """
        pass

    @abstractmethod
    async def search(self, vector: list[float], filters: dict, limit: int = 10) -> list[dict]:
        """Search for similar vectors.

        Returns list of matching records with 'id', 'score', and 'metadata'.
        """
        pass

    @abstractmethod
    async def delete(self, record_ids: list[str]):
        """Delete records by ID."""
        pass

    @abstractmethod
    async def fetch(self, record_ids: list[str]) -> list[dict]:
        """Fetch records by ID."""
        pass

    @abstractmethod
    def health_check(self) -> dict:
        """Return health status of the vector store."""
        pass
