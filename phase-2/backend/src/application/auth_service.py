from __future__ import annotations
import uuid
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt

from src.domain.models import User, Session
from src.domain.errors import AuthenticationError, NotFoundError, ConflictError, ValidationError
from src.persistence.interfaces import UserRepository, SessionRepository

logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        session_repo: SessionRepository,
        jwt_secret: str,
    ) -> None:
        self._user_repo = user_repo
        self._session_repo = session_repo
        self._jwt_secret = jwt_secret

    async def authenticate(self, email: str, password: str) -> tuple[str, str, User]:
        user = await self._user_repo.get_by_email(email.lower().strip())
        if user is None:
            raise AuthenticationError("Invalid email or password")

        if not user.is_active:
            raise AuthenticationError("Account is deactivated")

        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise AuthenticationError("Invalid email or password")

        access_token, refresh_token, _ = await self._issue_tokens(user)
        return access_token, refresh_token, user

    async def register(
        self,
        email: str,
        password: str,
        full_name: str,
        role: str = "officer",
        district_id: Optional[str] = None,
    ) -> User:
        if not email or not password:
            raise ValidationError("Email and password are required")

        existing = await self._user_repo.get_by_email(email.lower().strip())
        if existing is not None:
            raise ConflictError("A user with this email already exists")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            email=email.lower().strip(),
            password_hash=password_hash,
            full_name=full_name,
            role=role,
            district_id=district_id,
        )
        created = await self._user_repo.create(user)
        logger.info("User registered: id=%s email=%s role=%s", created.id, created.email, created.role)
        return created

    async def refresh_token(self, refresh_token: str) -> tuple[str, str, User]:
        try:
            payload = jwt.decode(refresh_token, self._jwt_secret, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            raise AuthenticationError("Invalid or expired refresh token")

        token_type = payload.get("type")
        user_id_str = payload.get("sub")
        if token_type != "refresh" or not user_id_str:
            raise AuthenticationError("Invalid token type")

        user_id = uuid.UUID(user_id_str)
        session_id = uuid.UUID(payload.get("sid", ""))
        token_hash = self._hash_token(refresh_token)

        session = await self._session_repo.find_by_hash(token_hash)
        if session is None or session.is_revoked:
            raise AuthenticationError("Session has been revoked")

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        await self._session_repo.revoke(session_id)
        access_token, new_refresh_token, _ = await self._issue_tokens(user)
        return access_token, new_refresh_token, user

    async def revoke_session(self, user_id: uuid.UUID) -> None:
        session = await self._session_repo.find_active_by_user_id(user_id)
        if session is not None:
            await self._session_repo.revoke(session.id)
            logger.info("Session revoked: user_id=%s session_id=%s", user_id, session.id)

    async def get_user_profile(self, user_id: uuid.UUID) -> User:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    async def validate_access_token(self, token: str) -> User:
        try:
            payload = jwt.decode(token, self._jwt_secret, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            raise AuthenticationError("Invalid or expired access token")

        token_type = payload.get("type")
        user_id_str = payload.get("sub")
        if token_type != "access" or not user_id_str:
            raise AuthenticationError("Invalid token type")

        session_id = payload.get("sid")
        token_hash = self._hash_token(token)

        session = await self._session_repo.find_by_hash(token_hash)
        if session is not None and session.is_revoked:
            raise AuthenticationError("Session has been revoked")

        user = await self._user_repo.get_by_id(uuid.UUID(user_id_str))
        if user is None:
            raise NotFoundError("User not found")

        return user

    async def _issue_tokens(self, user: User) -> tuple[str, str, Session]:
        now = datetime.utcnow()
        session_id = uuid.uuid4()

        access_expires = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "type": "access",
            "sid": str(session_id),
            "iat": now,
            "exp": access_expires,
        }
        access_token = jwt.encode(access_payload, self._jwt_secret, algorithm=ALGORITHM)

        refresh_expires = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_payload = {
            "sub": str(user.id),
            "type": "refresh",
            "sid": str(session_id),
            "iat": now,
            "exp": refresh_expires,
        }
        refresh_token = jwt.encode(refresh_payload, self._jwt_secret, algorithm=ALGORITHM)

        session = Session(
            id=session_id,
            user_id=user.id,
            token_hash=self._hash_token(access_token),
            refresh_token_hash=self._hash_token(refresh_token),
            expires_at=access_expires,
        )
        await self._session_repo.create(session)
        return access_token, refresh_token, session

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
