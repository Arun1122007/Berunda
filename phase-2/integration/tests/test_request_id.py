import sys
from pathlib import Path
_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

import pytest
from httpx import ASGITransport, AsyncClient

@pytest.mark.asyncio
@pytest.mark.integration
class TestRequestID:
    async def test_response_has_request_id(self, async_client):
        resp = await async_client.get("/health")
        assert "x-request-id" in resp.headers

    async def test_custom_request_id_is_preserved(self, async_client):
        custom_id = "my-custom-id-12345"
        resp = await async_client.get("/health", headers={"X-Request-ID": custom_id})
        assert resp.headers.get("x-request-id") == custom_id

    async def test_request_id_in_error_response(self, async_client):
        resp = await async_client.get("/api/v1/nonexistent")
        assert "x-request-id" in resp.headers
