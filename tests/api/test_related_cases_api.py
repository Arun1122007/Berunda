"""Integration tests for Related Cases API endpoints."""

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
async def sample_firs(db_session):
    from datetime import date
    from src.models.src_models import CaseMaster

    firs = [
        CaseMaster(CrimeNo="CR-2026-DSH-001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 15)),
        CaseMaster(CrimeNo="CR-2026-DSH-002", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 2, 10)),
        CaseMaster(CrimeNo="CR-2026-DSH-003", CaseStatusID=2, PoliceStationID=3, CrimeRegisteredDate=date(2026, 3, 5)),
        CaseMaster(CrimeNo="CR-2026-UNL-004", CaseStatusID=3, PoliceStationID=4, CrimeRegisteredDate=date(2026, 4, 20)),
    ]
    for f in firs:
        db_session.add(f)
    await db_session.commit()
    for f in firs:
        await db_session.refresh(f)
    return firs


@pytest.mark.integration
class TestRelatedCasesAPI:
    @pytest.mark.asyncio
    async def test_generate_related_cases(self, async_client: AsyncClient, sample_firs):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        for item in data:
            assert item["sourceFIRID"] == 1
            assert item["candidateFIRID"] is not None
            assert item["confidenceScore"] is not None
            assert item["supportingSignals"] is not None
            assert "suggestionID" in item

    @pytest.mark.asyncio
    async def test_generate_related_cases_second_call_returns_cached(self, async_client: AsyncClient, sample_firs):
        token = _make_token("officer")
        first = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        second = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert first.status_code == 200
        assert second.status_code == 200
        assert len(first.json()) == len(second.json())

    @pytest.mark.asyncio
    async def test_generate_related_cases_nonexistent_fir(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/fir/99999/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_generate_related_cases_viewer_forbidden(self, async_client: AsyncClient):
        token = _make_token("viewer")
        response = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_generate_related_cases_no_auth_returns_401(self, async_client: AsyncClient):
        response = await async_client.post("/api/v1/fir/1/related-cases/generate")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_generate_with_analyst_role(self, async_client: AsyncClient, sample_firs):
        token = _make_token("analyst")
        response = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_list_related_cases_empty(self, async_client: AsyncClient, sample_firs):
        token = _make_token("officer")
        response = await async_client.get(
            "/api/v1/fir/1/related-cases",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_list_related_cases_after_generate(self, async_client: AsyncClient, sample_firs):
        token = _make_token("officer")
        await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        response = await async_client.get(
            "/api/v1/fir/1/related-cases",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        for item in data:
            assert "suggestionID" in item

    @pytest.mark.asyncio
    async def test_list_related_cases_without_auth(self, async_client: AsyncClient, sample_firs):
        response = await async_client.get("/api/v1/fir/1/related-cases")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_review_accept_suggestion(self, async_client: AsyncClient, sample_firs):
        off_token = _make_token("officer")
        gen_resp = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {off_token}"},
        )
        suggestion_id = gen_resp.json()[0]["suggestionID"]

        sup_token = _make_token("supervisor")
        response = await async_client.put(
            f"/api/v1/fir/related-cases/{suggestion_id}/review",
            json={"ReviewStatus": "accepted", "ReviewReason": "Confirmed match"},
            headers={"Authorization": f"Bearer {sup_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["reviewStatus"] == "accepted"

    @pytest.mark.asyncio
    async def test_review_reject_suggestion(self, async_client: AsyncClient, sample_firs):
        off_token = _make_token("officer")
        gen_resp = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {off_token}"},
        )
        suggestion_id = gen_resp.json()[0]["suggestionID"]

        sup_token = _make_token("supervisor")
        response = await async_client.put(
            f"/api/v1/fir/related-cases/{suggestion_id}/review",
            json={"ReviewStatus": "rejected", "ReviewReason": "False positive"},
            headers={"Authorization": f"Bearer {sup_token}"},
        )
        assert response.status_code == 200
        assert response.json()["reviewStatus"] == "rejected"

    @pytest.mark.asyncio
    async def test_review_invalid_suggestion_id(self, async_client: AsyncClient):
        token = _make_token("supervisor")
        response = await async_client.put(
            "/api/v1/fir/related-cases/99999/review",
            json={"ReviewStatus": "accepted"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_review_analyst_forbidden(self, async_client: AsyncClient, sample_firs):
        token = _make_token("analyst")
        gen_resp = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        suggestion_id = gen_resp.json()[0]["suggestionID"]

        response = await async_client.put(
            f"/api/v1/fir/related-cases/{suggestion_id}/review",
            json={"ReviewStatus": "accepted"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_review_viewer_forbidden(self, async_client: AsyncClient, sample_firs):
        token = _make_token("viewer")
        officer_token = _make_token("officer")
        gen_resp = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {officer_token}"},
        )
        suggestion_id = gen_resp.json()[0]["suggestionID"]

        response = await async_client.put(
            f"/api/v1/fir/related-cases/{suggestion_id}/review",
            json={"ReviewStatus": "accepted"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_review_invalid_status_returns_422(self, async_client: AsyncClient, sample_firs):
        off_token = _make_token("officer")
        gen_resp = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {off_token}"},
        )
        suggestion_id = gen_resp.json()[0]["suggestionID"]

        sup_token = _make_token("supervisor")
        response = await async_client.put(
            f"/api/v1/fir/related-cases/{suggestion_id}/review",
            json={"ReviewStatus": "invalid_status"},
            headers={"Authorization": f"Bearer {sup_token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_generate_with_no_matching_signals(self, async_client: AsyncClient, sample_firs):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/fir/4/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        for item in data:
            assert item["sourceFIRID"] == 4

    @pytest.mark.asyncio
    async def test_list_after_review_shows_status(self, async_client: AsyncClient, sample_firs):
        off_token = _make_token("officer")
        gen_resp = await async_client.post(
            "/api/v1/fir/1/related-cases/generate",
            headers={"Authorization": f"Bearer {off_token}"},
        )
        suggestion_id = gen_resp.json()[0]["suggestionID"]

        sup_token = _make_token("supervisor")
        await async_client.put(
            f"/api/v1/fir/related-cases/{suggestion_id}/review",
            json={"ReviewStatus": "accepted", "ReviewReason": "Confirmed"},
            headers={"Authorization": f"Bearer {sup_token}"},
        )
        list_resp = await async_client.get(
            "/api/v1/fir/1/related-cases",
            headers={"Authorization": f"Bearer {sup_token}"},
        )
        reviewed = [s for s in list_resp.json() if s["suggestionID"] == suggestion_id]
        assert len(reviewed) == 1
        assert reviewed[0]["reviewStatus"] == "accepted"
        assert reviewed[0]["reviewReason"] == "Confirmed"

    @pytest.mark.asyncio
    async def test_generate_only_matches_crime_category(self, async_client: AsyncClient, sample_firs):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/fir/3/related-cases/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        for item in data:
            assert item["sourceFIRID"] == 3
