from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.main import app


class AsyncContextManagerMock:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.get = AsyncMock()
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


def _make_mock_result(scalar_one_val=0, scalars_all=None):
    if scalars_all is None:
        scalars_all = []
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = scalars_all
    mock_result.scalar_one.return_value = scalar_one_val
    mock_result.scalar_one_or_none.return_value = None
    return mock_result


@pytest.mark.asyncio
async def test_fir_routes_registered(client, mock_session):
    mock_session.execute.return_value = _make_mock_result(scalars_all=[])
    resp = await client.get("/api/v1/fir")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_entity_routes_registered(client, mock_session):
    mock_session.execute.return_value = _make_mock_result(scalars_all=[])
    resp = await client.get("/api/v1/entities")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_graph_routes_registered(client, mock_session):
    mock_session.execute.return_value = _make_mock_result()
    resp = await client.get("/api/v1/graph")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_hotspot_routes_registered(client, mock_session):
    mock_session.execute.return_value = _make_mock_result(scalars_all=[])
    resp = await client.get("/api/v1/hotspots")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_anomaly_routes_registered(client, mock_session):
    mock_session.execute.return_value = _make_mock_result(scalars_all=[])
    resp = await client.get("/api/v1/anomalies")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_risk_routes_registered(client, mock_session):
    mock_session.execute.return_value = _make_mock_result(scalars_all=[])
    resp = await client.get("/api/v1/risk")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_audit_routes_requires_auth(client, mock_session):
    resp = await client.get("/api/v1/audit")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_auth_me_returns_anonymous(client, mock_session):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_rag_routes_registered(client, mock_session):
    mock_session.execute.return_value = _make_mock_result(scalars_all=[])
    resp = await client.post("/api/v1/rag/query", json={"query": "test"})
    assert resp.status_code in (200, 500)


@pytest.mark.asyncio
async def test_health_still_works(client, mock_session):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
