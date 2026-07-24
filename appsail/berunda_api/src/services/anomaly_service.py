from __future__ import annotations

from datetime import date

from sqlalchemy import func, select

from src.models.int_models import AnomalyAlert
from src.services.base import BaseService


class AnomalyService(BaseService):
    async def get_alerts(
        self,
        district_id: int | None = None,
        alert_only: bool = True,
        week_start: date | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[AnomalyAlert], int]:
        query = select(AnomalyAlert)
        count_query = select(func.count(AnomalyAlert.AnomalyAlertID))

        if district_id is not None:
            query = query.where(AnomalyAlert.DistrictID == district_id)
            count_query = count_query.where(AnomalyAlert.DistrictID == district_id)
        if alert_only:
            query = query.where(AnomalyAlert.AlertLevel == 1)
            count_query = count_query.where(AnomalyAlert.AlertLevel == 1)
        if week_start is not None:
            query = query.where(AnomalyAlert.WeekStart >= week_start)
            count_query = count_query.where(AnomalyAlert.WeekStart >= week_start)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(AnomalyAlert.ZScore.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        items = list(result.scalars().all())
        return items, total
