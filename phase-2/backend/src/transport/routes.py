from fastapi import APIRouter

from src.transport.handlers import (
    handle_list_firs,
    handle_get_fir,
    handle_create_fir,
    handle_update_fir,
    handle_delete_fir,
    handle_login,
    handle_register,
    handle_refresh,
    handle_logout,
    handle_me,
)
from src.transport.dto import (
    FIRListResponse,
    FIRDetailResponse,
    TokenResponse,
    UserResponse,
)

fir_router = APIRouter(prefix="/api/v1/fir", tags=["FIRs"])

fir_router.add_api_route(
    "", endpoint=handle_list_firs, methods=["GET"],
    response_model=FIRListResponse,
    summary="List FIRs with pagination and filters",
)
fir_router.add_api_route(
    "/{fir_id}", endpoint=handle_get_fir, methods=["GET"],
    response_model=FIRDetailResponse,
    summary="Get FIR by ID",
)
fir_router.add_api_route(
    "", endpoint=handle_create_fir, methods=["POST"],
    response_model=FIRDetailResponse, status_code=201,
    summary="Create a new FIR",
)
fir_router.add_api_route(
    "/{fir_id}", endpoint=handle_update_fir, methods=["PUT"],
    response_model=FIRDetailResponse,
    summary="Update an existing FIR",
)
fir_router.add_api_route(
    "/{fir_id}", endpoint=handle_delete_fir, methods=["DELETE"],
    response_model=None,
    summary="Delete an FIR",
)

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

auth_router.add_api_route(
    "/login", endpoint=handle_login, methods=["POST"],
    response_model=TokenResponse,
    summary="Authenticate user and return tokens",
)
auth_router.add_api_route(
    "/register", endpoint=handle_register, methods=["POST"],
    response_model=UserResponse, status_code=201,
    summary="Register a new user (admin only)",
)
auth_router.add_api_route(
    "/refresh", endpoint=handle_refresh, methods=["POST"],
    response_model=TokenResponse,
    summary="Refresh access token",
)
auth_router.add_api_route(
    "/logout", endpoint=handle_logout, methods=["POST"],
    response_model=None,
    summary="Revoke current session",
)
auth_router.add_api_route(
    "/me", endpoint=handle_me, methods=["GET"],
    response_model=UserResponse,
    summary="Get current user profile",
)
