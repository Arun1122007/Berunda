from __future__ import annotations

from src.repositories.core import EntityRepository
from src.schemas.entity import EntitySearchQuery
from src.services.base import BaseService


class EntityService(BaseService):
    def __init__(self, repo: EntityRepository):
        super().__init__()
        self.repo = repo

    async def search_entities(self, query: EntitySearchQuery):
        cache_key = (
            f"entity:search:{query.name}:{query.district_id}:"
            f"{query.page}:{query.page_size}"
        )
        cached = await self._cache.get(cache_key)
        if cached is not None:
            ids, total = cached["ids"], cached["total"]
            if ids:
                items = []
                for eid in ids:
                    entity = await self.repo.get_entity(eid)
                    if entity:
                        items.append(entity)
            else:
                items = []
            return items, total

        items, total = await self.repo.search_entities(
            name=query.name,
            district_id=query.district_id,
            page=query.page,
            page_size=query.page_size,
        )

        await self._cache.set(
            cache_key, {"ids": [e.PersonEntityID for e in items], "total": total}
        )
        return items, total

    async def get_entity(self, entity_id: int):
        cache_key = f"entity:detail:{entity_id}"
        cached = await self._cache.get(cache_key)
        if cached is not None:
            return await self.repo.get_entity(entity_id)
        entity = await self.repo.get_entity(entity_id)
        if entity is not None:
            await self._cache.set(cache_key, {"id": entity_id})
        return entity

    async def get_entity_links(self, entity_id: int):
        return await self.repo.get_entity_links(entity_id)

    async def merge_entities(
        self, source_id: int, target_id: int, reviewed_by: int | None = None
    ):
        result = await self.repo.merge_entities(source_id, target_id)
        if result is None:
            return None
        await self._cache.invalidate("entity:search:*")
        await self._cache.invalidate(f"entity:detail:{source_id}")
        await self._cache.invalidate(f"entity:detail:{target_id}")
        return result
