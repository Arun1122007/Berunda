"""Integration tests for Dashboard API endpoints."""

from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings
from src.database import get_session
from src.dependencies import get_fir_repo
from src.main import app
from src.models.base import Base
from src.repositories.sqlite_adapter import SQLiteFIRRepository


def _make_token(role: str, user_id: int = 1, **extra) -> str:
    import jwt
    import time
    payload = {
        "id": user_id,
        "user_id": user_id,
        "role": role,
        "district_id": extra.get("district_id", 1),
        "police_station_id": extra.get("police_station_id", 5),
        "sub": f"user-{user_id}",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


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

    def override_get_fir_repo(request=None):
        return SQLiteFIRRepository(db_session)

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_fir_repo] = override_get_fir_repo
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def populated_firs(db_session):
    from datetime import date
    from src.models.src_models import CaseMaster

    firs = [
        CaseMaster(CrimeNo="CR-2026-DSH-001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 15)),
        CaseMaster(CrimeNo="CR-2026-DSH-002", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 2, 10)),
        CaseMaster(CrimeNo="CR-2026-DSH-003", CaseStatusID=2, PoliceStationID=5, CrimeRegisteredDate=date(2026, 3, 5)),
        CaseMaster(CrimeNo="CR-2026-DSH-004", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 4, 20)),
        CaseMaster(CrimeNo="CR-2026-DSH-005", CaseStatusID=3, PoliceStationID=5, CrimeRegisteredDate=date(2026, 5, 1)),
    ]
    for f in firs:
        db_session.add(f)
    await db_session.commit()
    for f in firs:
        await db_session.refresh(f)
    return firs


@pytest.mark.integration
class TestDashboardAPI:
    @pytest.mark.asyncio
    async def test_officer_dashboard_empty(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/dashboard/officer",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["totalFirs"] == 0
        assert data["pendingReviewCount"] == 0
        assert data["unassignedCount"] == 0

    @pytest.mark.asyncio
    async def test_officer_dashboard_with_data(self, async_client: AsyncClient, populated_firs):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/dashboard/officer",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["totalFirs"] == 5
        assert "statusCounts" in data
        assert "assignedToMeCount" in data
        assert "pendingReviewCount" in data
        assert "unassignedCount" in data
        assert "recentActivityCount" in data

    @pytest.mark.asyncio
    async def test_officer_dashboard_shows_fields(self, async_client: AsyncClient, populated_firs):
        token = _make_token("officer", user_id=42)
        response = await async_client.get(
            "/api/v1/dashboard/officer",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert "assignedToMeCount" in response.json()

    @pytest.mark.asyncio
    async def test_officer_dashboard_without_auth(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/dashboard/officer")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_supervisor_dashboard_empty(self, async_client: AsyncClient):
        token = _make_token("supervisor")
        response = await async_client.get(
            "/api/v1/dashboard/supervisor",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["totalFirs"] == 0
        assert data["activeOfficerCount"] == 0
        assert data["casesPerOfficer"] == {}

    @pytest.mark.asyncio
    async def test_supervisor_dashboard_with_data(self, async_client: AsyncClient, populated_firs):
        token = _make_token("supervisor")
        response = await async_client.get(
            "/api/v1/dashboard/supervisor",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["totalFirs"] == 5
        assert "statusCounts" in data
        assert "pendingReviewCount" in data
        assert "unassignedCount" in data
        assert "activeOfficerCount" in data
        assert "casesPerOfficer" in data

    @pytest.mark.asyncio
    async def test_supervisor_dashboard_admin_allowed(self, async_client: AsyncClient, populated_firs):
        token = _make_token("admin")
        response = await async_client.get(
            "/api/v1/dashboard/supervisor",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["totalFirs"] == 5

    @pytest.mark.asyncio
    async def test_supervisor_dashboard_officer_forbidden(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/dashboard/supervisor",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_supervisor_dashboard_viewer_forbidden(self, async_client: AsyncClient):
        token = _make_token("viewer")
        response = await async_client.get(
            "/api/v1/dashboard/supervisor",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_supervisor_dashboard_analyst_forbidden(self, async_client: AsyncClient):
        token = _make_token("analyst")
        response = await async_client.get(
            "/api/v1/dashboard/supervisor",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_supervisor_dashboard_no_auth_returns_401(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/dashboard/supervisor")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_activity_empty(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/dashboard/activity",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_activity_with_data(self, async_client: AsyncClient, populated_firs):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/dashboard/activity",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_activity_without_auth(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/dashboard/activity")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_activity_not_exceeds_10_items(self, async_client: AsyncClient, populated_firs):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/dashboard/activity",
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json()
        assert len(data) <= 10

    @pytest.mark.asyncio
    async def test_officer_dashboard_empty_ps(self, async_client: AsyncClient):
        token = _make_token("officer", police_station_id=None)
        response = await async_client.get(
            "/api/v1/dashboard/officer",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_supervisor_dashboard_empty_ps(self, async_client: AsyncClient):
        token = _make_token("supervisor", police_station_id=None)
        response = await async_client.get(
            "/api/v1/dashboard/supervisor",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_admin_dashboard_officer(self, async_client: AsyncClient, populated_firs):
        token = _make_token("admin")
        response = await async_client.get(
            "/api/v1/dashboard/officer",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["totalFirs"] == 5

    @pytest.mark.asyncio
    async def test_activity_returns_list(self, async_client: AsyncClient, populated_firs):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/dashboard/activity",
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json()
        assert isinstance(data, list)
