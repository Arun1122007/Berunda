"""Pydantic schemas for AI Assistant, Extraction, and Suggestion Lifecycle."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AISuggestionItem(BaseModel):
    field: str
    suggested_value: Any
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    reasoning: str | None = None


class AISuggestionPayload(BaseModel):
    suggested_crime_head: str | None = None
    suggested_act_sections: list[dict[str, str]] = []
    extracted_entities: list[dict[str, str]] = []
    mo_pattern: str | None = None
    confidence_score: float = Field(default=0.85, ge=0.0, le=1.0)
    summary: str | None = None
    items: list[AISuggestionItem] = []


class AIExtractionResponse(BaseModel):
    ExtractionID: int
    CaseMasterID: int
    Status: str
    ModelUsed: str | None = None
    RawJSON: str | None = None
    ReviewedBy: int | None = None
    CreatedAt: datetime | None = None
    UpdatedAt: datetime | None = None

    class Config:
        from_attributes = True


class AIExtractionReviewRequest(BaseModel):
    comments: str | None = None
