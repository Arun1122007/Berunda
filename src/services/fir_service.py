from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.models.src_models import (
    CaseMaster,
    InvOccuranceTime,
    Unit,
)
from src.schemas.fir import FIRCreate, FIRUpdate
from src.services.base import BaseService


class FIRService(BaseService):
    async def list_firs(
        self,
        page: int = 1,
        page_size: int = 20,
        district_id: int | None = None,
        police_station_id: int | None = None,
        status_id: int | None = None,
    ) -> tuple[list[CaseMaster], int]:
        cache_key = (
            f"fir:list:{page}:{page_size}:"
            f"{district_id}:{police_station_id}:{status_id}"
        )
        cached = await self._cache.get(cache_key)
        if cached is not None:
            ids, total = cached["ids"], cached["total"]
            if ids:
                result = await self.session.execute(
                    select(CaseMaster).where(CaseMaster.CaseMasterID.in_(ids))
                )
                items = list(result.scalars().all())
                id_order = {cid: i for i, cid in enumerate(ids)}
                items.sort(key=lambda x: id_order.get(x.CaseMasterID, 0))
            else:
                items = []
            return items, total

        query = select(CaseMaster)
        count_query = select(func.count(CaseMaster.CaseMasterID))

        if district_id is not None:
            query = query.where(
                CaseMaster.PoliceStationID.in_(
                    select(Unit.UnitID).where(Unit.DistrictID == district_id)
                )
            )
        if police_station_id is not None:
            query = query.where(CaseMaster.PoliceStationID == police_station_id)
        if status_id is not None:
            query = query.where(CaseMaster.CaseStatusID == status_id)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(CaseMaster.CaseMasterID.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        items = list(result.scalars().all())

        await self._cache.set(cache_key, {"ids": [c.CaseMasterID for c in items], "total": total})
        return items, total

    async def get_fir(self, case_master_id: int) -> CaseMaster | None:
        cache_key = f"fir:detail:{case_master_id}"
        cached = await self._cache.get(cache_key)
        if cached is not None:
            result = await self.session.execute(
                select(CaseMaster).where(CaseMaster.CaseMasterID == case_master_id)
            )
            return result.scalar_one_or_none()

        query = (
            select(CaseMaster)
            .where(CaseMaster.CaseMasterID == case_master_id)
            .options(
                selectinload(CaseMaster.occurrence),
                selectinload(CaseMaster.complainants),
                selectinload(CaseMaster.victims),
                selectinload(CaseMaster.accused),
                selectinload(CaseMaster.act_sections),
            )
        )
        result = await self.session.execute(query)
        case = result.scalar_one_or_none()
        if case is not None:
            await self._cache.set(cache_key, {"id": case_master_id})
        return case

    async def create_fir(self, data: FIRCreate) -> CaseMaster:
        case = CaseMaster(
            **data.model_dump(exclude={"BriefFacts", "Latitude", "Longitude"}, exclude_none=True)
        )
        self.session.add(case)
        await self.session.flush()

        if any([data.BriefFacts, data.Latitude is not None, data.Longitude is not None]):
            occurrence = InvOccuranceTime(
                CaseMasterID=case.CaseMasterID,
                BriefFacts=data.BriefFacts,
                Latitude=data.Latitude,
                Longitude=data.Longitude,
            )
            self.session.add(occurrence)

        await self.session.commit()
        await self.session.refresh(case)
        await self._cache.invalidate("fir:list:*")
        return case

    async def update_fir(self, case_master_id: int, data: FIRUpdate) -> CaseMaster | None:
        case = await self.get_fir(case_master_id)
        if case is None:
            return None
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(case, key, value)
        await self.session.commit()
        await self.session.refresh(case)
        await self._cache.invalidate("fir:list:*")
        await self._cache.invalidate(f"fir:detail:{case_master_id}")
        return case

    async def delete_fir(self, case_master_id: int) -> bool:
        case = await self.session.get(CaseMaster, case_master_id)
        if case is None:
            return False
        await self.session.delete(case)
        await self.session.commit()
        await self._cache.invalidate("fir:list:*")
        await self._cache.invalidate(f"fir:detail:{case_master_id}")
        return True
