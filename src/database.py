"""Database engine and session management — lazy initialization."""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.shared.logging import get_logger

logger = get_logger(__name__)

_engine = None
_session_factory: async_sessionmaker | None = None


async def wait_for_db(retries: int = 5, delay: float = 2.0) -> bool:
    """Retry DB connection with exponential backoff at startup."""
    import sqlalchemy as sa

    for attempt in range(retries):
        try:
            engine = get_engine()
            async with engine.connect() as conn:
                await conn.execute(sa.text("SELECT 1"))
            logger.info("Database connection established")
            return True
        except Exception as exc:
            if attempt < retries - 1:
                wait = delay * (2**attempt)
                logger.warning(
                    "DB not ready (attempt %d/%d), retrying in %.1fs", attempt + 1, retries, wait
                )
                await asyncio.sleep(wait)
            else:
                logger.error("Database unreachable after %d retries", retries, exc_info=exc)
                return False
    return False


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

        if db_url.startswith("sqlite+aiosqlite:///"):
            rel = db_url.removeprefix("sqlite+aiosqlite:///")
            if not Path(rel).is_absolute():
                db_url = f"sqlite+aiosqlite:///{(Path.cwd() / rel).as_posix()}"

        _engine = create_async_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=30,
            pool_recycle=1800,
            echo=settings.DATABASE_ECHO or settings.LOG_LEVEL == "DEBUG",
        )
    return _engine


async def dispose_engine() -> None:
    """Dispose the engine, releasing all connections."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
        logger.info("Database engine disposed")


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


_read_engine = None
_read_session_factory: async_sessionmaker | None = None


def get_read_engine():
    """Get or create a read-replica engine if READ_DATABASE_URL is set, else fallback to primary."""
    global _read_engine
    if _read_engine is None:
        read_url = os.environ.get("READ_DATABASE_URL") or settings.DATABASE_URL
        if read_url == settings.DATABASE_URL:
            return get_engine()
        if not read_url.startswith("postgresql+asyncpg://") and not read_url.startswith(
            "sqlite+aiosqlite://"
        ):
            return get_engine()
        _read_engine = create_async_engine(
            read_url,
            pool_pre_ping=True,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_recycle=1800,
            echo=settings.LOG_LEVEL == "DEBUG",
        )
    return _read_engine


def get_read_session_factory():
    global _read_session_factory
    if _read_session_factory is None:
        _read_session_factory = async_sessionmaker(
            get_read_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _read_session_factory


async def get_read_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a read-only session (uses read replica if configured)."""
    factory = get_read_session_factory()
    async with factory() as session:
        try:
            yield session
        finally:
            await session.close()
