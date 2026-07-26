from src.domain.models import FIR, Person, ActSection, User, Session
from src.domain.errors import DomainError, NotFoundError, AuthenticationError, AuthorizationError, ValidationError, ConflictError
from src.domain.rules import CrimeNumberRule, DistrictScopeRule, RoleHierarchyRule, GravityOffenceRule

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
