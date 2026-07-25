"""Smoke test configuration — lightweight validation of startup and core endpoints."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.smoke


@pytest.fixture(scope="session")
def smoke_app():
    from src.main import app

    return app


@pytest.fixture
def smoke_client(smoke_app):
    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=smoke_app)
    return AsyncClient(transport=transport, base_url="http://test")
