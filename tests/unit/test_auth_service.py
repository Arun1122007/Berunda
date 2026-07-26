"""Unit tests for AuthService — uses mocked session."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import bcrypt
import pytest

from src.exceptions import AuthenticationError, ConflictError
from src.repositories.sqlite_adapter import SQLiteAuthRepository
from src.services.auth_service import AuthService


class AsyncMockSession:
    def __init__(self, user=None):
        self.execute = AsyncMock()
        self.get = AsyncMock()
        self.flush = AsyncMock()
        self.commit = AsyncMock()
        self.refresh = AsyncMock()
        self.add = MagicMock()
        self.delete = AsyncMock()
        self._user = user

    def _make_scalar_result(self, value):
        m = MagicMock()
        m.scalar_one_or_none.return_value = value
        m.scalar_one.return_value = value if value is not None else 0
        m.scalars.return_value.all.return_value = value if isinstance(value, list) else []
        return m


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.UserID = 1
    user.Email = "test@example.com"
    user.Role = "officer"
    user.IsActive = True
    user.DistrictID = None
    user.HashedPassword = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode("utf-8")
    return user


@pytest.mark.unit
class TestAuthService:
    @pytest.mark.asyncio
    async def test_register_creates_user(self, mock_user):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(None)
        session.refresh.side_effect = lambda u: setattr(u, "UserID", 1)

        service = AuthService(SQLiteAuthRepository(session))
        user = await service.register("test@example.com", "password123", "officer", None)
        assert user is not None
        session.add.assert_called_once()
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_duplicate_email_raises(self, mock_user):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(mock_user)

        service = AuthService(SQLiteAuthRepository(session))
        with pytest.raises(ConflictError):
            await service.register("test@example.com", "password123", "admin", None)

    @pytest.mark.asyncio
    async def test_authenticate_valid_returns_tokens(self, mock_user):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(mock_user)

        service = AuthService(SQLiteAuthRepository(session))
        user, access, refresh = await service.authenticate("test@example.com", "password123")
        assert user is not None
        assert access is not None
        assert refresh is not None

    @pytest.mark.asyncio
    async def test_authenticate_invalid_password_raises(self, mock_user):
        session = AsyncMockSession()
        # Wrong password hash
        user = MagicMock()
        user.Email = "test@example.com"
        user.IsActive = True
        user.HashedPassword = bcrypt.hashpw(b"otherPass", bcrypt.gensalt()).decode("utf-8")
        session.execute.return_value = session._make_scalar_result(user)

        service = AuthService(SQLiteAuthRepository(session))
        with pytest.raises(AuthenticationError):
            await service.authenticate("test@example.com", "wrongPassword")

    @pytest.mark.asyncio
    async def test_authenticate_nonexistent_user_raises(self):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(None)

        service = AuthService(SQLiteAuthRepository(session))
        with pytest.raises(AuthenticationError):
            await service.authenticate("nobody@test.com", "password123")

    @pytest.mark.asyncio
    async def test_get_user_profile_returns_dict(self, mock_user):
        session = AsyncMockSession()
        # First call (user lookup) returns user, second call (district) returns None
        session.execute.return_value = session._make_scalar_result(mock_user)

        service = AuthService(SQLiteAuthRepository(session))
        profile = await service.get_user_profile(1)
        assert profile is not None
        assert profile["email"] == "test@example.com"
        assert profile["role"] == "officer"

    @pytest.mark.asyncio
    async def test_get_user_profile_nonexistent_returns_none(self):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(None)

        service = AuthService(SQLiteAuthRepository(session))
        profile = await service.get_user_profile(99999)
        assert profile is None
