from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class BaseVectorStore(ABC):
    """Abstract base class for vector stores."""

    @abstractmethod
    async def add(
        self, texts: list[str], embeddings: list[list[float]], metadatas: list[dict]
    ) -> list[str]:
        """Add documents to the store. Returns list of IDs."""
        pass

    @abstractmethod
    async def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filter: dict | None = None,
    ) -> list[dict]:
        """Search for similar documents. Returns list of {id, text, metadata, score}."""
        pass

    @abstractmethod
    async def delete(self, ids: list[str]) -> bool:
        """Delete documents by IDs."""
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """Clear all documents."""
        pass


class InMemoryVectorStore(BaseVectorStore):
    """In-memory vector store using numpy/scikit-learn for development."""

    def __init__(self):
        self._ids: list[str] = []
        self._texts: list[str] = []
        self._embeddings: list[list[float]] = []
        self._metadatas: list[dict] = []

    async def add(
        self,
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> list[str]:
        import uuid

        new_ids = [str(uuid.uuid4()) for _ in texts]
        self._ids.extend(new_ids)
        self._texts.extend(texts)
        self._embeddings.extend(embeddings)
        self._metadatas.extend(metadatas)
        return new_ids

    async def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filter: dict | None = None,
    ) -> list[dict]:
        if not self._embeddings:
            return []

        query_vec = np.array(query_embedding).reshape(1, -1)
        doc_vecs = np.array(self._embeddings)
        similarities = cosine_similarity(query_vec, doc_vecs)[0]

        # Apply metadata filter if provided
        valid_indices = list(range(len(self._ids)))
        if filter:
            valid_indices = [
                i
                for i in valid_indices
                if all(self._metadatas[i].get(k) == v for k, v in filter.items())
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
                    "id": self._ids[original_idx],
                    "text": self._texts[original_idx],
                    "metadata": self._metadatas[original_idx],
                    "score": float(filtered_similarities[idx]),
                }
            )
        return results

    async def delete(self, ids: list[str]) -> bool:
        id_set = set(ids)
        keep_indices = [i for i, id_ in enumerate(self._ids) if id_ not in id_set]
        self._ids = [self._ids[i] for i in keep_indices]
        self._texts = [self._texts[i] for i in keep_indices]
        self._embeddings = [self._embeddings[i] for i in keep_indices]
        self._metadatas = [self._metadatas[i] for i in keep_indices]
        return True

    async def clear(self) -> bool:
        self._ids = []
        self._texts = []
        self._embeddings = []
        self._metadatas = []
        return True


class RedisVectorStore(BaseVectorStore):
    """Vector store using Redis Search for production use."""

    def __init__(
        self, redis_url: str = "redis://localhost:6379/1", index_name: str = "berunda_vectors"
    ):
        self.redis_url = redis_url
        self.index_name = index_name
        self._redis = None

    async def _get_redis(self):
        if self._redis is None:
            try:
                import redis.asyncio as aioredis

                self._redis = await aioredis.from_url(self.redis_url)
            except ImportError:
                raise RuntimeError("redis-py not installed. Install with: pip install redis")
        return self._redis

    async def add(
        self, texts: list[str], embeddings: list[list[float]], metadatas: list[dict]
    ) -> list[str]:
        import uuid

        import numpy as np

        r = await self._get_redis()
        ids = [str(uuid.uuid4()) for _ in texts]
        pipe = r.pipeline()
        for i, tid in enumerate(ids):
            key = f"vec:{self.index_name}:{tid}"
            vec_bytes = np.array(embeddings[i], dtype=np.float32).tobytes()
            pipe.hset(
                key,
                mapping={
                    "vector": vec_bytes,
                    "text": texts[i][:1000],
                    "metadata": str(metadatas[i]),
                },
            )
        await pipe.execute()
        return ids

    async def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filter: dict | None = None,
    ) -> list[dict]:
        try:
            import numpy as np

            from src.services.rag_service import cosine_similarity

            r = await self._get_redis()

            keys = await r.keys(f"vec:{self.index_name}:*")
            results = []
            for key in keys:
                data = await r.hgetall(key)
                if not data:
                    continue
                stored_vec = np.frombuffer(data[b"vector"], dtype=np.float32).tolist()
                score = cosine_similarity(query_embedding, stored_vec)
                if filter:
                    import json

                    try:
                        meta = json.loads(data.get(b"metadata", b"{}"))
                    except Exception:
                        meta = {}
                    if not all(meta.get(k) == v for k, v in filter.items()):
                        continue
                results.append(
                    {
                        "id": key.decode().split(":")[-1],
                        "text": data.get(b"text", b"").decode(),
                        "metadata": data.get(b"metadata", b"{}").decode(),
                        "score": score,
                    }
                )
            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:top_k]
        except Exception:
            return []

    async def delete(self, ids: list[str]) -> bool:
        r = await self._get_redis()
        keys = [f"vec:{self.index_name}:{tid}" for tid in ids]
        await r.delete(*keys)
        return True

    async def clear(self) -> bool:
        r = await self._get_redis()
        keys = await r.keys(f"vec:{self.index_name}:*")
        if keys:
            await r.delete(*keys)
        return True


class CatalystVectorStore(BaseVectorStore):
    """Zoho Catalyst NoSQL-based vector store (placeholder for production)."""

    async def add(
        self, texts: list[str], embeddings: list[list[float]], metadatas: list[dict]
    ) -> list[str]:
        raise NotImplementedError(
            "CatalystVectorStore not implemented — use InMemoryVectorStore for dev"
        )

    async def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filter: dict | None = None,
    ) -> list[dict]:
        raise NotImplementedError

    async def delete(self, ids: list[str]) -> bool:
        raise NotImplementedError

    async def clear(self) -> bool:
        raise NotImplementedError


def create_vector_store(store_type: str = "memory", **kwargs) -> BaseVectorStore:
    """Factory function to create vector stores."""
    if store_type == "memory":
        return InMemoryVectorStore()
    if store_type == "redis":
        return RedisVectorStore(**kwargs)
    if store_type == "catalyst":
        return CatalystVectorStore()
    raise ValueError(f"Unknown vector store type: {store_type}")
