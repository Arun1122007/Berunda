import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

import pytest


@pytest.mark.asyncio
@pytest.mark.integration
class TestHealth:
    async def test_health_endpoint(self, async_client):
        resp = await async_client.get("/health")
        assert resp.status_code == 200

    async def test_readiness_endpoint(self, async_client):
        resp = await async_client.get("/ready")
        assert resp.status_code == 200

    async def test_api_status_endpoint(self, async_client):
        resp = await async_client.get("/api/v1/status")
        assert resp.status_code == 200
