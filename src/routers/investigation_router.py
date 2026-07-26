from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.dependencies import get_fir_repo
from src.middleware.auth import get_current_user, require_role
from src.repositories.core import FIRRepository
from src.schemas.investigation import (
    CaseAssignmentCreate,
    CaseAssignmentResponse,
    CaseStatusUpdate,
    InvestigationNoteCreate,
    InvestigationNoteResponse,
    SupervisorReviewCreate,
    SupervisorReviewResponse,
    TimelineEvent,
)
from src.services.fir_service import FIRService

router = APIRouter(prefix="/api/v1/fir", tags=["Investigation"])


@router.post("/{case_master_id}/notes", response_model=InvestigationNoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    case_master_id: int,
    data: InvestigationNoteCreate,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "officer"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id")
    try:
        note = await service.create_note(
            case_master_id=case_master_id,
            author_id=user_id,
            content=data.Content,
            note_type=data.NoteType,
            visibility=data.Visibility,
        )
        return note
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{case_master_id}/notes", response_model=list[InvestigationNoteResponse])
async def list_notes(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    return await service.list_notes(case_master_id)


@router.post("/{case_master_id}/assignments", response_model=CaseAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def assign_officer(
    case_master_id: int,
    data: CaseAssignmentCreate,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "supervisor"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id")
    try:
        result = await service.assign_officer(
            case_master_id=case_master_id,
            assigned_officer_id=data.AssignedOfficerID,
            assigned_by_user_id=user_id,
            reason=data.AssignmentReason,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{case_master_id}/assignments", response_model=list[CaseAssignmentResponse])
async def list_assignments(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    return await service.list_assignments(case_master_id)


@router.get("/{case_master_id}/assignment/active", response_model=CaseAssignmentResponse | None)
async def get_active_assignment(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    return await service.get_active_assignment(case_master_id)


@router.put("/{case_master_id}/status", response_model=dict)
async def update_case_status(
    case_master_id: int,
    data: CaseStatusUpdate,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "officer", "supervisor"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id")
    try:
        return await service.update_case_status(
            case_master_id=case_master_id,
            new_status_id=data.CaseStatusID,
            user_id=user_id,
            reason=data.Reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{case_master_id}/timeline", response_model=list[TimelineEvent])
async def get_timeline(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    return await service.get_timeline(case_master_id)


@router.post("/{case_master_id}/reviews", response_model=SupervisorReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    case_master_id: int,
    data: SupervisorReviewCreate,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "supervisor"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id")
    try:
        result = await service.create_review(
            case_master_id=case_master_id,
            supervisor_id=user_id,
            review_type=data.ReviewType,
            status=data.Status,
            comments=data.Comments,
            action_requested=data.ActionRequested,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{case_master_id}/reviews", response_model=list[SupervisorReviewResponse])
async def list_reviews(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    return await service.list_reviews(case_master_id)
