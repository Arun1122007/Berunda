from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.config import settings
from src.exceptions import AuthenticationError, ConflictError
from src.middleware.auth import JWT_ALGORITHM, JWT_SECRET
from src.repositories.core import AuthRepository
from src.services.base import BaseService

ACCESS_TOKEN_EXPIRY_MINUTES = settings.ACCESS_TOKEN_EXPIRY_MINUTES
REFRESH_TOKEN_EXPIRY_DAYS = settings.REFRESH_TOKEN_EXPIRY_DAYS


class AuthService(BaseService):
    def __init__(self, repo: AuthRepository):
        super().__init__()
        self.repo = repo

    async def authenticate(self, email: str, password: str):
        user = await self.repo.get_user_by_email(email)
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.HashedPassword.encode("utf-8")
        ):
            raise AuthenticationError("Invalid credentials")
        if not user.IsActive:
            raise AuthenticationError("Account is disabled")
        access_token, refresh_token = await self._issue_tokens(user)
        return user, access_token, refresh_token

    async def register(
        self, email: str, password: str, role: str = "officer", district_id: int | None = None
    ):
        existing = await self.repo.get_user_by_email(email)
        if existing:
            raise ConflictError("Email already registered")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = await self.repo.create_user(
            {"Email": email, "HashedPassword": hashed, "Role": role, "DistrictID": district_id}
        )
        await self.repo.commit()
        return user

    async def refresh_token(self, token_str: str):
        try:
            payload = jwt.decode(token_str, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Refresh token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise AuthenticationError("Not a refresh token")

        token_suffix = token_str[-64:]
        session_record = await self.repo.get_session_by_token(token_suffix)
        if not session_record or (
            hasattr(session_record, "RevokedAt") and session_record.RevokedAt
        ):
            raise AuthenticationError("Session revoked or not found")

        user = await self.repo.get_user_by_id(
            session_record.UserID
            if hasattr(session_record, "UserID")
            else session_record.get("UserID")
        )
        if not user or (hasattr(user, "IsActive") and not user.IsActive):
            raise AuthenticationError("User not found or disabled")

        if hasattr(session_record, "SessionID"):
            await self.repo.revoke_session(session_record.SessionID)
        access_token, refresh_token = await self._issue_tokens(user)
        return access_token, refresh_token

    async def revoke_session(self, token_str: str) -> None:
        token_suffix = token_str[-64:]
        session_record = await self.repo.get_session_by_token(token_suffix)
        if session_record and hasattr(session_record, "SessionID"):
            await self.repo.revoke_session(session_record.SessionID)
            await self.repo.commit()

    async def get_user_profile(self, user_id: int) -> dict | None:
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            return None
        district_name = None
        if hasattr(user, "DistrictID") and user.DistrictID and hasattr(self.repo, "get_district"):
            district = await self.repo.get_district(user.DistrictID)
            district_name = district.DistrictName if district else None
        return {
            "userId": user.UserID,
            "email": user.Email,
            "name": user.Email.split("@")[0],
            "role": user.Role,
            "district": district_name,
            "permissions": [],
        }

    async def _issue_tokens(self, user):
        now = datetime.now(timezone.utc)
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

        await self.repo.save_session(
            {
                "UserID": user.UserID,
                "TokenHash": refresh_token[-64:],
                "ExpiresAt": now + timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
            }
        )
        await self.repo.commit()
        return access_token, refresh_token
