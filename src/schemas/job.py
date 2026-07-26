from __future__ import annotations

from datetime import datetime
from pydantic import Field
from src.schemas.base import APIBase


class BackgroundJobCreate(APIBase):
    JobType: str = Field(..., examples=["ai_extraction", "related_case_computation", "report_generation", "orphan_cleanup"])
    Payload: str | None = Field(None, examples=['{"fir_id": 1}'])
    IdempotencyKey: str | None = Field(None, examples=["job-20260726-001"])


class BackgroundJobResponse(APIBase):
    JobID: str
    JobType: str
    Payload: str | None = None
    IdempotencyKey: str | None = None
    RequestedByUserID: int | None = None
    Status: str = "queued"
    AttemptCount: int = 0
    MaxAttempts: int = 3
    ResultRef: str | None = None
    ErrorMessage: str | None = None
    CreatedAt: datetime | None = None
    StartedAt: datetime | None = None
    CompletedAt: datetime | None = None
