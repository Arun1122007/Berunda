from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
from src.schemas.risk import RiskScoreResponse
from src.services.risk_service import RiskService

router = APIRouter(prefix="/api/v1/risk", tags=["Risk"])


@router.get("", response_model=list[RiskScoreResponse])
async def get_risk_scores(
    person_entity_id: int | None = Query(None),
    min_score: float | None = Query(None, ge=0.0, le=1.0),
    max_score: float | None = Query(None, ge=0.0, le=1.0),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = RiskService(session)
    items, _total = await service.get_scores(
        person_entity_id=person_entity_id,
        min_score=min_score,
        max_score=max_score,
        page=page,
        page_size=page_size,
    )
    return [RiskScoreResponse.model_validate(r) for r in items]


@router.post("/compute/{person_entity_id}", response_model=RiskScoreResponse)
async def compute_risk(
    person_entity_id: int,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = RiskService(session)
    score = await service.compute_risk_score(person_entity_id)
    return RiskScoreResponse.model_validate(score)
