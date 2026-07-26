"""Authorization policies — resource ownership, role scoping, permission checks.

Layering: transport (called by route handlers) → application (policy evaluation)
"""

from __future__ import annotations

from typing import Any

from src.exceptions import AuthorizationError


def require_active_user(user: dict) -> dict:
    """Ensure the caller has an authenticated session."""
    uid = user.get("user_id")
    if uid is None:
        raise AuthorizationError("Authentication required")
    return user


def require_role(roles: list[str], user: dict) -> dict:
    """Ensure the caller has one of the required roles."""
    user_role = user.get("role", "anonymous")
    if user_role not in roles:
        raise AuthorizationError(f"Requires one of {roles}, got '{user_role}'")
    return user


def require_district_access(
    resource_district_id: int | None,
    user: dict,
) -> None:
    """Ensure officer-level users can only access their own district's data."""
    if user.get("role") == "admin":
        return
    user_district = user.get("district_id")
    if user_district is not None and resource_district_id != user_district:
        raise AuthorizationError("Access restricted to assigned district")


def require_resource_ownership(
    resource_owner_id: int | None,
    user: dict,
) -> None:
    """Ensure the caller owns the resource or is admin."""
    if user.get("role") == "admin":
        return
    uid = user.get("user_id")
    if resource_owner_id is not None and resource_owner_id != uid:
        raise AuthorizationError("Resource access restricted to owner")


def filter_district_scoped(
    user: dict,
    district_id_field: str = "DistrictID",
) -> dict[str, Any]:
    """Return a filter dict that scopes queries by district for officer role."""
    if user.get("role") == "admin":
        return {}
    user_district = user.get("district_id")
    if user_district is not None:
        return {district_id_field: user_district}
    return {}


class AuthContext:
    """Container for authenticated user context — passed through service layer."""

    def __init__(self, user: dict) -> None:
        self.user_id: int | None = user.get("user_id")
        self.role: str = user.get("role", "anonymous")
        self.district_id: int | None = user.get("district_id")
        self.email: str = user.get("email", "")

    @property
    def is_authenticated(self) -> bool:
        return self.user_id is not None

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def is_analyst(self) -> bool:
        return self.role == "analyst"

    @property
    def is_officer(self) -> bool:
        return self.role == "officer"

    def can_access_district(self, target_district_id: int | None) -> bool:
        if self.is_admin or self.is_analyst:
            return True
        if self.district_id is None:
            return False
        return self.district_id == target_district_id

    def can_edit_fir(self, fir_district_id: int | None) -> bool:
        if self.is_admin:
            return True
        if self.is_analyst:
            return True
        return self.can_access_district(fir_district_id)

    def can_delete_fir(self) -> bool:
        return self.is_admin
