from __future__ import annotations

from fastapi import APIRouter, Depends

from src.middleware.auth import require_role

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/users")
async def list_users(
    user: dict = Depends(require_role(["admin"])),
):
    return {"users": []}


@router.post("/users")
async def create_user(
    user: dict = Depends(require_role(["admin"])),
):
    return {"message": "User creation not yet implemented"}


@router.patch("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    user: dict = Depends(require_role(["admin"])),
):
    return {"message": "Role update not yet implemented"}


@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    user: dict = Depends(require_role(["admin"])),
):
    return {"message": "Deactivation not yet implemented"}
