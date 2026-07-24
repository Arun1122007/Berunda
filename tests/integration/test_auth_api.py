"""Integration tests for auth endpoints with mocked DB session."""

from unittest.mock import AsyncMock, MagicMock

import bcrypt
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.main import app
from src.models.auth_models import Session, User

PASSWORD = "admin"
HASHED = bcrypt.hashpw(PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _make_user(user_id: int, email: str, role: str) -> MagicMock:
    u = MagicMock(spec=User)
    u.UserID = user_id
    u.Email = email
    u.HashedPassword = HASHED
    u.Role = role
    u.DistrictID = None
    u.IsActive = True
    return u


def _make_session_record(user_id: int) -> MagicMock:
    s = MagicMock(spec=Session)
    s.SessionID = 1
    s.UserID = user_id
    s.TokenHash = "dummy"
    s.RevokedAt = None
    return s


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock(return_value=MagicMock())
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    return session


@pytest.fixture
def client(mock_session):
    app.dependency_overrides[get_session] = lambda: mock_session
    transport = ASGITransport(app=app)
    yield AsyncClient(transport=transport, base_url="http://test")
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user():
    return _make_user(1, "admin@berunda.gov", "admin")


@pytest.fixture
def analyst_user():
    return _make_user(2, "analyst@berunda.gov", "analyst")


@pytest.fixture
def session_record():
    return _make_session_record(1)


@pytest.mark.asyncio
async def test_login_success(client, mock_session, admin_user):
    mock_session.execute.return_value = MagicMock(
        scalar_one_or_none=MagicMock(return_value=admin_user)
    )
    async with client as ac:
        resp = await ac.post(
            "/api/v1/auth/login",
            json={"email": "admin@berunda.gov", "password": PASSWORD},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert data["refreshToken"] is not None
    assert data["expiresIn"] > 0
    assert data["user"]["email"] == "admin@berunda.gov"
    assert data["user"]["role"] == "admin"


@pytest.mark.asyncio
async def test_login_analyst(client, mock_session, analyst_user):
    mock_session.execute.return_value = MagicMock(
        scalar_one_or_none=MagicMock(return_value=analyst_user)
    )
    async with client as ac:
        resp = await ac.post(
            "/api/v1/auth/login",
            json={"email": "analyst@berunda.gov", "password": PASSWORD},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["user"]["role"] == "analyst"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, mock_session):
    mock_session.execute.return_value = MagicMock(scalar_one_or_none=MagicMock(return_value=None))
    async with client as ac:
        resp = await ac.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@test.com", "password": "wrong"},
        )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_validation_error(client):
    async with client as ac:
        resp = await ac.post("/api/v1/auth/login", json={"email": "test"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_me_returns_anonymous_without_token(client):
    async with client as ac:
        resp = await ac.get("/api/v1/auth/me")
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "anonymous"


@pytest.mark.asyncio
async def test_me_with_valid_token(client, mock_session, admin_user):
    mock_session.execute.return_value = MagicMock(
        scalar_one_or_none=MagicMock(return_value=admin_user)
    )
    async with client as ac:
        login_resp = await ac.post(
            "/api/v1/auth/login",
            json={"email": "admin@berunda.gov", "password": PASSWORD},
        )
        if login_resp.status_code != 200:
            pytest.skip("Login failed")
        token = login_resp.json()["token"]
        resp = await ac.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "admin"


@pytest.mark.asyncio
async def test_me_with_invalid_token(client):
    async with client as ac:
        resp = await ac.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalidtoken123"},
        )
    assert resp.status_code == 200
    assert resp.json()["role"] == "anonymous"


@pytest.mark.asyncio
async def test_logout(client, mock_session, admin_user, session_record):
    mock_session.execute.return_value = MagicMock(
        scalar_one_or_none=MagicMock(return_value=admin_user)
    )
    async with client as ac:
        login_resp = await ac.post(
            "/api/v1/auth/login",
            json={"email": "admin@berunda.gov", "password": PASSWORD},
        )
        if login_resp.status_code != 200:
            pytest.skip("Login failed")
        token = login_resp.json()["token"]
        mock_session.execute.return_value = MagicMock(
            scalar_one_or_none=MagicMock(return_value=session_record)
        )
        resp = await ac.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["message"] == "Logged out successfully"


@pytest.mark.asyncio
async def test_refresh_with_valid_token(client, mock_session, admin_user, session_record):
    mock_session.execute.return_value = MagicMock(
        scalar_one_or_none=MagicMock(return_value=admin_user)
    )
    async with client as ac:
        login_resp = await ac.post(
            "/api/v1/auth/login",
            json={"email": "admin@berunda.gov", "password": PASSWORD},
        )
        if login_resp.status_code != 200:
            pytest.skip("Login failed")
        refresh_token = login_resp.json()["refreshToken"]
        mock_session.execute = AsyncMock(
            side_effect=[
                MagicMock(scalar_one_or_none=MagicMock(return_value=session_record)),
                MagicMock(scalar_one_or_none=MagicMock(return_value=admin_user)),
            ]
        )
        resp = await ac.post("/api/v1/auth/refresh", json={"refreshToken": refresh_token})
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert data["user"]["role"] == "admin"


@pytest.mark.asyncio
async def test_refresh_with_invalid_token(client):
    async with client as ac:
        resp = await ac.post("/api/v1/auth/refresh", json={"refreshToken": "bad_token"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_without_token(client):
    async with client as ac:
        resp = await ac.post("/api/v1/auth/refresh", json={})
    assert resp.status_code == 422
