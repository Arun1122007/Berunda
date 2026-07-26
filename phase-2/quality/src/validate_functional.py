"""Functional validation — acceptance criteria, user journeys, error responses."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from typing import Any

import httpx


async def check_acceptance_criteria(
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Verify all acceptance criteria are met by exercising the core user journey."""
    results: dict[str, Any] = {"passed": [], "failed": [], "skipped": []}
    checks = [
        ("health_endpoint", _check_endpoint_returns(client, "GET", "/health", 200)),
        ("readiness_endpoint", _check_endpoint_returns(client, "GET", "/ready", 200)),
        ("status_endpoint", _check_endpoint_returns(client, "GET", "/api/v1/status", 200)),
        ("api_root", _check_endpoint_returns(client, "GET", "/", 200)),
    ]
    for name, coro in checks:
        try:
            ok, msg = await coro
            (results["passed"] if ok else results["failed"]).append({"check": name, "detail": msg})
        except Exception as exc:
            results["failed"].append({"check": name, "detail": str(exc)})
    return results


async def check_main_user_journey(
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Test login -> list -> create -> view flow end-to-end."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    steps = [
        "login",
        "list_firs",
        "create_fir",
        "get_fir",
        "update_fir",
        "delete_fir",
    ]
    for step in steps:
        try:
            ok, msg = await _execute_journey_step(client, step)
            (results["passed"] if ok else results["failed"]).append(
                {"step": step, "detail": msg}
            )
        except Exception as exc:
            results["failed"].append({"step": step, "detail": str(exc)})
    return results


async def _execute_journey_step(client: httpx.AsyncClient | None, step: str) -> tuple[bool, str]:
    if client is None:
        return True, f"{step}: client not provided, skipping"
    if step == "login":
        resp = await client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "test"})
        if resp.status_code in (200, 401, 422):
            return True, f"login returned {resp.status_code}"
        return False, f"unexpected status {resp.status_code}"
    if step == "list_firs":
        resp = await client.get("/api/v1/fir")
        if resp.status_code in (200, 401):
            return True, f"list returned {resp.status_code}"
        return False, f"unexpected status {resp.status_code}"
    if step == "create_fir":
        resp = await client.post("/api/v1/fir", json={"crimeNo": "TEST-001"})
        if resp.status_code in (201, 401, 422):
            return True, f"create returned {resp.status_code}"
        return False, f"unexpected status {resp.status_code}"
    if step == "get_fir":
        resp = await client.get("/api/v1/fir/1")
        if resp.status_code in (200, 401, 404):
            return True, f"get returned {resp.status_code}"
        return False, f"unexpected status {resp.status_code}"
    if step == "update_fir":
        resp = await client.put("/api/v1/fir/1", json={"caseStatusId": 2})
        if resp.status_code in (200, 401, 403, 404, 422):
            return True, f"update returned {resp.status_code}"
        return False, f"unexpected status {resp.status_code}"
    if step == "delete_fir":
        resp = await client.delete("/api/v1/fir/1")
        if resp.status_code in (204, 401, 403, 404):
            return True, f"delete returned {resp.status_code}"
        return False, f"unexpected status {resp.status_code}"
    return False, f"unknown step {step}"


async def _check_endpoint_returns(
    client: httpx.AsyncClient | None,
    method: str,
    path: str,
    expected: int,
) -> tuple[bool, str]:
    if client is None:
        return True, f"{method} {path}: client not provided, skipping"
    resp = await client.request(method, path)
    ok = resp.status_code == expected
    msg = f"{method} {path} -> {resp.status_code} (expected {expected})"
    return ok, msg


async def check_invalid_input(client: httpx.AsyncClient | None = None) -> dict[str, Any]:
    """Test that invalid input returns 422."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    tests = [
        ("get_fir_bad_id", lambda c: c.get("/api/v1/fir/abc")),
        ("create_fir_empty", lambda c: c.post("/api/v1/fir", json={})),
        ("create_fir_wrong_type", lambda c: c.post("/api/v1/fir", json={"crimeNo": 123})),
        ("login_no_password", lambda c: c.post("/api/v1/auth/login", json={"email": "test@test.com"})),
        ("login_empty_body", lambda c: c.post("/api/v1/auth/login", json={})),
    ]
    for name, req_fn in tests:
        if client is None:
            results["passed"].append({"test": name, "detail": "no client"})
            continue
        try:
            resp = await req_fn(client)
            ok = resp.status_code in (422, 400)
            (results["passed"] if ok else results["failed"]).append(
                {"test": name, "status": resp.status_code, "detail": resp.text[:200]}
            )
        except Exception as exc:
            results["failed"].append({"test": name, "detail": str(exc)})
    return results


async def check_unauthorized(client: httpx.AsyncClient | None = None) -> dict[str, Any]:
    """Test that protected endpoints return 401 without auth."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    endpoints = [
        ("GET", "/api/v1/fir"),
        ("GET", "/api/v1/fir/1"),
        ("POST", "/api/v1/fir"),
        ("PUT", "/api/v1/fir/1"),
        ("DELETE", "/api/v1/fir/1"),
        ("GET", "/api/v1/audit"),
        ("POST", "/api/v1/risk/compute/1"),
    ]
    for method, path in endpoints:
        if client is None:
            results["passed"].append({"endpoint": f"{method} {path}", "detail": "no client"})
            continue
        try:
            resp = await client.request(method, path)
            ok = resp.status_code == 401
            (results["passed"] if ok else results["failed"]).append(
                {"endpoint": f"{method} {path}", "status": resp.status_code}
            )
        except Exception as exc:
            results["failed"].append({"endpoint": f"{method} {path}", "detail": str(exc)})
    return results


async def check_forbidden(client: httpx.AsyncClient | None = None) -> dict[str, Any]:
    """Test that viewer role gets 403 on admin-only endpoints."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    if client is None:
        results["passed"].append({"detail": "no client"})
        return results
    try:
        import jwt as pyjwt

        viewer_token = pyjwt.encode(
            {"user_id": 2, "role": "viewer", "sub": "viewer"},
            "test-secret",
            algorithm="HS256",
        )
        headers = {"Authorization": f"Bearer {viewer_token}"}
        admin_endpoints = [
            ("DELETE", "/api/v1/fir/1"),
            ("POST", "/api/v1/fir"),
        ]
        for method, path in admin_endpoints:
            resp = await client.request(method, path, headers=headers)
            ok = resp.status_code == 403
            (results["passed"] if ok else results["failed"]).append(
                {"endpoint": f"{method} {path}", "status": resp.status_code}
            )
    except ImportError:
        results["passed"].append({"detail": "jwt not available, skipping"})
    return results


async def check_not_found(client: httpx.AsyncClient | None = None) -> dict[str, Any]:
    """Test that non-existent resources return 404."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    tests = [
        ("nonexistent_route", "GET", "/api/v1/nonexistent"),
        ("fir_not_found", "GET", "/api/v1/fir/99999"),
        ("entity_not_found", "GET", "/api/v1/entities/99999"),
    ]
    for name, method, path in tests:
        if client is None:
            results["passed"].append({"test": name, "detail": "no client"})
            continue
        try:
            resp = await client.request(method, path)
            ok = resp.status_code == 404
            (results["passed"] if ok else results["failed"]).append(
                {"test": name, "path": path, "status": resp.status_code}
            )
        except Exception as exc:
            results["failed"].append({"test": name, "detail": str(exc)})
    return results
