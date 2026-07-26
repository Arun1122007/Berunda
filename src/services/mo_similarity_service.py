"""Modus Operandi (MO) Similarity Service for Phase 3 Enterprise Scale.

Computes vector embedding similarity across FIR brief facts to discover linked crimes,
serial offenders, and pattern clusters across police districts.
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.embedding_provider import OpenAIEmbeddingProvider
from src.repositories.vector_repo import SQLiteVectorStore
from src.services.base import BaseService

logger = logging.getLogger("berunda.mo_similarity")


class MOSimilarityService(BaseService):
    """Service for pattern matching and discovering serial crimes via text embeddings."""

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.vector_store = SQLiteVectorStore(session)
        self.provider = OpenAIEmbeddingProvider()

    def _jaccard_word_similarity(self, text_a: str, text_b: str) -> float:
        """Fallback keyword similarity when vector embeddings are unindexed."""
        words_a = set(text_a.lower().replace(".", "").replace(",", "").split())
        words_b = set(text_b.lower().replace(".", "").replace(",", "").split())
        if not words_a or not words_b:
            return 0.0
        intersection = words_a.intersection(words_b)
        union = words_a.union(words_b)
        return len(intersection) / len(union) if union else 0.0

    async def find_similar_cases(
        self, case_id: int, top_k: int = 5, min_score: float = 0.4
    ) -> list[dict[str, Any]]:
        """Find cases with similar Modus Operandi (MO) or incident brief facts via vector search."""
        logger.info(f"Searching for similar MO cases for CaseMasterID #{case_id}...")

        # 1. Fetch target case vector from VectorStore
        target_record = await self.vector_store.fetch([f"FIR_{case_id}"])
        if not target_record:
            logger.warning(f"Target case {case_id} is not embedded in the vector store.")
            return []

        target_vector = target_record[0]["vector"]

        # 2. Search against vector store
        # We don't apply district filters here assuming similarities can span the state
        # But we DO exclude the target case itself via post-filtering.
        candidates = await self.vector_store.search(target_vector, filters={}, limit=top_k + 1)

        results = []
        for cand in candidates:
            cand_fir_id = int(cand["metadata"].get("fir_id", 0))
            if cand_fir_id == case_id:
                continue

            score = cand["score"]
            if score >= min_score:
                results.append(
                    {
                        "caseId": cand_fir_id,
                        "crimeNo": cand["metadata"].get("official_fir_number", ""),
                        "similarityScore": round(score, 4),
                        "matchType": "SERIAL_MO_PATTERN" if score > 0.80 else "SIMILAR_CIRCUMSTANCES",
                        "metadata": cand["metadata"]
                    }
                )

        results.sort(key=lambda x: x["similarityScore"], reverse=True)
        return results[:top_k]
