from datetime import datetime

from pydantic import Field

from src.schemas.base import APIBase


class InvestigationNoteCreate(APIBase):
    Content: str = Field(..., min_length=1, max_length=10000, examples=["Visited the crime scene. Collected fingerprints from the rear door."])
    NoteType: str = Field("general", examples=["general", "witness_statement", "forensic", "field_visit"])
    Visibility: str = Field("station", examples=["station", "supervisor", "private"])


class InvestigationNoteResponse(APIBase):
    NoteID: int
    CaseMasterID: int
    AuthorID: int
    NoteType: str | None = None
    Content: str
    IsAmendment: bool = False
    OriginalNoteID: int | None = None
    Visibility: str | None = None
    CreatedAt: datetime | None = None
    UpdatedAt: datetime | None = None


class CaseAssignmentCreate(APIBase):
    AssignedOfficerID: int = Field(..., examples=[101])
    AssignmentReason: str | None = Field(None, max_length=500, examples=["Primary investigating officer assigned"])


class CaseAssignmentResponse(APIBase):
    AssignmentID: int
    CaseMasterID: int
    AssignedOfficerID: int
    AssignedByUserID: int
    AssignmentReason: str | None = None
    Status: str | None = None
    AssignedAt: datetime | None = None
    EndedAt: datetime | None = None


class CaseStatusUpdate(APIBase):
    CaseStatusID: int = Field(..., ge=1, le=20, examples=[2])
    Reason: str | None = Field(None, max_length=500)


class SupervisorReviewCreate(APIBase):
    ReviewType: str = Field("periodic", examples=["periodic", "evidence_review", "progress_review"])
    Status: str = Field("pending", examples=["pending", "approved", "changes_requested"])
    Comments: str | None = Field(None, max_length=5000)
    ActionRequested: str | None = Field(None, max_length=500)


class SupervisorReviewResponse(APIBase):
    ReviewID: int
    CaseMasterID: int
    SupervisorID: int
    ReviewType: str | None = None
    Status: str | None = None
    Comments: str | None = None
    ActionRequested: str | None = None
    ReviewedAt: datetime | None = None


class TimelineEvent(APIBase):
    type: str
    timestamp: datetime | str | None = None
    description: str | None = None
    note_id: int | None = None
    assignment_id: int | None = None
    review_id: int | None = None
