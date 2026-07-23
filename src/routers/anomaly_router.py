from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
from src.schemas.anomaly import AnomalyAlertResponse
from src.services.anomaly_service import AnomalyService

router = APIRouter(prefix="/api/v1/anomalies", tags=["Anomalies"])


@router.get("", response_model=list[AnomalyAlertResponse])
async def get_anomalies(
    district_id: int | None = Query(None),
    alert_only: bool = Query(True),
    week_start: date | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    if user.get("role") != "admin":
        district_id = user.get("district_id")

    service = AnomalyService(session)
    items, total = await service.get_alerts(
        district_id=district_id,
        alert_only=alert_only,
        week_start=week_start,
        page=page,
        page_size=page_size,
    )
    return [AnomalyAlertResponse.model_validate(a) for a in items]
