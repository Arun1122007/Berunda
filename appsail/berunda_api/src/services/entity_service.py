from __future__ import annotations

from sqlalchemy import func, or_, select

from src.models.int_models import PersonEntity, PersonEntityLink
from src.schemas.entity import EntitySearchQuery
from src.services.base import BaseService


class EntityService(BaseService):
    async def search_entities(self, query: EntitySearchQuery) -> tuple[list[PersonEntity], int]:
        stmt = select(PersonEntity)
        count_stmt = select(func.count(PersonEntity.PersonEntityID))

        if query.name:
            name_filter = or_(
                PersonEntity.CanonicalName.ilike(f"%{query.name}%"),
            )
            stmt = stmt.where(name_filter)
            count_stmt = count_stmt.where(name_filter)
        if query.district_id is not None:
            stmt = stmt.where(PersonEntity.PrimaryDistrictID == query.district_id)
            count_stmt = count_stmt.where(PersonEntity.PrimaryDistrictID == query.district_id)

        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = stmt.order_by(PersonEntity.CanonicalName)
        stmt = stmt.offset((query.page - 1) * query.page_size).limit(query.page_size)

        result = await self.session.execute(stmt)
        items = list(result.scalars().all())
        return items, total

    async def get_entity(self, entity_id: int) -> PersonEntity | None:
        result = await self.session.execute(
            select(PersonEntity).where(PersonEntity.PersonEntityID == entity_id)
        )
        return result.scalar_one_or_none()

    async def get_entity_links(self, entity_id: int) -> list[PersonEntityLink]:
        result = await self.session.execute(
            select(PersonEntityLink).where(PersonEntityLink.PersonEntityID == entity_id)
        )
        return list(result.scalars().all())

    async def merge_entities(
        self, source_id: int, target_id: int, reviewed_by: int | None = None
    ) -> PersonEntity | None:
        source = await self.get_entity(source_id)
        target = await self.get_entity(target_id)
        if source is None or target is None:
            return None

        links = await self.get_entity_links(source_id)
        for link in links:
            link.PersonEntityID = target_id
            link.IsReviewed = 1
            link.ReviewedBy = reviewed_by

        await self.session.delete(source)
        await self.session.commit()
        await self.session.refresh(target)
        return target
