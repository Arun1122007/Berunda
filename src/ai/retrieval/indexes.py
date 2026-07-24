from __future__ import annotations

from abc import ABC, abstractmethod


class BaseIndex(ABC):
    """Abstract base class for search indexes."""

    @abstractmethod
    def add(self, ids: list[str], vectors: list[list[float]], metadata: list[dict]) -> None:
        pass

    @abstractmethod
    def search(self, query: list[float], top_k: int, filter: dict | None = None) -> list[dict]:
        pass

    @abstractmethod
    def delete(self, ids: list[str]) -> bool:
        pass


class InMemoryIndex(BaseIndex):
    """Simple in-memory vector index with linear search."""

    def __init__(self):
        self.ids: list[str] = []
        self.vectors: list[list[float]] = []
        self.metadata: list[dict] = []

    def add(self, ids: list[str], vectors: list[list[float]], metadata: list[dict]) -> None:
        self.ids.extend(ids)
        self.vectors.extend(vectors)
        self.metadata.extend(metadata)

    def search(self, query: list[float], top_k: int, filter: dict | None = None) -> list[dict]:
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity

        if not self.vectors:
            return []

        query_vec = np.array(query).reshape(1, -1)
        doc_vecs = np.array(self.vectors)
        similarities = cosine_similarity(query_vec, doc_vecs)[0]

        valid_indices = list(range(len(self.ids)))
        if filter:
            valid_indices = [
                i
                for i in valid_indices
                if all(self.metadata[i].get(k) == v for k, v in filter.items())
            ]

        if not valid_indices:
            return []

        filtered_similarities = similarities[valid_indices]
        top_indices = np.argsort(filtered_similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            original_idx = valid_indices[idx]
            results.append(
                {
                    "id": self.ids[original_idx],
                    "vector": self.vectors[original_idx],
                    "metadata": self.metadata[original_idx],
                    "score": float(filtered_similarities[idx]),
                }
            )
        return results

    def delete(self, ids: list[str]) -> bool:
        id_set = set(ids)
        keep = [i for i, id_ in enumerate(self.ids) if id_ not in id_set]
        self.ids = [self.ids[i] for i in keep]
        self.vectors = [self.vectors[i] for i in keep]
        self.metadata = [self.metadata[i] for i in keep]
        return True


class FAISSIndex(BaseIndex):
    """FAISS-based index for production (placeholder)."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self._index = None
        self.ids: list[str] = []
        self.metadata: list[dict] = []

    def add(self, ids: list[str], vectors: list[list[float]], metadata: list[dict]) -> None:
        import faiss
        import numpy as np

        if self._index is None:
            self._index = faiss.IndexFlatIP(self.dimension)

        vecs = np.array(vectors, dtype=np.float32)
        faiss.normalize_L2(vecs)
        self._index.add(vecs)
        self.ids.extend(ids)
        self.metadata.extend(metadata)

    def search(self, query: list[float], top_k: int, filter: dict | None = None) -> list[dict]:
        import faiss
        import numpy as np

        if self._index is None or self._index.ntotal == 0:
            return []

        query_vec = np.array([query], dtype=np.float32)
        faiss.normalize_L2(query_vec)
        scores, indices = self._index.search(query_vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.ids):
                continue
            results.append(
                {
                    "id": self.ids[idx],
                    "metadata": self.metadata[idx],
                    "score": float(score),
                }
            )
        return results

    def delete(self, ids: list[str]) -> bool:  # noqa: ARG002
        # FAISS doesn't support deletion easily - would need IndexIDMap
        return False


def create_index(index_type: str = "memory", **kwargs) -> BaseIndex:
    """Factory for indexes."""
    if index_type == "memory":
        return InMemoryIndex()
    if index_type == "faiss":
        return FAISSIndex(**kwargs)
    raise ValueError(f"Unknown index type: {index_type}")
