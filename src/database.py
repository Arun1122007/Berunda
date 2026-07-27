"""Database engine and session management — lazy initialization."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

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

        # Resolve relative SQLite paths relative to app root (where database.py is located)
        if db_url.startswith("sqlite+aiosqlite:///"):
            rel = db_url.removeprefix("sqlite+aiosqlite:///")
            rel_path = Path(rel)
            if not rel_path.is_absolute():
                import os
                import shutil
                from contextlib import suppress

                app_root = Path(__file__).resolve().parent.parent
                db_file = (app_root / rel_path).resolve()
                if os.name != "nt" and db_file.exists():
                    tmp_db = Path("/tmp/berunda.db")
                    if not tmp_db.exists():
                        with suppress(Exception):
                            shutil.copy2(db_file, tmp_db)
                    if tmp_db.exists():
                        db_file = tmp_db
                db_url = f"sqlite+aiosqlite:///{db_file.as_posix()}"

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


async def wait_for_db(retries: int = 5, delay: float = 2.0) -> bool:
    """Wait for the database to become available with retries."""
    import asyncio

    for attempt in range(retries):
        try:
            engine = get_engine()
            async with engine.connect() as conn:
                await conn.execute(sa.text("SELECT 1"))
            return True
        except Exception:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
    return False


async def dispose_engine() -> None:
    """Dispose of the global engine, releasing all connections."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
