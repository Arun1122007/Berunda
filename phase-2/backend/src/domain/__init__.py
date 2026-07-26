from src.domain.errors import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    DomainError,
    NotFoundError,
    ValidationError,
)
from src.domain.models import FIR, ActSection, Person, Session, User
from src.domain.rules import CrimeNumberRule, DistrictScopeRule, GravityOffenceRule, RoleHierarchyRule

ErrorCode = str

__all__ = [
    "FIR",
    "User",
    "Session",
    "Person",
    "ActSection",
    "ErrorCode",
    "DomainError",
    "NotFoundError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "ConflictError",
    "CrimeNumberRule",
    "DistrictScopeRule",
    "RoleHierarchyRule",
    "GravityOffenceRule",
]
