"""Tests for the FastAPI application bootstrap."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def app():
    from src.main import app

    return app


@pytest.fixture
def client(app):
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health_returns_200(client):
    async with client as ac:
        response = await ac.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_returns_expected_structure(client):
    async with client as ac:
        response = await ac.get("/health")
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"
    assert "uptime_seconds" in data
    assert isinstance(data["uptime_seconds"], float)


@pytest.mark.asyncio
async def test_readiness_returns_200(client):
    async with client as ac:
        response = await ac.get("/ready")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_readiness_returns_checks(client):
    async with client as ac:
        response = await ac.get("/ready")
    data = response.json()
    assert data["status"] in ("ready", "degraded")
    assert "checks" in data
    assert data["checks"]["python"] is True
    assert "database" in data["checks"]


@pytest.mark.asyncio
async def test_root_returns_200(client):
    async with client as ac:
        response = await ac.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_root_returns_service_info(client):
    async with client as ac:
        response = await ac.get("/")
    data = response.json()
    assert data["service"] == "Berunda"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_api_status_returns_200(client):
    async with client as ac:
        response = await ac.get("/api/v1/status")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_api_status_returns_correct_structure(client):
    async with client as ac:
        response = await ac.get("/api/v1/status")
    data = response.json()
    assert data["api_version"] == "v1"
    assert data["service"] == "Berunda"
    assert data["status"] == "operational"


@pytest.mark.asyncio
async def test_unhandled_error_returns_safe_response(client):
    async with client as ac:
        response = await ac.get("/nonexistent-route")
    assert response.status_code == 404
