import sys
from pathlib import Path
_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

import pytest
from httpx import ASGITransport, AsyncClient

@pytest.mark.asyncio
@pytest.mark.integration
class TestFIRCRUD:
    async def test_list_firs_empty(self, async_client, auth_headers_admin):
        resp = await async_client.get("/api/v1/fir", headers=auth_headers_admin)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 0
        assert "items" in data
        assert "page" in data

    async def test_create_fir(self, async_client, auth_headers_admin):
        resp = await async_client.post("/api/v1/fir", headers=auth_headers_admin, json={
            "crimeNo": "CR-2026-TEST001"
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["crimeNo"] == "CR-2026-TEST001"
        assert "caseMasterID" in data

    async def test_create_and_retrieve(self, async_client, auth_headers_admin):
        create_resp = await async_client.post("/api/v1/fir", headers=auth_headers_admin, json={
            "crimeNo": "CR-2026-TEST002"
        })
        cid = create_resp.json()["caseMasterID"]
        get_resp = await async_client.get(f"/api/v1/fir/{cid}", headers=auth_headers_admin)
        assert get_resp.status_code == 200
        assert get_resp.json()["crimeNo"] == "CR-2026-TEST002"

    async def test_get_nonexistent_returns_404(self, async_client, auth_headers_admin):
        resp = await async_client.get("/api/v1/fir/99999", headers=auth_headers_admin)
        assert resp.status_code == 404

    async def test_create_without_auth_returns_401(self, async_client):
        resp = await async_client.post("/api/v1/fir", json={"crimeNo": "CR-2026-NOAUTH"})
        assert resp.status_code == 401
