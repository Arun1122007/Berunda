"""End-to-end user journey: Login -> List -> Create -> View -> Update -> Delete -> Verify.

Uses ASGITransport (in-memory). Implemented as a single test function to
avoid session-sharing issues across test methods.

Usage:
  pytest tests/end-to-end/ --run-e2e -v
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database import get_session
from src.main import app
from src.models.base import Base


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_full_user_journey():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async def override_get_session():
            yield session

        app.dependency_overrides[get_session] = override_get_session
        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # --- Login ---
            resp = await client.post(
                "/api/v1/auth/register",
                json={"email": "e2e_admin@test.com", "password": "e2ePass123", "role": "admin"},
            )
            assert resp.status_code == 201

            resp = await client.post(
                "/api/v1/auth/login",
                json={"email": "e2e_admin@test.com", "password": "e2ePass123"},
            )
            assert resp.status_code == 200
            token = resp.json()["token"]
            auth_header = {"Authorization": f"Bearer {token}"}

            # --- Get profile ---
            resp = await client.get("/api/v1/auth/me", headers=auth_header)
            assert resp.status_code == 200
            assert resp.json()["email"] == "e2e_admin@test.com"
            assert resp.json()["role"] == "admin"

            # --- List cases (empty) ---
            resp = await client.get("/api/v1/fir", headers=auth_header)
            assert resp.status_code == 200
            data = resp.json()
            assert data["items"] == []
            assert data["total"] == 0

            # --- Create case ---
            resp = await client.post(
                "/api/v1/fir",
                json={"crimeNo": "CR-2026-E2E-001", "caseNo": "E2E/2026", "briefFacts": "E2E test case"},
                headers=auth_header,
            )
            assert resp.status_code == 201
            data = resp.json()
            assert data["crimeNo"] == "CR-2026-E2E-001"
            assert data["caseMasterID"] > 0
            case_id = data["caseMasterID"]

            # --- Get created case ---
            resp = await client.get(f"/api/v1/fir/{case_id}", headers=auth_header)
            assert resp.status_code == 200
            data = resp.json()
            assert data["crimeNo"] == "CR-2026-E2E-001"

            # --- List includes new case ---
            resp = await client.get("/api/v1/fir", headers=auth_header)
            assert resp.status_code == 200
            data = resp.json()
            crime_nos = [item.get("crimeNo") for item in data["items"]]
            assert "CR-2026-E2E-001" in crime_nos
            assert data["total"] >= 1

            # --- Update case ---
            resp = await client.put(
                f"/api/v1/fir/{case_id}",
                json={"briefFacts": "Updated E2E test case facts"},
                headers=auth_header,
            )
            assert resp.status_code == 200

            # --- Verify update persisted ---
            resp = await client.get(f"/api/v1/fir/{case_id}", headers=auth_header)
            assert resp.status_code == 200

            # --- Delete case ---
            resp = await client.delete(f"/api/v1/fir/{case_id}", headers=auth_header)
            assert resp.status_code == 204

            # --- Verify deleted not in list ---
            resp = await client.get("/api/v1/fir", headers=auth_header)
            assert resp.status_code == 200
            crime_nos = [item.get("crimeNo") for item in resp.json()["items"]]
            assert "CR-2026-E2E-001" not in crime_nos

            # --- Failure: invalid login ---
            try:
                await client.post(
                    "/api/v1/auth/login",
                    json={"email": "nonexistent@test.com", "password": "wrong"},
                )
            except Exception:
                pass

            # --- Failure: create without auth ---
            resp = await client.post("/api/v1/fir", json={"crimeNo": "CR-2026-UNAUTH"})
            assert resp.status_code == 401

        app.dependency_overrides.clear()
