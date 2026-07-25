from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.cache_service import CacheService, get_cache


class BaseService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._cache: CacheService = get_cache()
