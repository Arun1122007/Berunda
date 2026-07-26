"""Database engine and session management — lazy initialization."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

_engine = None
_session_factory: async_sessionmaker | None = None


def get_engine():
    global _engine
    if _engine is None:
        db_url = settings.DATABASE_URL
        if (
            not db_url.startswith("postgresql+asyncpg://")
            and not db_url.startswith("sqlite+aiosqlite://")
            and not db_url.startswith("mysql+aiomysql://")
        ):
            raise ValueError("DATABASE_URL must be a valid async postgresql, mysql, or sqlite URL")

        # Resolve relative SQLite paths to absolute
        if db_url.startswith("sqlite+aiosqlite:///"):
            rel = db_url.removeprefix("sqlite+aiosqlite:///")
            if not Path(rel).is_absolute():
                db_url = f"sqlite+aiosqlite:///{(Path.cwd() / rel).as_posix()}"

        is_sqlite = db_url.startswith("sqlite+aiosqlite://")
        if is_sqlite:
            _engine = create_async_engine(
                db_url,
                poolclass=NullPool,
                echo=settings.LOG_LEVEL == "DEBUG",
            )
        else:
            _engine = create_async_engine(
                db_url,
                pool_pre_ping=True,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW,
                pool_timeout=30,
                pool_recycle=1800,
                echo=settings.LOG_LEVEL == "DEBUG",
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
