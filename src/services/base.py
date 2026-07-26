from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.cache_service import CacheService, get_cache


class BaseService:
    def __init__(self, session: Optional[AsyncSession] = None, repo: Optional[Any] = None) -> None:
        self.repo = repo
        self.session = session or (getattr(repo, "session", None) if repo else None)
        self._cache: CacheService = get_cache()
