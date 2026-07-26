from __future__ import annotations

import logging

from src.ai.embedding_provider import OpenAIEmbeddingProvider
from src.ai.query_parser import QueryParser
from src.repositories.vector_repo import SQLiteVectorStore
from src.services.base import BaseService

logger = logging.getLogger("berunda.search")


class SearchService(BaseService):
    """Semantic and Hybrid Search Service."""

    def __init__(self, session, repo=None):
        super().__init__(session, repo)
        self.embedding_provider = OpenAIEmbeddingProvider()
        self.vector_store = SQLiteVectorStore(session)
        self.query_parser = QueryParser()

    async def search_hybrid(self, query: str, user: dict, filters: dict | None = None, page_size: int = 20) -> dict:
        """Execute a hybrid search combining keyword matching, metadata filters, and semantic vector similarity."""
        # 1. Scope Enforcement (RBAC)
        base_filters = filters or {}
        role = user.get("role")
        if role == "citizen":
            raise PermissionError("Citizens are restricted to accessing their own FIRs directly.")
        elif role in ["officer", "supervisor"]:
            district_id = user.get("district_id")
            if district_id:
                base_filters["district_id"] = str(district_id)

        # 2. Query Understanding
        parsed_query = self.query_parser.parse(query)
        semantic_text = parsed_query["semantic_text"]

        # Merge parsed filters with requested filters
        for k, v in parsed_query["filters"].items():
            if k not in base_filters:
                base_filters[k] = v

        # 3. Vector Embeddings
        try:
            query_vector = await self.embedding_provider.create_embedding(semantic_text)
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            raise RuntimeError("SEARCH_PROVIDER_TIMEOUT")

        if not query_vector:
            return {"items": [], "total": 0, "message": "Failed to generate query embedding."}

        # 4. Semantic Search (with base_filters acting as metadata filters)
        results = await self.vector_store.search(query_vector, filters=base_filters, limit=page_size)

        # 5. Format Output
        output = []
        for r in results:
            # Rehydrate from DB if necessary or just return metadata snippet
            meta = r["metadata"]
            output.append({
                "fir_id": meta.get("fir_id"),
                "official_fir_number": meta.get("official_fir_number"),
                "crime_category": meta.get("crime_category"),
                "district": meta.get("district_id"),
                "score": round(r["score"], 4),
                "match_type": "HYBRID",
                "synthetic_data": meta.get("synthetic_data", True),
                "safe_snippet": "Matched based on authorized semantic narrative."
            })

        return {
            "query": query,
            "interpreted_filters": parsed_query["filters"],
            "results": output,
            "pagination": {"page": 1, "page_size": page_size, "total_visible_results": len(output)}
        }
