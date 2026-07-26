import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

import pytest


@pytest.mark.asyncio
@pytest.mark.integration
class TestCORS:
    async def test_security_headers_present(self, async_client):
        resp = await async_client.get("/health")
        headers = resp.headers
        assert "x-content-type-options" in headers
        assert headers["x-content-type-options"] == "nosniff"

    async def test_frame_options_deny(self, async_client):
        resp = await async_client.get("/health")
        assert resp.headers.get("x-frame-options") == "DENY"
