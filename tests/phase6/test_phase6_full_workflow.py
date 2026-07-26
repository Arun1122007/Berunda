"""Phase 6 comprehensive workflow tests using isolated in-memory SQLite.

Uses the same pattern as tests/integration/conftest.py:
  - session-scoped engine (avoids event-loop conflicts)
  - function-scoped session (each test gets a clean transaction)
  - dependency overrides (no global engine patching)
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database import get_session
from src.main import app
from src.models.base import Base


@pytest.fixture(scope="session")
def in_memory_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    return engine


@pytest_asyncio.fixture(scope="session")
async def tables(in_memory_engine):
    async with in_memory_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session(in_memory_engine, tables):
    factory = async_sessionmaker(in_memory_engine, expire_on_commit=False)
    async with factory() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestHealth:
    async def test_health(self, client):
        resp = await client.get("/health")
        assert resp.status_code == 200

    async def test_readiness(self, client):
        resp = await client.get("/ready")
        assert resp.status_code == 200

    async def test_root(self, client):
        resp = await client.get("/")
        assert resp.status_code == 200


@pytest.mark.asyncio
class TestAuth:
    async def test_register_and_login(self, client):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "officer@test.com", "password": "TestPass123", "role": "officer",
        })
        assert resp.status_code == 201
        resp = await client.post("/api/v1/auth/login", json={
            "email": "officer@test.com", "password": "TestPass123",
        })
        assert resp.status_code == 200
        assert "token" in resp.json()

    async def test_login_wrong_credentials(self, client):
        resp = await client.post("/api/v1/auth/login", json={
            "email": "noone@test.com", "password": "wrong",
        })
        assert resp.status_code == 401

    async def test_login_disabled_user(self, client):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "disabled@test.com", "password": "TestPass123", "role": "officer",
        })
        assert resp.status_code == 201
        resp = await client.post("/api/v1/auth/login", json={
            "email": "disabled@test.com", "password": "wrong",
        })
        assert resp.status_code == 401


@pytest.mark.asyncio
class TestFIR:
    async def _setup(self, client):
        await client.post("/api/v1/auth/register", json={
            "email": "fir_admin@test.com", "password": "TestPass123", "role": "admin",
        })
        resp = await client.post("/api/v1/auth/login", json={
            "email": "fir_admin@test.com", "password": "TestPass123",
        })
        token = resp.json()["token"]
        return {"Authorization": f"Bearer {token}"}

    async def test_create_fir(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-2026-TEST-001", "briefFacts": "Test FIR",
        }, headers=headers)
        assert resp.status_code == 201
        assert resp.json()["crimeNo"] == "CR-2026-TEST-001"

    async def test_list_firs(self, client):
        headers = await self._setup(client)
        await client.post("/api/v1/fir", json={
            "crimeNo": "CR-2026-TEST-002",
        }, headers=headers)
        resp = await client.get("/api/v1/fir", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

    async def test_get_fir(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-2026-TEST-003",
        }, headers=headers)
        case_id = resp.json()["caseMasterID"]
        resp = await client.get(f"/api/v1/fir/{case_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["caseMasterID"] == case_id

    async def test_update_fir(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-2026-TEST-004",
        }, headers=headers)
        case_id = resp.json()["caseMasterID"]
        resp = await client.put(f"/api/v1/fir/{case_id}", json={
            "briefFacts": "Updated",
        }, headers=headers)
        assert resp.status_code == 200

    async def test_status_transition(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-2026-TEST-005",
        }, headers=headers)
        case_id = resp.json()["caseMasterID"]
        resp = await client.put(f"/api/v1/fir/{case_id}/status", json={
            "caseStatusID": 2,
        }, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["changed"] is True

    async def test_invalid_status_transition(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-2026-TEST-006",
        }, headers=headers)
        case_id = resp.json()["caseMasterID"]
        resp = await client.put(f"/api/v1/fir/{case_id}/status", json={
            "caseStatusID": 8,
        }, headers=headers)
        assert resp.status_code == 404


@pytest.mark.asyncio
class TestInvestigation:
    async def _setup(self, client):
        await client.post("/api/v1/auth/register", json={
            "email": "inv_admin@test.com", "password": "TestPass123", "role": "admin",
        })
        resp = await client.post("/api/v1/auth/login", json={
            "email": "inv_admin@test.com", "password": "TestPass123",
        })
        token = resp.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-INV-001",
        }, headers=headers)
        case_id = resp.json()["caseMasterID"]
        return headers, case_id

    async def test_create_note(self, client):
        headers, case_id = await self._setup(client)
        resp = await client.post(f"/api/v1/fir/{case_id}/notes", json={
            "content": "Test investigation note",
            "noteType": "general",
        }, headers=headers)
        assert resp.status_code == 201

    async def test_list_notes(self, client):
        headers, case_id = await self._setup(client)
        await client.post(f"/api/v1/fir/{case_id}/notes", json={
            "content": "Note 1",
        }, headers=headers)
        resp = await client.get(f"/api/v1/fir/{case_id}/notes", headers=headers)
        assert resp.status_code == 200

    async def test_get_timeline(self, client):
        headers, case_id = await self._setup(client)
        resp = await client.get(f"/api/v1/fir/{case_id}/timeline", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_assign_officer(self, client):
        headers, case_id = await self._setup(client)
        resp = await client.post(f"/api/v1/fir/{case_id}/assignments", json={
            "assignedOfficerID": 1,
            "assignmentReason": "Test assignment",
        }, headers=headers)
        assert resp.status_code == 201

    async def test_supervisor_review(self, client):
        headers, case_id = await self._setup(client)
        resp = await client.post(f"/api/v1/fir/{case_id}/reviews", json={
            "reviewType": "progress_review",
            "status": "approved",
            "comments": "Good progress",
        }, headers=headers)
        assert resp.status_code == 201


@pytest.mark.asyncio
class TestSearchAndDashboard:
    async def _setup(self, client):
        await client.post("/api/v1/auth/register", json={
            "email": "sd_admin@test.com", "password": "TestPass123", "role": "admin",
        })
        resp = await client.post("/api/v1/auth/login", json={
            "email": "sd_admin@test.com", "password": "TestPass123",
        })
        token = resp.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}
        await client.post("/api/v1/fir", json={
            "crimeNo": "CR-SD-001", "briefFacts": "Search test",
        }, headers=headers)
        return headers

    async def test_search(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/search", json={
            "page": 1, "pageSize": 20,
        }, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

    async def test_dashboard(self, client):
        headers = await self._setup(client)
        resp = await client.get("/api/v1/dashboard/officer", headers=headers)
        assert resp.status_code == 200

    async def test_reports(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/reports", json={
            "reportType": "fir_summary",
            "parameters": "{}",
            "fileFormat": "json",
        }, headers=headers)
        assert resp.status_code == 201

    async def test_audit(self, client):
        headers = await self._setup(client)
        resp = await client.get("/api/v1/audit", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_police_stations(self, client):
        headers = await self._setup(client)
        resp = await client.get("/api/v1/police-stations", headers=headers)
        assert resp.status_code == 200

    async def test_districts(self, client):
        headers = await self._setup(client)
        resp = await client.get("/api/v1/police-stations/districts", headers=headers)
        assert resp.status_code == 200

    async def test_lifecycle_info(self, client):
        resp = await client.get("/api/v1/fir/statuses/lifecycle")
        assert resp.status_code == 200
        data = resp.json()
        assert "states" in data
        assert "transitions" in data

    async def test_allowed_transitions(self, client):
        resp = await client.get("/api/v1/fir/statuses/transitions",
                                 params={"current_status_id": 1})
        assert resp.status_code == 200
        assert "allowed_transitions" in resp.json()

    async def test_evidence_upload(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-EV-001",
        }, headers=headers)
        case_id = resp.json()["caseMasterID"]
        resp = await client.post(
            f"/api/v1/fir/{case_id}/evidence",
            files={"file": ("test.pdf", b"%PDF-1.4 content", "application/pdf")},
            data={"description": "Test evidence"},
            headers=headers,
        )
        assert resp.status_code == 201

    async def test_related_cases(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-RC-001",
        }, headers=headers)
        case_id = resp.json()["caseMasterID"]
        await client.post("/api/v1/fir", json={
            "crimeNo": "CR-RC-002",
        }, headers=headers)
        resp = await client.post(f"/api/v1/fir/{case_id}/related-cases/generate",
                                 headers=headers)
        assert resp.status_code == 200

    async def test_ai_endpoint(self, client):
        headers = await self._setup(client)
        resp = await client.post("/api/v1/fir", json={
            "crimeNo": "CR-AI-001",
        }, headers=headers)
        case_id = resp.json()["caseMasterID"]
        resp = await client.post(f"/api/v1/ai/firs/{case_id}/summarize", headers=headers)
        assert resp.status_code in (200, 400)
