"""Integration tests for Investigation API endpoints."""

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
async def sample_fir(db_session):
    from datetime import date
    from src.models.src_models import CaseMaster

    fir = CaseMaster(CrimeNo="CR-2026-TST-001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 15))
    db_session.add(fir)
    await db_session.commit()
    await db_session.refresh(fir)
    return fir


@pytest.mark.integration
class TestInvestigationAPI:
    @pytest.mark.asyncio
    async def test_create_note_success(self, async_client: AsyncClient, sample_fir):
        token = _make_token("officer")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            json={
                "NoteType": "field_visit",
                "Content": "Visited the crime scene. Collected fingerprints from the rear door.",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Visited the crime scene. Collected fingerprints from the rear door."
        assert data["noteType"] == "field_visit"
        assert data["caseMasterID"] == sample_fir.CaseMasterID

    @pytest.mark.asyncio
    async def test_create_note_no_auth_returns_401(self, async_client: AsyncClient, sample_fir):
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            json={"NoteType": "general", "Content": "Test note"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_note_viewer_forbidden(self, async_client: AsyncClient, sample_fir):
        token = _make_token("viewer")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            json={"NoteType": "general", "Content": "Test note"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_note_analyst_forbidden(self, async_client: AsyncClient, sample_fir):
        token = _make_token("analyst")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            json={"NoteType": "general", "Content": "Analyst note"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_note_invalid_fir_404(self, async_client: AsyncClient):
        token = _make_token("officer")
        response = await async_client.post(
            "/api/v1/fir/99999/notes",
            json={"NoteType": "general", "Content": "Note for non-existent FIR"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_note_invalid_returns_422(self, async_client: AsyncClient, sample_fir):
        token = _make_token("officer")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_list_notes_empty(self, async_client: AsyncClient, sample_fir):
        token = _make_token("officer")
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_list_notes_after_create(self, async_client: AsyncClient, sample_fir):
        token = _make_token("officer")
        await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            json={"NoteType": "witness_statement", "Content": "First note"},
            headers={"Authorization": f"Bearer {token}"},
        )
        await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            json={"NoteType": "field_visit", "Content": "Second note"},
            headers={"Authorization": f"Bearer {token}"},
        )
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/notes",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["content"] == "First note"
        assert data[0]["noteType"] == "witness_statement"
        assert data[1]["content"] == "Second note"

    @pytest.mark.asyncio
    async def test_assign_officer_success(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            json={"AssignedOfficerID": 42, "AssignmentReason": "Lead investigator"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["assignedOfficerID"] == 42
        assert data["caseMasterID"] == sample_fir.CaseMasterID
        assert data["assignedByUserID"] == 1

    @pytest.mark.asyncio
    async def test_assign_officer_analyst_forbidden(self, async_client: AsyncClient, sample_fir):
        token = _make_token("analyst")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            json={"AssignedOfficerID": 42},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_assign_officer_viewer_forbidden(self, async_client: AsyncClient, sample_fir):
        token = _make_token("viewer")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            json={"AssignedOfficerID": 42},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_assign_officer_no_auth_returns_401(self, async_client: AsyncClient, sample_fir):
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            json={"AssignedOfficerID": 42},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_list_assignments_after_create(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            json={"AssignedOfficerID": 42, "AssignmentReason": "Primary"},
            headers={"Authorization": f"Bearer {token}"},
        )
        await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            json={"AssignedOfficerID": 43, "AssignmentReason": "Secondary"},
            headers={"Authorization": f"Bearer {token}"},
        )
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["assignedOfficerID"] == 42

    @pytest.mark.asyncio
    async def test_list_assignments_empty(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_active_assignment_after_assign(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            json={"AssignedOfficerID": 42},
            headers={"Authorization": f"Bearer {token}"},
        )
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignment/active",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["assignedOfficerID"] == 42
        assert data["status"] == "active"

    @pytest.mark.asyncio
    async def test_get_active_assignment_not_found(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignment/active",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_update_status_success(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        old_id = sample_fir.CaseStatusID
        response = await async_client.put(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/status",
            json={"CaseStatusID": 2, "Reason": "Starting investigation"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["CaseMasterID"] == sample_fir.CaseMasterID
        assert data["NewStatusID"] == 2
        assert data["OldStatusID"] == old_id
        assert data["Changed"] is True

    @pytest.mark.asyncio
    async def test_update_status_viewer_forbidden(self, async_client: AsyncClient, sample_fir):
        token = _make_token("viewer")
        response = await async_client.put(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/status",
            json={"CaseStatusID": 2},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_status_no_auth_returns_401(self, async_client: AsyncClient, sample_fir):
        response = await async_client.put(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/status",
            json={"CaseStatusID": 2},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_update_status_same_status_no_change(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        await async_client.put(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/status",
            json={"CaseStatusID": 2},
            headers={"Authorization": f"Bearer {token}"},
        )
        response = await async_client.put(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/status",
            json={"CaseStatusID": 2, "Reason": "Same status"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["NewStatusID"] == 2
        assert data["OldStatusID"] == 2
        assert data["Changed"] is False

    @pytest.mark.asyncio
    async def test_update_status_invalid_case_status_id_422(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        response = await async_client.put(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/status",
            json={"CaseStatusID": 999},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_timeline_has_fir_registered_event(self, async_client: AsyncClient, sample_fir):
        token = _make_token("officer")
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/timeline",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["type"] == "FIR_REGISTERED"

    @pytest.mark.asyncio
    async def test_timeline_returns_200(self, async_client: AsyncClient, sample_fir):
        off_token = _make_token("officer")
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/timeline",
            headers={"Authorization": f"Bearer {off_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_create_review_success(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/reviews",
            json={
                "ReviewType": "periodic",
                "Status": "approved",
                "Comments": "Good progress on the case.",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "approved"
        assert data["comments"] == "Good progress on the case."
        assert data["caseMasterID"] == sample_fir.CaseMasterID

    @pytest.mark.asyncio
    async def test_create_review_officer_forbidden(self, async_client: AsyncClient, sample_fir):
        token = _make_token("officer")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/reviews",
            json={"ReviewType": "periodic", "Status": "approved"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_review_no_auth_returns_401(self, async_client: AsyncClient, sample_fir):
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/reviews",
            json={"ReviewType": "periodic", "Status": "approved"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_list_reviews_empty(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/reviews",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_list_reviews_after_create(self, async_client: AsyncClient, sample_fir):
        token = _make_token("supervisor")
        await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/reviews",
            json={
                "ReviewType": "correction_request",
                "Status": "correction_requested",
                "Comments": "Need more evidence",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        response = await async_client.get(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/reviews",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["comments"] == "Need more evidence"
        assert data[0]["status"] == "correction_requested"

    @pytest.mark.asyncio
    async def test_admin_can_assign(self, async_client: AsyncClient, sample_fir):
        token = _make_token("admin")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/assignments",
            json={"AssignedOfficerID": 7},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        assert response.json()["assignedOfficerID"] == 7

    @pytest.mark.asyncio
    async def test_admin_can_review(self, async_client: AsyncClient, sample_fir):
        token = _make_token("admin")
        response = await async_client.post(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/reviews",
            json={"ReviewType": "periodic", "Status": "approved"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        assert response.json()["status"] == "approved"

    @pytest.mark.asyncio
    async def test_admin_can_update_status(self, async_client: AsyncClient, sample_fir):
        token = _make_token("admin")
        response = await async_client.put(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/status",
            json={"CaseStatusID": 2},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["Changed"] is True

    @pytest.mark.asyncio
    async def test_update_status_analyst_forbidden(self, async_client: AsyncClient, sample_fir):
        token = _make_token("analyst")
        response = await async_client.put(
            f"/api/v1/fir/{sample_fir.CaseMasterID}/status",
            json={"CaseStatusID": 2},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
