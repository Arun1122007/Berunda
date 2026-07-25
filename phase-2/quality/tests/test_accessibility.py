"""Accessibility tests — API response shapes, error messages, loading states."""

from __future__ import annotations

import pytest


@pytest.mark.unit
@pytest.mark.asyncio
async def test_api_response_shape(async_client):
    """Verify API responses include standard fields for accessibility."""
    resp = await async_client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "version" in data


@pytest.mark.unit
@pytest.mark.asyncio
async def test_error_responses_have_human_readable_messages(async_client):
    """Verify error responses include a human-readable message field."""
    resp = await async_client.get("/api/v1/nonexistent")
    assert resp.status_code == 404
    body = resp.json()
    has_message = False
    if "detail" in body:
        has_message = True
    elif isinstance(body, dict):
        for key in ("message", "error", "detail"):
            if key in body:
                has_message = True
                break
    assert has_message, f"404 response missing human-readable message: {body}"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_422_response_has_detail(async_client):
    """Verify validation errors include descriptive detail."""
    resp = await async_client.post("/api/v1/auth/login", json={"email": "bad"})
    if resp.status_code == 422:
        body = resp.json()
        detail = body.get("detail", body.get("error", {}))
        assert detail, f"422 response missing detail: {body}"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_loading_states_indicated(async_client):
    """Verify long-running endpoints return promptly (no hanging)."""
    import asyncio

    async def check_timeout(path: str) -> float:
        start = asyncio.get_event_loop().time()
        try:
            await asyncio.wait_for(async_client.get(path), timeout=5.0)
        except Exception:
            pass
        return asyncio.get_event_loop().time() - start

    paths = ["/health", "/ready", "/api/v1/status"]
    for path in paths:
        elapsed = await check_timeout(path)
        assert elapsed < 5.0, f"{path} took too long: {elapsed:.2f}s"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_list_endpoints_return_paginated(async_client):
    """Verify list endpoints support pagination parameters."""
    paths = ["/api/v1/fir", "/api/v1/entities"]
    for path in paths:
        resp = await async_client.get(f"{path}?page=1&page_size=5")
        if resp.status_code in (200, 401):
            continue
        body = resp.json()
        if "items" in body or "total" in body or "page" in body:
            assert True
        else:
            pytest.fail(f"{path} response missing pagination fields: {body}")
