from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
from src.schemas.fairness import FairnessCheckRequest, FairnessCheckResponse
from src.services.fairness_service import FairnessService

router = APIRouter(prefix="/api/v1/fairness", tags=["Fairness"])


@router.post("/audit", response_model=FairnessCheckResponse)
async def run_fairness_audit(
    data: FairnessCheckRequest,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = FairnessService(session)
    return await service.run_feature_audit(user.get("name", "system"))
