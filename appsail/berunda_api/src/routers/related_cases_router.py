from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import get_fir_repo
from src.middleware.auth import get_current_user, require_role
from src.repositories.core import FIRRepository
from src.schemas.related_case import RelatedCaseReviewRequest as RelatedCaseReview
from src.schemas.related_case import RelatedCaseSuggestionResponse
from src.services.fir_service import FIRService

router = APIRouter(prefix="/api/v1/fir", tags=["Related Cases"])


@router.post("/{case_master_id}/related-cases/generate", response_model=list[RelatedCaseSuggestionResponse])
async def generate_related_cases(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "officer", "supervisor", "analyst"])),
):
    service = FIRService(repo)
    try:
        return await service.generate_related_cases(case_master_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{case_master_id}/related-cases", response_model=list[RelatedCaseSuggestionResponse])
async def list_related_cases(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    return await service.list_related_cases(case_master_id)


@router.put("/related-cases/{suggestion_id}/review", response_model=RelatedCaseSuggestionResponse)
async def review_related_case(
    suggestion_id: int,
    data: RelatedCaseReview,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "officer", "supervisor"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id")
    try:
        return await service.review_related_case(
            suggestion_id=suggestion_id,
            review_status=data.ReviewStatus,
            reviewed_by_user_id=user_id,
            review_reason=data.ReviewReason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
