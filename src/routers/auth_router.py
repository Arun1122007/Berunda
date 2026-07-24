from __future__ import annotations

import jwt as pyjwt
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import JWT_ALGORITHM, JWT_SECRET, get_current_user
from src.schemas.auth import (
    LoginRequest,
    LogoutResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    try:
        user, access_token, refresh_token = await service.authenticate(data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return TokenResponse(
        token=access_token,
        refreshToken=refresh_token,
        expiresIn=3600,
        user=UserResponse(
            userId=user.UserID,
            email=user.Email,
            name=user.Email.split("@")[0],
            role=user.Role,
            permissions=[],
        ),
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    try:
        user = await service.register(data.email, data.password, data.role, data.district_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return UserResponse(
        userId=user.UserID,
        email=user.Email,
        name=user.Email.split("@")[0],
        role=user.Role,
        permissions=[],
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    try:
        access_token, refresh_token = await service.refresh_token(data.refreshToken)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    decoded = pyjwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return TokenResponse(
        token=access_token,
        refreshToken=refresh_token,
        expiresIn=3600,
        user=UserResponse(
            userId=decoded["user_id"],
            email="",
            name="User",
            role=decoded["role"],
            permissions=[],
        ),
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    authorization: str = Header(default=""),
    db: AsyncSession = Depends(get_session),
):
    token_str = authorization.replace("Bearer ", "") if authorization else ""
    if token_str:
        service = AuthService(db)
        await service.revoke_session(token_str)
    return LogoutResponse()


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    uid = current_user.get("user_id")
    if uid:
        service = AuthService(db)
        profile = await service.get_user_profile(uid)
        if profile:
            return UserResponse(**profile)

    return UserResponse(
        userId=uid or 0,
        email=current_user.get("email", ""),
        name="Current User",
        role=current_user.get("role", "anonymous"),
        permissions=[],
    )
