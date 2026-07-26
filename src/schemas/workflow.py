from __future__ import annotations

from datetime import datetime
from pydantic import Field
from src.schemas.base import APIBase


class CaseAssignmentCreate(APIBase):
    AssignedOfficerID: int = Field(..., examples=[101])
    AssignmentReason: str | None = Field(None, examples=["Assigned for specialized cyber investigation."])


class CaseAssignmentResponse(APIBase):
    AssignmentID: int
    CaseMasterID: int
    AssignedOfficerID: int
    AssignedByUserID: int
    AssignmentReason: str | None = None
    Status: str = "active"
    AssignedAt: datetime | None = None
    EndedAt: datetime | None = None


class InvestigationNoteCreate(APIBase):
    NoteType: str = Field("general", examples=["witness_statement"])
    Content: str = Field(..., examples=["Witness stated observing a suspicious blue van near the crime scene around 22:00."])
    IsAmendment: bool = Field(False)
    OriginalNoteID: int | None = Field(None)
    Visibility: str = Field("station", examples=["station", "supervisor_only"])


class InvestigationNoteResponse(APIBase):
    NoteID: int
    CaseMasterID: int
    AuthorID: int
    NoteType: str
    Content: str
    IsAmendment: bool
    OriginalNoteID: int | None = None
    Visibility: str
    CreatedAt: datetime | None = None
    UpdatedAt: datetime | None = None


class FIRStatusTransitionRequest(APIBase):
    TargetStatus: str = Field(..., examples=["under_investigation", "review_pending", "closed"])
    Reason: str | None = Field(None, examples=["Preliminary inquiry completed, initiating formal investigation."])


class FIRStatusTransitionResponse(APIBase):
    CaseMasterID: int
    PreviousStatus: str | None = None
    CurrentStatus: str
    TransitionedAt: datetime | None = None
    TransitionedBy: int | None = None


class SupervisorReviewCreate(APIBase):
    ReviewType: str = Field("periodic", examples=["periodic", "status_change", "correction_request"])
    Status: str = Field("approved", examples=["approved", "correction_requested", "rejected"])
    Comments: str | None = Field(None, examples=["Investigation procedure verified. Ensure witness statements are signed."])
    ActionRequested: str | None = Field(None, examples=["Obtain CCTV footage from neighboring shop."])


class SupervisorReviewResponse(APIBase):
    ReviewID: int
    CaseMasterID: int
    SupervisorID: int
    ReviewType: str
    Status: str
    Comments: str | None = None
    ActionRequested: str | None = None
    ReviewedAt: datetime | None = None
