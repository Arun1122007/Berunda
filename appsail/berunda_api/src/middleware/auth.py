"""JWT authentication and RBAC middleware."""

from __future__ import annotations

import warnings

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config import settings

security = HTTPBearer(auto_error=False)

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = "HS256"

_WEAK_JWT = frozenset(
    {
        "dev-secret-change-in-production",
        "replace-with-a-random-64-hex-char-string",
        "replace_this_with_a_secure_random_string_in_production",
        "test-secret-for-testing-only",
    }
)
if JWT_SECRET in _WEAK_JWT:
    warnings.warn(
        "JWT_SECRET is set to a known weak/placeholder value. "
        'Generate a strong secret with: python -c "import secrets; print(secrets.token_hex(32))"',
        stacklevel=2,
    )


class AuthDependency:
    def __init__(self, required_roles: list[str] | None = None):
        self.required_roles = required_roles

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials | None = Depends(security)
    ) -> dict:
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        try:
            import jwt

            payload = jwt.decode(
                credentials.credentials,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        if self.required_roles:
            user_role = payload.get("role", "")
            if user_role not in self.required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )
        return payload


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    if credentials is None:
        return {"user_id": None, "role": "anonymous"}
    try:
        import jwt

        return jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return {"user_id": None, "role": "anonymous"}


def require_role(roles: list[str]):
    return AuthDependency(required_roles=roles)
