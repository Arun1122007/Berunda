from __future__ import annotations
from typing import Callable, Awaitable

from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain.errors import AuthenticationError, AuthorizationError
from src.domain.models import User
from src.domain.rules import RoleHierarchyRule
from src.application.auth_service import AuthService

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    auth_service: AuthService = Depends(),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error_code": "AUTHENTICATION_FAILED", "message": "Missing authentication token"},
        )
    try:
        user = await auth_service.validate_access_token(credentials.credentials)
        request.state.current_user = user
        return user
    except (AuthenticationError, AuthorizationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error_code": e.error_code, "message": e.message},
        ) from e


def require_role(minimum_role: str) -> Callable[[User], User]:
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not RoleHierarchyRule.has_role(current_user.role, minimum_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error_code": "FORBIDDEN", "message": f"Requires role: {minimum_role} or higher"},
            )
        return current_user
    return role_checker


class AuthDependency:
    def __init__(self, minimum_role: str | None = None) -> None:
        self._minimum_role = minimum_role

    async def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if self._minimum_role is not None:
            if not RoleHierarchyRule.has_role(current_user.role, self._minimum_role):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={"error_code": "FORBIDDEN", "message": f"Requires role: {self._minimum_role} or higher"},
                )
        return current_user
