"""Database engine and session management — lazy initialization."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL: str = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/berunda",
)

_engine = None
_session_factory: async_sessionmaker | None = None


def get_engine():
    global _engine
    if _engine is None:
        if not DATABASE_URL.startswith("postgresql+asyncpg://") and not DATABASE_URL.startswith(
            "sqlite+aiosqlite://"
        ):
            raise ValueError("DATABASE_URL must be a valid async postgresql or sqlite URL")

        # Enterprise-grade connection pool configuration
        _engine = create_async_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Health check before using a connection
            pool_size=int(os.environ.get("DB_POOL_SIZE", "5")),
            max_overflow=int(os.environ.get("DB_MAX_OVERFLOW", "10")),
            pool_timeout=30,
            pool_recycle=1800,  # Recycle connections after 30 minutes
            echo=os.environ.get("LOG_LEVEL") == "DEBUG",
        )
    return _engine


def get_session_factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
        finally:
            await session.close()
