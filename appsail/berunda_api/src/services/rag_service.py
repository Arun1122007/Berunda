"""Retrieval-Augmented Generation (RAG) Service."""

from __future__ import annotations

import json
import time

import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.int_models import RAGCorpusChunk
from src.models.src_models import CaseMaster, InvOccuranceTime
from src.schemas.rag import RAGCitation, RAGQuery, RAGResponse
from src.services.base import BaseService
from src.services.embedding_service import EmbeddingService


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (norm1 * norm2))


class RAGService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.embedding_service = EmbeddingService(session)

    async def _populate_chunks(self):
        """Populate database with embeddings for cases if missing."""
        existing = await self.session.execute(select(RAGCorpusChunk).limit(1))
        if existing.scalar_one_or_none():
            return

        cases = await self.session.execute(select(CaseMaster).join(InvOccuranceTime, isouter=True))
        chunks = []
        for case in cases.scalars().all():
            if not case.occurrence or not case.occurrence.BriefFacts:
                continue

            text = f"Case {case.CrimeNo}: {case.occurrence.BriefFacts}"

            chunks.append(
                {
                    "CaseMasterID": case.CaseMasterID,
                    "ChunkIndex": 0,
                    "ChunkText": text,
                    "TenantDistrictID": None,  # Add proper district mapping if needed
                }
            )

            # Batch process to avoid large payloads
            if len(chunks) >= 50:
                await self.embedding_service.store_chunks(chunks)
                chunks = []

        if chunks:
            await self.embedding_service.store_chunks(chunks)

    async def query(self, rag_query: RAGQuery, user: dict | None = None) -> RAGResponse:
        start = time.time()

        # Ensure chunks exist (one-time setup for MVP)
        await self._populate_chunks()

        # Generate embedding for the query
        query_embeddings = await self.embedding_service.generate_embeddings([rag_query.query])
        if not query_embeddings:
            elapsed = (time.time() - start) * 1000
            return RAGResponse(
                answer="Failed to generate embeddings for query.",
                citations=[],
                confidence=0.0,
                processing_time_ms=round(elapsed, 2),
            )

        query_vec = query_embeddings[0]

        # Fetch candidate chunks
        stmt = select(
            RAGCorpusChunk.ChunkID,
            RAGCorpusChunk.ChunkText,
            RAGCorpusChunk.CaseMasterID,
            RAGCorpusChunk.Embedding,
            CaseMaster.CrimeNo,
        ).outerjoin(CaseMaster, RAGCorpusChunk.CaseMasterID == CaseMaster.CaseMasterID)

        if user and user.get("role") != "admin":
            rag_query.district_id = user.get("district_id")

        if rag_query.district_id is not None:
            stmt = stmt.where(RAGCorpusChunk.TenantDistrictID == rag_query.district_id)

        stmt = stmt.limit(100)  # Hardcode limit to optimize tokens and memory before pgvector

        result = await self.session.execute(stmt)
        rows = list(result.all())

        if not rows:
            elapsed = (time.time() - start) * 1000
            return RAGResponse(
                answer="No case data available to search. Please ensure FIR records exist.",
                citations=[],
                confidence=0.0,
                processing_time_ms=round(elapsed, 2),
            )

        citations = []
        for row in rows:
            if not row.Embedding:
                continue

            try:
                chunk_vec = json.loads(row.Embedding)
                score = cosine_similarity(query_vec, chunk_vec)

                if score >= 0.2:  # Threshold for relevance
                    citations.append(
                        RAGCitation(
                            CaseMasterID=row.CaseMasterID or 0,
                            ChunkText=row.ChunkText[:500] if row.ChunkText else "",
                            Relevance=score,
                            CrimeNo=row.CrimeNo,
                        )
                    )
            except (json.JSONDecodeError, ValueError, TypeError):
                continue

        # Sort by relevance
        citations.sort(key=lambda c: c.Relevance, reverse=True)
        top_citations = citations[: rag_query.top_k]

        if top_citations:
            top_texts = [c.ChunkText for c in top_citations[:3]]
            context = " ".join(top_texts)
            answer = (
                f"Based on {len(top_citations)} relevant case record(s), "
                f"here is what I found regarding your query.\n\n"
                f"Context: {context[:600]}..."
            )
            confidence = float(np.mean([c.Relevance for c in top_citations]))
        else:
            answer = (
                "I couldn't find specific cases matching your query. "
                "Try rephrasing or using different keywords."
            )
            confidence = 0.0

        elapsed = (time.time() - start) * 1000
        return RAGResponse(
            answer=answer,
            citations=top_citations,
            confidence=round(confidence, 4),
            processing_time_ms=round(elapsed, 2),
        )
