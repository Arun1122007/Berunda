from datetime import datetime
from typing import Literal

from pydantic import Field

from src.schemas.base import APIBase


class RelatedCaseSuggestionResponse(APIBase):
    SuggestionID: int
    SourceFIRID: int
    CandidateFIRID: int
    ConfidenceScore: float
    SupportingSignals: str
    Explanation: str
    ModelVersion: str | None = None
    ReviewStatus: str | None = None
    ReviewedByUserID: int | None = None
    ReviewReason: str | None = None
    ReviewedAt: datetime | None = None
    CreatedAt: datetime | None = None

    CandidateCrimeNo: str | None = None
    CandidateStatusID: int | None = None


class RelatedCaseReview(APIBase):
    ReviewStatus: Literal["accepted", "rejected"] = Field(..., examples=["accepted", "rejected"])
    ReviewReason: str | None = Field(None, max_length=500, examples=["Same vehicle number plate reported in both cases"])


RelatedCaseReviewRequest = RelatedCaseReview
