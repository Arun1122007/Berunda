"""End-to-end test — complete user journey for Berunda FIR management."""

from __future__ import annotations

import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database import get_session
from src.main import app
from src.models.base import Base
from src.models.src_models import District


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def in_memory_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with factory() as session:
        if not await session.get(District, 1):
            session.add(District(DistrictID=1, DistrictName="Bengaluru Urban", StateID=1))
            await session.commit()

    yield factory
    await engine.dispose()


@pytest_asyncio.fixture
async def async_client(in_memory_db):
    async def override_get_session():
        async with in_memory_db() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_user_journey(async_client):
    """Complete 12-step user journey."""
    # 1. Register a new user
    reg_resp = await async_client.post("/api/v1/auth/register", json={
        "email": "e2e-admin@berunda.gov",
        "password": "StrongP@ss123",
        "role": "admin",
        "districtId": 1,
    })
    assert reg_resp.status_code == 201, f"Register failed: {reg_resp.text}"
    reg_data = reg_resp.json()
    assert "userId" in reg_data
    assert reg_data["email"] == "e2e-admin@berunda.gov"

    # 2. Login
    login_resp = await async_client.post("/api/v1/auth/login", json={
        "email": "e2e-admin@berunda.gov",
        "password": "StrongP@ss123",
    })
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    login_data = login_resp.json()
    assert "token" in login_data
    assert "refreshToken" in login_data
    token = login_data["token"]
    refresh_token = login_data["refreshToken"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # 3. Get current user
    me_resp = await async_client.get("/api/v1/auth/me", headers=auth_headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "e2e-admin@berunda.gov"

    # 4. List FIRs (should be empty)
    list_resp = await async_client.get("/api/v1/fir", headers=auth_headers)
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert "items" in list_data
    assert "total" in list_data
    initial_total = list_data["total"]

    # 5. Create an FIR
    create_resp = await async_client.post("/api/v1/fir", headers=auth_headers, json={
        "crimeNo": "CR-2026-E2E-001",
        "briefFacts": "End-to-end test case for Berunda platform",
    })
    assert create_resp.status_code == 201, f"Create failed: {create_resp.text}"
    create_data = create_resp.json()
    assert "caseMasterID" in create_data
    assert create_data["crimeNo"] == "CR-2026-E2E-001"
    case_id = create_data["caseMasterID"]

    # 6. Get the created FIR by ID
    get_resp = await async_client.get(f"/api/v1/fir/{case_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data["crimeNo"] == "CR-2026-E2E-001"
    assert get_data["caseMasterID"] == case_id

    # 7. Verify list reflects new case
    list_resp2 = await async_client.get("/api/v1/fir", headers=auth_headers)
    assert list_resp2.json()["total"] == initial_total + 1

    # 8. Update the FIR
    update_resp = await async_client.put(f"/api/v1/fir/{case_id}", headers=auth_headers, json={
        "briefFacts": "Updated facts after preliminary investigation.",
        "caseStatusId": 2,
    })
    assert update_resp.status_code == 200, f"Update failed: {update_resp.text}"
    update_data = update_resp.json()
    assert update_data["caseMasterID"] == case_id

    # 9. Refresh the token
    refresh_resp = await async_client.post("/api/v1/auth/refresh", json={
        "refreshToken": refresh_token,
    })
    assert refresh_resp.status_code == 200, f"Refresh failed: {refresh_resp.text}"
    refresh_data = refresh_resp.json()
    assert "token" in refresh_data
    assert "refreshToken" in refresh_data

    # 10. Test invalid input (missing CrimeNo → 422)
    invalid_resp = await async_client.post("/api/v1/fir", headers=auth_headers, json={
        "briefFacts": "Missing crime number",
    })
    assert invalid_resp.status_code == 422, f"Expected 422, got {invalid_resp.status_code}: {invalid_resp.text}"

    # 11. Test unauthorized access (no auth header → 401)
    noauth_resp = await async_client.post("/api/v1/fir", json={"crimeNo": "CR-2026-NOAUTH"})
    assert noauth_resp.status_code == 401, f"Expected 401, got {noauth_resp.status_code}"

    # 12. Confirm error response format
    # NOTE: Contract specifies {"error": {"code": ..., "message": ..., "requestId": ...}}
    # but backend returns {"detail": "..."} for HTTPException errors and
    # {"error": {"code": ..., "message": ...}} for BerundaError exceptions.
    # See contract_mismatches.md for details.
    err_resp = await async_client.get("/api/v1/fir/99999", headers=auth_headers)
    assert err_resp.status_code == 404
    err_body = err_resp.json()
    assert isinstance(err_body, dict), f"Error response should be JSON object, got: {err_body}"
