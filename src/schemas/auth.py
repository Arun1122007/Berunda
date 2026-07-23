from __future__ import annotations

from pydantic import Field

from src.schemas.base import APIBase


class LoginRequest(APIBase):
    email: str
    password: str


class RegisterRequest(APIBase):
    email: str
    password: str
    name: str = ""
    role: str = "officer"
    district_id: int | None = None


class RefreshRequest(APIBase):
    refreshToken: str = Field(alias="refreshToken")  # noqa: N815


class TokenResponse(APIBase):
    token: str
    refreshToken: str  # noqa: N815
    expiresIn: int  # noqa: N815
    user: UserResponse


class LogoutResponse(APIBase):
    message: str = "Logged out successfully"


class UserResponse(APIBase):
    userId: int  # noqa: N815
    email: str = ""
    name: str
    role: str
    district: str | None = None
    policeStation: str | None = None  # noqa: N815
    permissions: list[str] = []
