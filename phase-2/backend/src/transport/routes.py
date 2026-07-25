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

fir_router = APIRouter(prefix="/api/v1/firs", tags=["FIRs"])

fir_router.add_api_route("", endpoint=handle_list_firs, methods=["GET"], summary="List FIRs with pagination and filters")
fir_router.add_api_route("/{fir_id}", endpoint=handle_get_fir, methods=["GET"], summary="Get FIR by ID")
fir_router.add_api_route("", endpoint=handle_create_fir, methods=["POST"], summary="Create a new FIR", status_code=201)
fir_router.add_api_route("/{fir_id}", endpoint=handle_update_fir, methods=["PUT"], summary="Update an existing FIR")
fir_router.add_api_route("/{fir_id}", endpoint=handle_delete_fir, methods=["DELETE"], summary="Delete an FIR")

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

auth_router.add_api_route("/login", endpoint=handle_login, methods=["POST"], summary="Authenticate user and return tokens")
auth_router.add_api_route("/register", endpoint=handle_register, methods=["POST"], summary="Register a new user (admin only)")
auth_router.add_api_route("/refresh", endpoint=handle_refresh, methods=["POST"], summary="Refresh access token")
auth_router.add_api_route("/logout", endpoint=handle_logout, methods=["POST"], summary="Revoke current session")
auth_router.add_api_route("/me", endpoint=handle_me, methods=["GET"], summary="Get current user profile")
