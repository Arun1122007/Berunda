"""Tests for the FastAPI application bootstrap — health, readiness, security, and error safety."""

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


# ── Health -------------------------------------------------------------------


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
    assert data["status"] in ("healthy", "degraded")
    assert "version" in data
    assert "checks" in data
    assert data["checks"]["python"] is True
    assert "uptime_seconds" in data["checks"]
    assert isinstance(data["checks"]["uptime_seconds"], (int, float))


# ── Readiness ----------------------------------------------------------------


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


# ── Root ---------------------------------------------------------------------


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


# ── API Status ---------------------------------------------------------------


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


# ── Error Handling Safety ----------------------------------------------------


@pytest.mark.asyncio
async def test_nonexistent_route_returns_404(client):
    async with client as ac:
        response = await ac.get("/nonexistent-route")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_error_response_is_json_not_html(client):
    async with client as ac:
        response = await ac.get("/nonexistent-route")
    assert "application/json" in response.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_error_response_does_not_leak_traceback(client):
    async with client as ac:
        response = await ac.get("/nonexistent-route")
    body = response.text.lower()
    assert "traceback" not in body
    assert "file" not in body or "line" not in body


# ── Security Headers ---------------------------------------------------------


@pytest.mark.asyncio
async def test_security_headers_present(client):
    async with client as ac:
        response = await ac.get("/health")
    headers = response.headers
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-frame-options") == "DENY"
    assert "strict-transport-security" in headers
    assert "referrer-policy" in headers


@pytest.mark.asyncio
async def test_correlation_id_in_response(client):
    async with client as ac:
        response = await ac.get("/health")
    assert "x-request-id" in response.headers
    cid = response.headers["x-request-id"]
    assert len(cid) > 0
    assert cid.count("-") >= 4  # UUID format


# ── Metrics (when prometheus_client is available) ----------------------------


@pytest.mark.asyncio
async def test_metrics_endpoint_when_enabled(client):
    async with client as ac:
        response = await ac.get("/metrics")
    assert response.status_code in (200, 404)  # 404 if prometheus not enabled
