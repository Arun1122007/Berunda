from __future__ import annotations

from datetime import date

from sqlalchemy import func, select

from src.models.int_models import HotspotLayer
from src.services.base import BaseService


class HotspotService(BaseService):
    async def get_hotspots(
        self,
        district_id: int | None = None,
        week_start: date | None = None,
        week_end: date | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[HotspotLayer], int]:
        query = select(HotspotLayer)
        count_query = select(func.count(HotspotLayer.HotspotLayerID))

        if district_id is not None:
            query = query.where(HotspotLayer.DistrictID == district_id)
            count_query = count_query.where(HotspotLayer.DistrictID == district_id)
        if week_start is not None:
            query = query.where(HotspotLayer.WeekStart >= week_start)
            count_query = count_query.where(HotspotLayer.WeekStart >= week_start)
        if week_end is not None:
            query = query.where(HotspotLayer.WeekEnd <= week_end)
            count_query = count_query.where(HotspotLayer.WeekEnd <= week_end)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(HotspotLayer.DensityScore.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        items = list(result.scalars().all())
        return items, total
