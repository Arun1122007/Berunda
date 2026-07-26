from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from src.dependencies import get_socioeconomic_repo
from src.middleware.auth import get_current_user
from src.repositories.core import SocioeconomicRepository
from src.schemas.socioeconomic import SocioeconomicRecord
from src.services.socioeconomic_service import SocioeconomicService

router = APIRouter(prefix="/api/v1/socioeconomic", tags=["Socioeconomic"])


@router.get("", response_model=list[SocioeconomicRecord])
async def get_socioeconomic_indicators(
    district_id: int | None = Query(None),
    sort_by: str = Query("crime_rate_per_100k"),
    order: str = Query("desc"),
    repo: SocioeconomicRepository = Depends(get_socioeconomic_repo),
    user: dict = Depends(get_current_user),
):
    service = SocioeconomicService(repo=repo)
    items = await service.get_indicators(
        district_id=district_id,
        sort_by=sort_by,
        order=order,
    )
    return [SocioeconomicRecord.model_validate(item) for item in items]
