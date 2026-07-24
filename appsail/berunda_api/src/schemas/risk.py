from __future__ import annotations

from datetime import datetime

from src.schemas.base import APIBase


class RiskScoreResponse(APIBase):
    RiskScoreID: int
    PersonEntityID: int
    Score: float
    ModelVersion: str | None = None
    FeaturesJSON: str | None = None
    ComputedAt: datetime | None = None


class RiskScoreQuery(APIBase):
    person_entity_id: int | None = None
    min_score: float | None = None
    max_score: float | None = None
    page: int = 1
    page_size: int = 20
