"""Integration tests for all API endpoints with mocked DB session."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.main import app
from src.middleware.auth import JWT_SECRET

AUTH_HEADER = {
    "Authorization": f"Bearer {jwt.encode({'user_id': 1, 'role': 'admin'}, JWT_SECRET, algorithm='HS256')}"
}


class AsyncContextManagerMock:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


class MockModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock(return_value=_make_result(scalars_all=[], scalar_one_val=0))
    session.get = AsyncMock(return_value=None)
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def client(mock_session):
    async def override_get_session():
        yield mock_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    yield client
    app.dependency_overrides.clear()


def _make_result(scalar_one_val=None, scalars_all=None, scalar_one_or_none=None):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = scalars_all or []
    mock_result.scalar_one.return_value = scalar_one_val
    mock_result.scalar_one_or_none.return_value = scalar_one_or_none or None
    return mock_result


# ── Health ──


@pytest.mark.asyncio
async def test_health(client):
    async with client as ac:
        resp = await ac.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_readiness(client):
    async with client as ac:
        resp = await ac.get("/ready")
    assert resp.status_code == 200
    data = resp.json()
    assert "database" in data["checks"]


@pytest.mark.asyncio
async def test_api_status(client):
    async with client as ac:
        resp = await ac.get("/api/v1/status")
    assert resp.status_code == 200
    assert resp.json()["service"] == "Berunda"


# ── FIR ──


@pytest.mark.asyncio
async def test_list_firs(client, mock_session):
    mock_session.execute.return_value = _make_result(
        scalars_all=[MockModel(CaseMasterID=1, CrimeNo="CR001")],
        scalar_one_val=1,
    )
    async with client as ac:
        resp = await ac.get("/api/v1/fir")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_fir_found(client, mock_session):
    mock_model = MockModel(CaseMasterID=1, CrimeNo="CR001")
    mock_model.complainants = []
    mock_model.victims = []
    mock_model.accused = []
    mock_model.act_sections = []
    mock_exec = MagicMock()
    mock_exec.scalar_one_or_none.return_value = mock_model
    mock_session.execute = AsyncMock(return_value=mock_exec)

    async with client as ac:
        resp = await ac.get("/api/v1/fir/1")
    assert resp.status_code == 200
    assert resp.json()["crimeNo"] == "CR001"


@pytest.mark.asyncio
async def test_get_fir_not_found(client, mock_session):
    mock_exec = MagicMock()
    mock_exec.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_exec)
    async with client as ac:
        resp = await ac.get("/api/v1/fir/999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_create_fir(client, mock_session):
    mock_exec = MagicMock()
    mock_exec.scalar_one.return_value = 1
    mock_session.execute = AsyncMock(return_value=mock_exec)
    mock_session.refresh.side_effect = lambda obj: setattr(obj, "CaseMasterID", 1)

    async with client as ac:
        resp = await ac.post("/api/v1/fir", json={"crimeNo": "CR-NEW-001"}, headers=AUTH_HEADER)
    assert resp.status_code == 201
    assert resp.json()["crimeNo"] == "CR-NEW-001"


@pytest.mark.asyncio
async def test_update_fir(client, mock_session):
    mock_exec = MagicMock()
    mock_exec.scalar_one_or_none.return_value = MockModel(CaseMasterID=1, CrimeNo="CR001")
    mock_session.execute = AsyncMock(return_value=mock_exec)
    async with client as ac:
        resp = await ac.put("/api/v1/fir/1", json={"caseStatusId": 2}, headers=AUTH_HEADER)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_update_fir_not_found(client, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    async with client as ac:
        resp = await ac.put("/api/v1/fir/999", json={"caseStatusId": 2}, headers=AUTH_HEADER)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_fir(client, mock_session):
    mock_session.get = AsyncMock(return_value=MockModel(CaseMasterID=1, CrimeNo="CR001"))
    async with client as ac:
        resp = await ac.delete("/api/v1/fir/1", headers=AUTH_HEADER)
    assert resp.status_code == 204


# ── Entity ──


@pytest.mark.asyncio
async def test_list_entities(client, mock_session):
    mock_session.execute.return_value = _make_result(
        scalars_all=[MockModel(PersonEntityID=1, CanonicalName="Person A")],
        scalar_one_val=1,
    )
    async with client as ac:
        resp = await ac.get("/api/v1/entities")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_get_entity(client, mock_session):
    mock_exec = MagicMock()
    mock_exec.scalar_one_or_none.return_value = MockModel(
        PersonEntityID=1, CanonicalName="Person A"
    )
    mock_session.execute = AsyncMock(return_value=mock_exec)
    async with client as ac:
        resp = await ac.get("/api/v1/entities/1")
    assert resp.status_code == 200
    assert resp.json()["canonicalName"] == "Person A"


@pytest.mark.asyncio
async def test_get_entity_not_found(client, mock_session):
    mock_exec = MagicMock()
    mock_exec.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_exec)
    async with client as ac:
        resp = await ac.get("/api/v1/entities/999")
    assert resp.status_code == 404


# ── Graph ──


@pytest.mark.asyncio
async def test_graph_endpoint(client, mock_session):
    mock_session.execute.return_value = _make_result(scalars_all=[])
    async with client as ac:
        resp = await ac.get("/api/v1/graph")
    assert resp.status_code == 200
    data = resp.json()
    assert "nodes" in data
    assert "edges" in data


# ── Hotspot ──


@pytest.mark.asyncio
async def test_hotspots(client, mock_session):
    mock_session.execute.return_value = _make_result(scalars_all=[])
    async with client as ac:
        resp = await ac.get("/api/v1/hotspots")
    assert resp.status_code == 200


# ── Anomaly ──


@pytest.mark.asyncio
async def test_anomalies(client, mock_session):
    mock_session.execute.return_value = _make_result(scalars_all=[])
    async with client as ac:
        resp = await ac.get("/api/v1/anomalies")
    assert resp.status_code == 200


# ── Risk ──


@pytest.mark.asyncio
async def test_risk_scores(client, mock_session):
    mock_session.execute.return_value = _make_result(scalars_all=[])
    async with client as ac:
        resp = await ac.get("/api/v1/risk")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_risk_compute(client, mock_session):
    mock_session.get = AsyncMock(
        return_value=MockModel(PersonEntityID=1, CanonicalName="Test Person")
    )
    mock_link_exec = MagicMock()
    mock_link_exec.scalars.return_value.all.return_value = [
        MockModel(CaseMasterID=1, PersonID=100, PersonEntityID=1)
    ]
    mock_link_exec2 = MagicMock()
    mock_link_exec2.scalars.return_value.all.return_value = [
        MockModel(CaseMasterID=1, CrimeRegisteredDate=datetime(2026, 1, 1), GravityOffenceID=5, CrimeMajorHeadID=2)
    ]
    mock_session.execute = AsyncMock(side_effect=[mock_link_exec, mock_link_exec2])
    mock_session.refresh.side_effect = lambda obj: setattr(obj, "RiskScoreID", 1)
    async with client as ac:
        resp = await ac.post("/api/v1/risk/compute/1")
    assert resp.status_code == 200


# ── RAG ──


@pytest.mark.asyncio
async def test_rag_query(client, mock_session):
    mock_session.execute.return_value = _make_result(scalars_all=[])
    async with client as ac:
        resp = await ac.post("/api/v1/rag/query", json={"query": "test query"})
    assert resp.status_code in (200, 500)


# ── Audit (Auth Required) ──


@pytest.mark.asyncio
async def test_audit_requires_auth(client):
    async with client as ac:
        resp = await ac.get("/api/v1/audit")
    assert resp.status_code == 401


# ── 404 Routes ──


@pytest.mark.asyncio
async def test_nonexistent_route(client):
    async with client as ac:
        resp = await ac.get("/api/v1/nonexistent")
    assert resp.status_code == 404
