"""Database reset utility — drops all tables, recreates them, and seeds data.

Usage:
    python -c "from reset_db import reset_database; reset_database()"
    python -m phase-2.database-auth.reset_db
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session as SASession, sessionmaker

from src.config import settings
from src.models import Base


def get_sync_engine_url(url: str | None = None) -> str:
    source = url or settings.DATABASE_URL
    return source.replace("+aiosqlite", "").replace("+asyncpg", "")


def drop_all(url: str | None = None, engine=None) -> None:
    owned_engine = engine is None
    if owned_engine:
        engine = create_engine(get_sync_engine_url(url))
    try:
        Base.metadata.reflect(engine)
        table_names = list(Base.metadata.tables.keys())
        # Disable FK checks for SQLite
        if "sqlite" in engine.name:
            with engine.connect() as conn:
                conn.execute(text("PRAGMA foreign_keys = OFF"))
                conn.commit()

        Base.metadata.drop_all(engine)

        if "sqlite" in engine.name:
            with engine.connect() as conn:
                conn.execute(text("PRAGMA foreign_keys = ON"))
                conn.commit()

        print(f"Dropped {len(table_names)} tables: {', '.join(sorted(table_names))}")
        return table_names
    finally:
        if owned_engine:
            engine.dispose()


def create_all(url: str | None = None, engine=None) -> list[str]:
    owned_engine = engine is None
    if owned_engine:
        engine = create_engine(get_sync_engine_url(url))
    try:
        Base.metadata.create_all(engine)
        tables = list(Base.metadata.tables.keys())
        print(f"Created {len(tables)} tables: {', '.join(sorted(tables))}")
        return tables
    finally:
        if owned_engine:
            engine.dispose()


def seed_data(url: str | None = None, engine=None) -> None:
    from phase2.database_auth.seed_data import seed_all

    owned_engine = engine is None
    if owned_engine:
        engine = create_engine(get_sync_engine_url(url))
    try:
        session_factory = sessionmaker(bind=engine)
        with session_factory() as session:
            seed_all(session)
    finally:
        if owned_engine:
            engine.dispose()


def reset_database(url: str | None = None) -> None:
    """Drop all tables, recreate them, and seed with lookup + demo data."""
    engine = create_engine(get_sync_engine_url(url))
    try:
        drop_all(url, engine=engine)
        create_all(url, engine=engine)
        # Reload metadata after create
        Base.metadata.refresh(engine)
        seed_data(url, engine=engine)
        print("Database reset complete.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "reset"
    url = sys.argv[2] if len(sys.argv) > 2 else None

    if action == "drop":
        drop_all(url)
    elif action == "create":
        create_all(url)
    elif action == "seed":
        seed_data(url)
    elif action == "reset":
        reset_database(url)
    else:
        print(f"Usage: python {__file__} [drop|create|seed|reset] [DATABASE_URL]")
