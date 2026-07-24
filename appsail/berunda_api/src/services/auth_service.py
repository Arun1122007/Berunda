from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import select

from src.config import settings
from src.middleware.auth import JWT_ALGORITHM, JWT_SECRET
from src.models.auth_models import Session, User
from src.models.src_models import District
from src.services.base import BaseService

ACCESS_TOKEN_EXPIRY_MINUTES = settings.ACCESS_TOKEN_EXPIRY_MINUTES
REFRESH_TOKEN_EXPIRY_DAYS = settings.REFRESH_TOKEN_EXPIRY_DAYS


class AuthService(BaseService):
    async def authenticate(self, email: str, password: str) -> tuple[User, str, str]:
        result = await self.session.execute(select(User).where(User.Email == email))
        user = result.scalar_one_or_none()
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.HashedPassword.encode("utf-8")
        ):
            raise ValueError("Invalid credentials")
        if not user.IsActive:
            raise ValueError("Account is disabled")
        access_token, refresh_token = await self._issue_tokens(user)
        return user, access_token, refresh_token

    async def register(
        self, email: str, password: str, role: str = "officer", district_id: int | None = None
    ) -> User:
        existing = await self.session.execute(select(User).where(User.Email == email))
        if existing.scalar_one_or_none():
            raise ValueError("Email already registered")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(Email=email, HashedPassword=hashed, Role=role, DistrictID=district_id)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def refresh_token(self, token_str: str) -> tuple[str, str]:
        try:
            payload = jwt.decode(token_str, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Not a refresh token")

        token_suffix = token_str[-64:]
        result = await self.session.execute(
            select(Session).where(Session.TokenHash == token_suffix)
        )
        session_record = result.scalar_one_or_none()
        if not session_record or session_record.RevokedAt:
            raise ValueError("Session revoked or not found")

        user_result = await self.session.execute(
            select(User).where(User.UserID == session_record.UserID)
        )
        user = user_result.scalar_one_or_none()
        if not user or not user.IsActive:
            raise ValueError("User not found or disabled")

        session_record.RevokedAt = datetime.now(timezone.utc)
        access_token, refresh_token = await self._issue_tokens(user)
        return access_token, refresh_token

    async def revoke_session(self, token_str: str) -> None:
        token_suffix = token_str[-64:]
        result = await self.session.execute(
            select(Session).where(Session.TokenHash == token_suffix)
        )
        session_record = result.scalar_one_or_none()
        if session_record:
            session_record.RevokedAt = datetime.now(timezone.utc)
            await self.session.commit()

    async def get_user_profile(self, user_id: int) -> dict | None:
        result = await self.session.execute(select(User).where(User.UserID == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        district_name = None
        if user.DistrictID:
            d_result = await self.session.execute(
                select(District).where(District.DistrictID == user.DistrictID)
            )
            district = d_result.scalar_one_or_none()
            district_name = district.DistrictName if district else None
        return {
            "userId": user.UserID,
            "email": user.Email,
            "name": user.Email.split("@")[0],
            "role": user.Role,
            "district": district_name,
            "permissions": [],
        }

    async def _issue_tokens(self, user: User) -> tuple[str, str]:
        now = datetime.utcnow()
        access_payload = {
            "user_id": user.UserID,
            "role": user.Role,
            "district_id": user.DistrictID,
            "type": "access",
            "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES),
            "iat": now,
            "jti": str(uuid.uuid4()),
        }
        refresh_payload = {
            "user_id": user.UserID,
            "role": user.Role,
            "district_id": user.DistrictID,
            "type": "refresh",
            "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
            "iat": now,
            "jti": str(uuid.uuid4()),
        }
        access_token = jwt.encode(access_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        db_session = Session(
            UserID=user.UserID,
            TokenHash=refresh_token[-64:],
            ExpiresAt=now + timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
        )
        self.session.add(db_session)
        await self.session.commit()
        return access_token, refresh_token
