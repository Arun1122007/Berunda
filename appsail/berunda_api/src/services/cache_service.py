"""Redis cache-aside service for query result caching."""

from __future__ import annotations

import json
from typing import Any

from src.config import settings
from src.shared.logging import get_logger

logger = get_logger(__name__)


class CacheService:
    """Lightweight cache-aside helper backed by Redis."""

    def __init__(self) -> None:
        self._redis = None
        self._enabled = bool(settings.REDIS_URL and settings.CACHE_TTL_SECONDS > 0)

    async def _get_redis(self):
        if self._redis is None and self._enabled:
            try:
                import redis.asyncio as aioredis

                self._redis = await aioredis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                )
            except Exception as exc:
                logger.warning("Redis unavailable — cache disabled", exc_info=exc)
                self._enabled = False
        return self._redis

    async def get(self, key: str) -> Any | None:
        if not self._enabled:
            return None
        r = await self._get_redis()
        if r is None:
            return None
        try:
            data = await r.get(key)
            if data:
                return json.loads(data)
        except Exception as exc:
            logger.debug("Cache GET error for %s: %s", key, exc)
        return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        if not self._enabled:
            return
        r = await self._get_redis()
        if r is None:
            return
        try:
            await r.setex(key, ttl or settings.CACHE_TTL_SECONDS, json.dumps(value, default=str))
        except Exception as exc:
            logger.debug("Cache SET error for %s: %s", key, exc)

    async def invalidate(self, pattern: str) -> None:
        if not self._enabled:
            return
        r = await self._get_redis()
        if r is None:
            return
        try:
            keys = await r.keys(pattern)
            if keys:
                await r.delete(*keys)
        except Exception as exc:
            logger.debug("Cache INVALIDATE error for %s: %s", pattern, exc)

    async def close(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None


_cache_service: CacheService | None = None


def get_cache() -> CacheService:
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
