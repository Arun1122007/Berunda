"""Request handlers for the Phase 2 backend.

Handlers delegate to application services. They must NOT contain business logic.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, Query, Request, status

from src.application.auth_service import AuthService
from src.application.fir_service import FIRService
from src.domain.errors import DomainError
from src.domain.models import FIR
from src.infrastructure.auth import get_current_user, require_role
from src.transport.dto import (
    FIRCreateRequest,
    FIRDetailResponse,
    FIRListResponse,
    FIRUpdateRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

logger = logging.getLogger(__name__)

ERROR_MAP: dict[str, int] = {
    "NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "AUTHENTICATION_FAILED": status.HTTP_401_UNAUTHORIZED,
    "FORBIDDEN": status.HTTP_403_FORBIDDEN,
    "VALIDATION_ERROR": status.HTTP_422_UNPROCESSABLE_ENTITY,
    "CONFLICT": status.HTTP_409_CONFLICT,
}


def _error_to_http(exc: DomainError) -> HTTPException:
    http_status = ERROR_MAP.get(exc.error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    return HTTPException(
        status_code=http_status,
        detail={"error_code": exc.error_code, "message": exc.message},
    )


async def handle_list_firs(
    request: Request,
    current_user=Depends(get_current_user),
    district_id: Optional[str] = None,
    police_station_id: Optional[str] = None,
    case_status_id: Optional[str] = None,
    crime_major_head_id: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    fir_service: FIRService = request.app.state.fir_service
    try:
        offset = (page - 1) * page_size
        items, total = await fir_service.list_firs(
            user_id=current_user.id,
            district_id=district_id,
            police_station_id=police_station_id,
            case_status_id=case_status_id,
            crime_major_head_id=crime_major_head_id,
            from_date=from_date,
            to_date=to_date,
            offset=offset,
            limit=page_size,
        )
        return FIRListResponse(
            items=[FIRDetailResponse.model_validate(f) for f in items],
            total=total,
            page=page,
            page_size=page_size,
        )
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_get_fir(
    request: Request,
    fir_id: uuid.UUID,
    current_user=Depends(get_current_user),
):
    fir_service: FIRService = request.app.state.fir_service
    try:
        fir = await fir_service.get_fir(fir_id=fir_id, user_id=current_user.id)
        return FIRDetailResponse.model_validate(fir)
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_create_fir(
    request: Request,
    body: FIRCreateRequest,
    current_user=Depends(get_current_user),
):
    fir_service: FIRService = request.app.state.fir_service
    try:
        fir_data = FIR(
            crime_no=body.crime_no,
            police_station_id=body.police_station_id,
            case_category_id=body.case_category_id,
            gravity_offence_id=body.gravity_offence_id,
            crime_major_head_id=body.crime_major_head_id,
            crime_minor_head_id=body.crime_minor_head_id,
            case_status_id=body.case_status_id,
            district_id=body.district_id,
            case_no=body.case_no,
            incident_from_date=body.incident_from_date,
            incident_to_date=body.incident_to_date,
            brief_facts=body.brief_facts,
            latitude=body.latitude,
            longitude=body.longitude,
            registered_date=datetime.utcnow(),
        )
        created = await fir_service.create_fir(fir_data=fir_data, user_id=current_user.id)
        return FIRDetailResponse.model_validate(created)
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_update_fir(
    request: Request,
    fir_id: uuid.UUID,
    body: FIRUpdateRequest,
    current_user=Depends(get_current_user),
):
    fir_service: FIRService = request.app.state.fir_service
    try:
        existing = await fir_service.get_fir(fir_id=fir_id, user_id=current_user.id)
        update_data = body.model_dump(exclude_unset=True)
        merged = existing.model_copy(update=update_data)
        updated = await fir_service.update_fir(fir_id=fir_id, fir_data=merged, user_id=current_user.id)
        return FIRDetailResponse.model_validate(updated)
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_delete_fir(
    request: Request,
    fir_id: uuid.UUID,
    current_user=Depends(get_current_user),
):
    fir_service: FIRService = request.app.state.fir_service
    try:
        await fir_service.delete_fir(fir_id=fir_id, user_id=current_user.id)
        return {"message": "FIR deleted successfully"}
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_login(
    request: Request,
    body: LoginRequest,
):
    auth_service: AuthService = request.app.state.auth_service
    try:
        access_token, refresh_token, user = await auth_service.authenticate(
            email=body.email,
            password=body.password,
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user),
        )
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_register(
    request: Request,
    body: RegisterRequest,
    current_user=Depends(require_role("admin")),
):
    auth_service: AuthService = request.app.state.auth_service
    try:
        user = await auth_service.register(
            email=body.email,
            password=body.password,
            full_name=body.full_name,
            role=body.role,
            district_id=body.district_id,
        )
        return UserResponse.model_validate(user)
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_refresh(
    request: Request,
    body: RefreshRequest,
):
    auth_service: AuthService = request.app.state.auth_service
    try:
        access_token, refresh_token, user = await auth_service.refresh_token(
            refresh_token=body.refresh_token,
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user),
        )
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_logout(
    request: Request,
    current_user=Depends(get_current_user),
):
    auth_service: AuthService = request.app.state.auth_service
    try:
        await auth_service.revoke_session(user_id=current_user.id)
        return {"message": "Logged out successfully"}
    except DomainError as e:
        raise _error_to_http(e) from e


async def handle_me(
    request: Request,
    current_user=Depends(get_current_user),
):
    auth_service: AuthService = request.app.state.auth_service
    try:
        user = await auth_service.get_user_profile(user_id=current_user.id)
        return UserResponse.model_validate(user)
    except DomainError as e:
        raise _error_to_http(e) from e
