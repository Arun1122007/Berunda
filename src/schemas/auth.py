from pydantic import Field

from src.schemas.base import APIBase


class LoginRequest(APIBase):
    email: str = Field(examples=["admin@berunda.gov", "officer@ksp.karnataka.gov.in"])
    password: str = Field(examples=["your-secure-password"])


class RegisterRequest(APIBase):
    email: str = Field(examples=["new-officer@ksp.karnataka.gov.in"])
    password: str = Field(min_length=8, examples=["secure-p@ss-2026"])
    role: str = Field(default="officer", examples=["officer", "analyst"])
    district_id: int | None = Field(None, examples=[1, 5])


class RefreshRequest(APIBase):
    refreshToken: str = Field(alias="refreshToken", examples=["eyJhbGciOiJIUzI1NiIs..."])  # noqa: N815


class UserResponse(APIBase):
    userId: int  # noqa: N815
    email: str
    name: str
    role: str
    district: str | None = None
    permissions: list[str] = Field(default_factory=list)


class TokenResponse(APIBase):
    token: str
    refreshToken: str  # noqa: N815
    expiresIn: int = Field(alias="expiresIn")  # noqa: N815
    user: UserResponse


class LogoutResponse(APIBase):
    message: str = "Logged out successfully"
