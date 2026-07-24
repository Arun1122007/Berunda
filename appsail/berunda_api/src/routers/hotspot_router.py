from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
from src.schemas.hotspot import HotspotLayerResponse
from src.services.hotspot_service import HotspotService

router = APIRouter(prefix="/api/v1/hotspots", tags=["Hotspots"])


@router.get("", response_model=list[HotspotLayerResponse])
async def get_hotspots(
    district_id: int | None = Query(None),
    week_start: date | None = Query(None),
    week_end: date | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    if user.get("role") != "admin":
        district_id = user.get("district_id")

    service = HotspotService(session)
    items, total = await service.get_hotspots(
        district_id=district_id,
        week_start=week_start,
        week_end=week_end,
        page=page,
        page_size=page_size,
    )
    return [HotspotLayerResponse.model_validate(h) for h in items]
