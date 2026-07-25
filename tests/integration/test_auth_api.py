"""Integration tests for Auth API endpoints."""

from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database import get_session
from src.main import app
from src.models.base import Base


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

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.mark.integration
class TestAuthAPI:
    async def test_register_returns_201(self, async_client: AsyncClient):
        response = await async_client.post(
            "/api/v1/auth/register",
            json={
                "email": "new@test.com",
                "password": "password123",
                "role": "officer",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@test.com"
        assert data["role"] == "officer"

    async def test_register_duplicate_returns_409(self, async_client: AsyncClient):
        await async_client.post(
            "/api/v1/auth/register",
            json={"email": "dup@test.com", "password": "password123"},
        )
        response = await async_client.post(
            "/api/v1/auth/register",
            json={"email": "dup@test.com", "password": "password123"},
        )
        assert response.status_code == 409

    async def test_login_valid_returns_token(self, async_client: AsyncClient):
        await async_client.post(
            "/api/v1/auth/register",
            json={"email": "login@test.com", "password": "testPass123"},
        )
        response = await async_client.post(
            "/api/v1/auth/login",
            json={"email": "login@test.com", "password": "testPass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "refreshToken" in data
        assert len(data["token"]) > 0

    async def test_login_invalid_returns_401(self, async_client: AsyncClient):
        response = await async_client.post(
            "/api/v1/auth/login",
            json={"email": "wrong@test.com", "password": "wrong"},
        )
        assert response.status_code == 401

    async def test_get_me_returns_user(self, async_client: AsyncClient):
        await async_client.post(
            "/api/v1/auth/register",
            json={"email": "me@test.com", "password": "testPass123", "role": "analyst"},
        )
        login_resp = await async_client.post(
            "/api/v1/auth/login",
            json={"email": "me@test.com", "password": "testPass123"},
        )
        token = login_resp.json()["token"]

        response = await async_client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "me@test.com"

    async def test_me_without_auth_returns_ok(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/auth/me")
        assert response.status_code == 200

    async def test_logout_revokes_session(self, async_client: AsyncClient):
        await async_client.post(
            "/api/v1/auth/register",
            json={"email": "logout@test.com", "password": "testPass123"},
        )
        login_resp = await async_client.post(
            "/api/v1/auth/login",
            json={"email": "logout@test.com", "password": "testPass123"},
        )
        token = login_resp.json()["token"]

        response = await async_client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
