from __future__ import annotations

from fastapi import APIRouter, Depends

from src.dependencies import get_fairness_repo
from src.middleware.auth import get_current_user
from src.repositories.core import FairnessRepository
from src.schemas.fairness import FairnessCheckRequest, FairnessCheckResponse
from src.services.fairness_service import FairnessService

router = APIRouter(prefix="/api/v1/fairness", tags=["Fairness"])


@router.post("/audit", response_model=FairnessCheckResponse)
async def run_fairness_audit(
    data: FairnessCheckRequest,
    repo: FairnessRepository = Depends(get_fairness_repo),
    user: dict = Depends(get_current_user),
):
    service = FairnessService(repo=repo)
    return await service.run_feature_audit(user.get("name", "system"))
