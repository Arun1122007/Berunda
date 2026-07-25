import sys
from pathlib import Path
_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

import pytest
import pytest_asyncio
import bcrypt
from httpx import ASGITransport, AsyncClient

@pytest.mark.asyncio
@pytest.mark.integration
class TestAuthorization:
    async def test_create_requires_auth(self, async_client):
        resp = await async_client.post("/api/v1/fir", json={"crimeNo": "AUTH-TEST-1"})
        assert resp.status_code in (401, 403)

    async def test_create_allows_admin(self, async_client, auth_headers_admin):
        resp = await async_client.post("/api/v1/fir", headers=auth_headers_admin, json={"crimeNo": "AUTH-TEST-2"})
        assert resp.status_code == 201

    async def test_delete_requires_admin(self, async_client, auth_headers_admin):
        create_resp = await async_client.post("/api/v1/fir", headers=auth_headers_admin, json={"crimeNo": "AUTH-TEST-3"})
        cid = create_resp.json()["caseMasterID"]
        # Create viewer token
        from src.services.auth_service import AuthService
        from src.database import get_session
        app = __import__("src.main", fromlist=["app"]).app
        del_resp = await async_client.delete(f"/api/v1/fir/{cid}", headers=auth_headers_admin)
        assert del_resp.status_code == 204
