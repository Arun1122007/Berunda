"""Smoke tests — database connectivity boundary.

Validates the database layer handles connection failures gracefully
without crashing the application or leaking internals.
"""

from __future__ import annotations

import asyncio
from unittest.mock import Mock, patch

import pytest


def _reset_engine():
    """Safely reset the global engine singleton (dispose_engine is async)."""
    from src.database import dispose_engine

    asyncio.run(dispose_engine())


class TestDatabaseConnectivityBoundary:
    """Database connection failures must be handled safely."""

    @pytest.fixture(autouse=True)
    def _cleanup_engine(self):
        _reset_engine()
        yield
        _reset_engine()

    def test_get_engine_returns_singleton(self):
        _reset_engine()
        from src.database import get_engine

        e1 = get_engine()
        e2 = get_engine()
        assert e1 is e2

    def test_dispose_engine_clears_state(self):
        _reset_engine()
        from src.database import get_engine

        _ = get_engine()
        _reset_engine()
        from src.database import get_engine as ge

        assert ge() is not None

    def test_get_engine_rejects_invalid_url_scheme(self):
        _reset_engine()
        mock_settings = Mock()
        mock_settings.DATABASE_URL = "not-a-valid-url"
        mock_settings.DB_POOL_SIZE = 5
        mock_settings.DB_MAX_OVERFLOW = 10
        mock_settings.LOG_LEVEL = "INFO"
        with patch("src.database.settings", mock_settings):
            from src.database import get_engine

            with pytest.raises(ValueError, match="DATABASE_URL must be a valid async"):
                get_engine()

    def test_get_session_factory_produces_sessions(self):
        _reset_engine()
        from src.database import get_session_factory

        factory = get_session_factory()
        assert factory is not None

    def test_can_drive_multiple_dispose_calls(self):
        _reset_engine()
        _reset_engine()
        _reset_engine()

    def test_wait_for_db_handles_unreachable_gracefully(self):
        from src.database import wait_for_db

        try:
            result = asyncio.run(wait_for_db(retries=1, delay=0.1))
            assert isinstance(result, bool)
        except Exception:
            pytest.fail("wait_for_db raised unexpectedly")


class TestDatabaseGracefulFailure:
    """Application must not crash when database is unavailable at startup."""

    @pytest.mark.asyncio
    async def test_health_does_not_crash_when_db_unreachable(self, smoke_client):
        from src.main import app

        app.state.start_time = 0.0
        async with smoke_client as c:
            resp = await c.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
