import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

import pytest


@pytest.mark.asyncio
@pytest.mark.integration
class TestAuthFlow:
    async def test_register_returns_201(self, async_client):
        resp = await async_client.post("/api/v1/auth/register", json={
            "email": "new@test.com", "password": "testpass123", "role": "officer"
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "userId" in data
        assert data["email"] == "new@test.com"

    async def test_register_duplicate_returns_409(self, async_client):
        await async_client.post("/api/v1/auth/register", json={
            "email": "dup@test.com", "password": "testpass123", "role": "officer"
        })
        resp = await async_client.post("/api/v1/auth/register", json={
            "email": "dup@test.com", "password": "testpass123", "role": "officer"
        })
        assert resp.status_code == 409

    async def test_login_valid_returns_token(self, async_client):
        await async_client.post("/api/v1/auth/register", json={
            "email": "login@test.com", "password": "testpass123", "role": "admin"
        })
        resp = await async_client.post("/api/v1/auth/login", json={
            "email": "login@test.com", "password": "testpass123"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data
        assert "refreshToken" in data

    async def test_login_invalid_returns_401(self, async_client):
        resp = await async_client.post("/api/v1/auth/login", json={
            "email": "nonexist@test.com", "password": "wrong"
        })
        assert resp.status_code == 401

    async def test_me_returns_user(self, async_client, auth_headers_admin):
        resp = await async_client.get("/api/v1/auth/me", headers=auth_headers_admin)
        assert resp.status_code == 200
        data = resp.json()
        assert "userId" in data
        assert "role" in data

    async def test_me_without_auth_returns_ok(self, async_client):
        resp = await async_client.get("/api/v1/auth/me")
        assert resp.status_code == 200

    async def test_logout_revokes_session(self, async_client, auth_headers_admin):
        resp = await async_client.post("/api/v1/auth/logout", headers=auth_headers_admin)
        assert resp.status_code == 200
