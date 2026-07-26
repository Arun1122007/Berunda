from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from src.dependencies import get_offender_repo
from src.middleware.auth import get_current_user
from src.repositories.core import OffenderRepository
from src.schemas.offender import OffenderProfileResponse, OffenderSummaryResponse
from src.services.offender_service import OffenderService

router = APIRouter(prefix="/api/v1/offenders", tags=["Offenders"])


@router.get("", response_model=list[OffenderSummaryResponse])
async def get_offenders(
    search: str | None = Query(None),
    min_cases: int = Query(1, ge=1),
    jurisdiction: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    repo: OffenderRepository = Depends(get_offender_repo),
    user: dict = Depends(get_current_user),
):
    service = OffenderService(repo=repo)
    items, _total = await service.get_offenders(
        search=search,
        min_cases=min_cases,
        jurisdiction=jurisdiction,
        page=page,
        page_size=page_size,
    )
    return [OffenderSummaryResponse.model_validate(o) for o in items]


@router.get("/{offender_id}", response_model=OffenderProfileResponse)
async def get_offender_profile(
    offender_id: int,
    repo: OffenderRepository = Depends(get_offender_repo),
    user: dict = Depends(get_current_user),
):
    service = OffenderService(repo=repo)
    profile = await service.get_offender_profile(offender_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Offender dossier not found")
    return OffenderProfileResponse.model_validate(profile)
