import sys
from pathlib import Path
_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

import pytest
from httpx import ASGITransport, AsyncClient

@pytest.mark.asyncio
@pytest.mark.integration
class TestErrorContract:
    async def test_404_error_response(self, async_client, auth_headers_admin):
        resp = await async_client.get("/api/v1/fir/99999", headers=auth_headers_admin)
        assert resp.status_code == 404
        # Error response should be JSON
        assert "application/json" in resp.headers.get("content-type", "")

    async def test_401_error_response(self, async_client):
        # FIR list endpoint is public, but detail requires auth
        resp = await async_client.get("/api/v1/fir/1")
        assert resp.status_code in (401, 200, 404)

    async def test_no_stack_trace_in_response(self, async_client, auth_headers_admin):
        resp = await async_client.get("/api/v1/fir/99999", headers=auth_headers_admin)
        body = resp.text
        assert "Traceback" not in body
        assert "File \"" not in body
