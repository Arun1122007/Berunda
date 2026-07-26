from datetime import datetime

from pydantic import Field

from src.schemas.base import APIBase


class ReportRequestCreate(APIBase):
    ReportType: str = Field(..., examples=["fir_summary", "investigation_progress", "evidence_inventory", "case_timeline"])
    Parameters: str | None = Field(None, examples=['{"case_master_id": 1, "include_evidence": true}'])
    FileFormat: str = Field("pdf", examples=["pdf", "csv", "json"])


class ReportRequestResponse(APIBase):
    ReportID: str
    RequestedByUserID: int
    ReportType: str
    Parameters: str | None = None
    Status: str
    StorageObjectRef: str | None = None
    FileFormat: str | None = None
    ErrorMessage: str | None = None
    CreatedAt: datetime | None = None
    CompletedAt: datetime | None = None
    ExpiresAt: datetime | None = None


class ReportContent(APIBase):
    report_id: str
    report_type: str
    generated_at: str
    generated_by: int
    content: dict
    is_synthetic_data: bool = True
