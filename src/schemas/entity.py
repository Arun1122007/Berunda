from __future__ import annotations

from datetime import datetime

from src.schemas.base import APIBase


class PersonEntityResponse(APIBase):
    PersonEntityID: int
    CanonicalName: str
    DOB: datetime | None = None
    Gender: str | None = None
    PrimaryDistrictID: int | None = None
    RiskScoreID: int | None = None
    CreatedAt: datetime | None = None
    UpdatedAt: datetime | None = None


class PersonEntityLinkResponse(APIBase):
    PersonEntityLinkID: int
    PersonEntityID: int
    SourceTable: str | None = None
    CaseMasterID: int | None = None
    Confidence: float | None = None
    IsReviewed: int | None = None


class EntitySearchQuery(APIBase):
    name: str | None = None
    district_id: int | None = None
    min_confidence: float | None = None
    page: int = 1
    page_size: int = 20


class EntitySearchResponse(APIBase):
    items: list[PersonEntityResponse]
    total: int
    page: int
    page_size: int


class EntityMergeRequest(APIBase):
    source_entity_id: int
    target_entity_id: int
    reviewed_by: int | None = None
