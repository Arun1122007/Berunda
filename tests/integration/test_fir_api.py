"""Integration tests for FIR API endpoints."""

from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database import get_session
from src.main import app
from src.models.base import Base
from src.models.auth_models import User
from src.services.auth_service import AuthService


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def async_client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_token(db_session):
    service = AuthService(db_session)
    await service.register("admin@test.com", "admin123", "admin", None)
    _, access, _ = await service.authenticate("admin@test.com", "admin123")
    return access


@pytest.mark.integration
class TestFIRAPI:
    async def test_list_firs_empty(self, async_client: AsyncClient, admin_token: str):
        response = await async_client.get(
            "/api/v1/fir",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    async def test_create_fir(self, async_client: AsyncClient, admin_token: str):
        response = await async_client.post(
            "/api/v1/fir",
            json={"crimeNo": "CR-2026-INT-TEST-001"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["crimeNo"] == "CR-2026-INT-TEST-001"
        assert data["caseMasterId"] > 0

    async def test_create_and_retrieve(self, async_client: AsyncClient, admin_token: str):
        create_resp = await async_client.post(
            "/api/v1/fir",
            json={"crimeNo": "CR-2026-INT-TEST-002", "briefFacts": "Integration test case"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_resp.status_code == 201
        case_id = create_resp.json()["caseMasterId"]

        get_resp = await async_client.get(
            f"/api/v1/fir/{case_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["crimeNo"] == "CR-2026-INT-TEST-002"
        assert data["caseMasterId"] == case_id

    async def test_list_after_create(self, async_client: AsyncClient, admin_token: str):
        await async_client.post(
            "/api/v1/fir",
            json={"crimeNo": "CR-2026-INT-TEST-003"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        response = await async_client.get(
            "/api/v1/fir",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0

    async def test_create_without_auth_returns_401(self, async_client: AsyncClient):
        response = await async_client.post(
            "/api/v1/fir",
            json={"crimeNo": "CR-2026-UNAUTH"},
        )
        assert response.status_code == 401

    async def test_list_without_auth_returns_401(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/fir")
        assert response.status_code == 401

    async def test_get_nonexistent_returns_404(self, async_client: AsyncClient, admin_token: str):
        response = await async_client.get(
            "/api/v1/fir/99999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_create_fir_all_fields(self, async_client: AsyncClient, admin_token: str):
        response = await async_client.post(
            "/api/v1/fir",
            json={
                "crimeNo": "CR-2026-INT-FULL",
                "caseNo": "INT/2026",
                "policeStationId": 5,
                "caseCategoryId": 1,
                "gravityOffenceId": 2,
                "crimeMajorHeadId": 1,
                "crimeMinorHeadId": 1,
                "caseStatusId": 1,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
