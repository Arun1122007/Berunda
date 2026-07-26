"""Integration tests for Report API endpoints."""

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


@pytest.mark.integration
class TestReportAPI:
    @pytest.mark.asyncio
    async def test_request_report_success(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/reports",
            json={
                "ReportType": "fir_summary",
                "Parameters": '{"case_master_id": 1}',
                "FileFormat": "pdf",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["reportType"] == "fir_summary"
        assert data["status"] == "requested"
        assert data["requestedByUserID"] == 1
        assert data["reportID"].startswith("RPT-")

    @pytest.mark.asyncio
    async def test_request_report_investigation_progress(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/reports",
            json={
                "ReportType": "investigation_progress",
                "Parameters": '{"case_master_id": 1}',
                "FileFormat": "csv",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["reportType"] == "investigation_progress"
        assert data["fileFormat"] == "csv"

    @pytest.mark.asyncio
    async def test_request_report_evidence_inventory(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/reports",
            json={
                "ReportType": "evidence_inventory",
                "FileFormat": "json",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["reportType"] == "evidence_inventory"

    @pytest.mark.asyncio
    async def test_request_report_case_timeline(self, async_client: AsyncClient):
        token = _make_token("analyst")
        response = await async_client.post(
            "/api/v1/reports",
            json={
                "ReportType": "case_timeline",
                "FileFormat": "pdf",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_request_report_supervisor_allowed(self, async_client: AsyncClient):
        token = _make_token("supervisor")
        response = await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_request_report_viewer_forbidden(self, async_client: AsyncClient):
        token = _make_token("viewer")
        response = await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_request_report_no_auth_returns_401(self, async_client: AsyncClient):
        response = await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_request_report_invalid_returns_422(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/reports",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_list_reports_empty(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/reports",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_list_reports_after_create(self, async_client: AsyncClient):
        token = _make_token("officer")
        await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary"},
            headers={"Authorization": f"Bearer {token}"},
        )
        response = await async_client.get(
            "/api/v1/reports",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["reportType"] == "fir_summary"

    @pytest.mark.asyncio
    async def test_list_reports_without_auth(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/reports")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_report_by_id(self, async_client: AsyncClient):
        token = _make_token("officer")
        create_resp = await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary"},
            headers={"Authorization": f"Bearer {token}"},
        )
        report_id = create_resp.json()["reportID"]

        response = await async_client.get(
            f"/api/v1/reports/{report_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["reportID"] == report_id
        assert data["status"] == "requested"

    @pytest.mark.asyncio
    async def test_get_report_not_found(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/reports/RPT-NONEXISTENT",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_report_without_auth_returns_200(self, async_client: AsyncClient):
        token = _make_token("officer")
        create_resp = await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary"},
            headers={"Authorization": f"Bearer {token}"},
        )
        report_id = create_resp.json()["reportID"]
        response = await async_client.get(f"/api/v1/reports/{report_id}")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_generate_report(self, async_client: AsyncClient):
        token = _make_token("officer")
        create_resp = await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary", "Parameters": '{"case_master_id": 1}', "FileFormat": "pdf"},
            headers={"Authorization": f"Bearer {token}"},
        )
        report_id = create_resp.json()["reportID"]

        response = await async_client.post(
            f"/api/v1/reports/{report_id}/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_generate_report_not_found(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/reports/RPT-NONEXISTENT/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_generate_report_analyst(self, async_client: AsyncClient):
        token = _make_token("analyst")
        create_resp = await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "evidence_inventory"},
            headers={"Authorization": f"Bearer {token}"},
        )
        report_id = create_resp.json()["reportID"]

        response = await async_client.post(
            f"/api/v1/reports/{report_id}/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_generate_report_viewer_forbidden(self, async_client: AsyncClient):
        token = _make_token("viewer")
        response = await async_client.post(
            "/api/v1/reports/RPT-FAKE/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_admin_all_report_ops(self, async_client: AsyncClient):
        token = _make_token("admin")
        create_resp = await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert create_resp.status_code == 201

    @pytest.mark.asyncio
    async def test_list_reports_shows_all_for_user(self, async_client: AsyncClient):
        token1 = _make_token("officer", user_id=10)
        token2 = _make_token("officer", user_id=20)

        await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary"},
            headers={"Authorization": f"Bearer {token1}"},
        )
        await async_client.post(
            "/api/v1/reports",
            json={"ReportType": "case_timeline"},
            headers={"Authorization": f"Bearer {token2}"},
        )

        response = await async_client.get(
            "/api/v1/reports",
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
