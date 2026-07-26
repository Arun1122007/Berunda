from datetime import datetime

from pydantic import Field

from src.schemas.base import APIBase


class EvidenceMetadata(APIBase):
    EvidenceID: int
    CaseMasterID: int
    EvidenceType: str | None = None
    Description: str | None = None
    StoragePath: str | None = None
    CollectedAt: datetime | None = None
    CollectedBy: str | None = None
    Source: str | None = None
    Location: str | None = None
    Checksum: str | None = None
    FileType: str | None = None
    FileSize: int | None = None
    Status: str | None = None
    Sensitivity: str | None = None
    CreatedAt: datetime | None = None
    UpdatedAt: datetime | None = None


class EvidenceStatusUpdate(APIBase):
    Status: str = Field(..., examples=["available", "under_review", "restricted", "archived"])
