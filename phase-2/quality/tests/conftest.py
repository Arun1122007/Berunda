"""Test fixtures for quality workstream — reuses existing project conftest."""

from __future__ import annotations

import os
import sys
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any

_root = Path(__file__).resolve().parents[3]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pytest


@pytest.fixture
def app() -> Any:
    """Return the FastAPI application instance."""
    try:
        from src.main import app as _app
        return _app
    except ImportError:
        pytest.skip("FastAPI app module not found")


@pytest.fixture
async def async_client(app: Any) -> AsyncGenerator[Any, None]:
    """Provide an async HTTP client for testing API endpoints."""
    try:
        from httpx import ASGITransport, AsyncClient

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    except ImportError as exc:
        pytest.skip(f"httpx not available: {exc}")


@pytest.fixture
async def in_memory_db() -> AsyncGenerator[Any, None]:
    """Create an in-memory SQLite database for testing."""
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    from src.models.base import Base

    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_session

    await engine.dispose()


@pytest.fixture
def auth_headers_admin() -> dict[str, str]:
    """Return auth headers for an admin user."""
    import uuid
    import jwt as pyjwt
    import os
    import time

    secret = os.environ.get("AUTH_JWT_SECRET", "test-secret")
    payload = {
        "sub": "admin",
        "user_id": 1,
        "role": "admin",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "jti": str(uuid.uuid4()),
    }
    token = pyjwt.encode(payload, secret, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_viewer() -> dict[str, str]:
    """Return auth headers for a viewer-only user."""
    import uuid
    import jwt as pyjwt
    import os
    import time

    secret = os.environ.get("AUTH_JWT_SECRET", "test-secret")
    payload = {
        "sub": "viewer",
        "user_id": 2,
        "role": "viewer",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "jti": str(uuid.uuid4()),
    }
    token = pyjwt.encode(payload, secret, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}
