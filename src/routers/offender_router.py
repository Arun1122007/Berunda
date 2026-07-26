from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
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
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = OffenderService(session)
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
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = OffenderService(session)
    profile = await service.get_offender_profile(offender_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Offender dossier not found")
    return OffenderProfileResponse.model_validate(profile)
