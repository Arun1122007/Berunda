from __future__ import annotations

from pydantic import Field

from src.schemas.base import APIBase


class RAGQuery(APIBase):
    query: str = Field(..., min_length=1)
    top_k: int = 5
    district_id: int | None = None
    crime_head_id: int | None = None


class RAGCitation(APIBase):
    CaseMasterID: int
    ChunkText: str
    Relevance: float
    CrimeNo: str | None = None


class RAGResponse(APIBase):
    answer: str
    citations: list[RAGCitation]
    confidence: float
    processing_time_ms: float
