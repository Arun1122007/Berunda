"""Integration tests for Catalyst Webhook API endpoints."""

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
from src.services.webhook_service import get_webhook_service


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


@pytest.fixture(autouse=True)
def clear_webhook_store():
    service = get_webhook_service()
    service._webhooks.clear()
    service._delivery_log.clear()
    yield
    service._webhooks.clear()
    service._delivery_log.clear()


@pytest.mark.integration
class TestWebhookAPI:
    @pytest.mark.asyncio
    async def test_register_and_list_webhooks(self, async_client: AsyncClient):
        token = _make_token("admin")
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "url": "https://catalyst.zoho.com/test-endpoint",
            "events": ["case.assigned", "evidence.uploaded"],
            "secret": "supersecretkey123",
            "description": "Zoho Catalyst Production Receiver"
        }

        # Register webhook
        response = await async_client.post("/api/v1/webhooks", json=payload, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "createdAt" in data
        assert "successCount" in data
        assert "failureCount" in data
        assert data["url"] == payload["url"]
        assert data["events"] == payload["events"]
        assert data["active"] is True

        webhook_id = data["id"]

        # List webhooks
        list_resp = await async_client.get("/api/v1/webhooks", headers=headers)
        assert list_resp.status_code == 200
        list_data = list_resp.json()
        assert len(list_data) == 1
        assert list_data[0]["id"] == webhook_id

    @pytest.mark.asyncio
    async def test_test_dispatch_webhook(self, async_client: AsyncClient):
        token = _make_token("supervisor")
        headers = {"Authorization": f"Bearer {token}"}

        # Register webhook with simulated target
        payload = {
            "url": "catalyst://simulated-target",
            "events": ["case.assigned"],
            "secret": "hmac_secret"
        }
        await async_client.post("/api/v1/webhooks", json=payload, headers=headers)

        # Trigger test dispatch
        dispatch_payload = {
            "eventType": "case.assigned",
            "payload": {"assignmentId": 101, "caseMasterId": 500, "assignedOfficerId": 42}
        }
        dispatch_resp = await async_client.post("/api/v1/webhooks/test-dispatch", json=dispatch_payload, headers=headers)
        assert dispatch_resp.status_code == 200
        logs = dispatch_resp.json()
        assert len(logs) >= 1
        assert logs[0]["eventType"] == "case.assigned"
        assert logs[0]["status"] in ("success", "failed")

    @pytest.mark.asyncio
    async def test_unregister_webhook(self, async_client: AsyncClient):
        token = _make_token("admin")
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "url": "https://catalyst.zoho.com/to-delete",
            "events": ["supervisor.review.created"]
        }
        reg_resp = await async_client.post("/api/v1/webhooks", json=payload, headers=headers)
        webhook_id = reg_resp.json()["id"]

        # Delete webhook
        del_resp = await async_client.delete(f"/api/v1/webhooks/{webhook_id}", headers=headers)
        assert del_resp.status_code == 204

        # Delete non-existent
        del_resp2 = await async_client.delete(f"/api/v1/webhooks/{webhook_id}", headers=headers)
        assert del_resp2.status_code == 404
