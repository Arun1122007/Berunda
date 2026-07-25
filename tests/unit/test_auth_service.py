"""Unit tests for AuthService."""

from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.exceptions import AuthenticationError, ConflictError
from src.models.base import Base
from src.models.auth_models import User
from src.services.auth_service import AuthService


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.mark.unit
class TestAuthService:
    async def test_register_creates_user(self, db_session: AsyncSession):
        service = AuthService(db_session)
        user = await service.register("test@example.com", "password123", "officer", None)
        assert user.Email == "test@example.com"
        assert user.Role == "officer"
        assert user.IsActive is True

    async def test_register_duplicate_email_raises(self, db_session: AsyncSession):
        service = AuthService(db_session)
        await service.register("dup@example.com", "password123", "admin", None)
        with pytest.raises(ConflictError):
            await service.register("dup@example.com", "password123", "analyst", None)

    async def test_authenticate_valid_returns_tokens(self, db_session: AsyncSession):
        service = AuthService(db_session)
        await service.register("auth@test.com", "securePass1", "analyst", None)
        user, access_token, refresh_token = await service.authenticate(
            "auth@test.com", "securePass1"
        )
        assert user is not None
        assert access_token is not None
        assert refresh_token is not None
        assert len(access_token) > 0
        assert len(refresh_token) > 0

    async def test_authenticate_invalid_password_raises(self, db_session: AsyncSession):
        service = AuthService(db_session)
        await service.register("bad@test.com", "goodPassword", "officer", None)
        with pytest.raises(AuthenticationError):
            await service.authenticate("bad@test.com", "wrongPassword")

    async def test_authenticate_nonexistent_user_raises(self, db_session: AsyncSession):
        service = AuthService(db_session)
        with pytest.raises(AuthenticationError):
            await service.authenticate("nobody@test.com", "password123")

    async def test_get_user_profile_returns_dict(self, db_session: AsyncSession):
        service = AuthService(db_session)
        user = await service.register("profile@test.com", "password123", "admin", None)
        profile = await service.get_user_profile(user.UserID)
        assert profile is not None
        assert profile["email"] == "profile@test.com"
        assert profile["role"] == "admin"

    async def test_get_user_profile_nonexistent_returns_none(self, db_session: AsyncSession):
        service = AuthService(db_session)
        profile = await service.get_user_profile(99999)
        assert profile is None
