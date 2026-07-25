"""Domain exception hierarchy — typed errors for every layer."""

from __future__ import annotations


class BerundaError(Exception):
    """Base exception for all Berunda domain errors."""

    status_code: int = 500
    code: str = "INTERNAL_ERROR"

    def __init__(self, message: str = "An unexpected error occurred.", detail: dict | None = None):
        self.message = message
        self.detail = detail or {}
        super().__init__(self.message)


class NotFoundError(BerundaError):
    status_code = 404
    code = "NOT_FOUND"


class AuthenticationError(BerundaError):
    status_code = 401
    code = "AUTHENTICATION_ERROR"


class AuthorizationError(BerundaError):
    status_code = 403
    code = "FORBIDDEN"


class ValidationError(BerundaError):
    status_code = 422
    code = "VALIDATION_ERROR"


class ConflictError(BerundaError):
    status_code = 409
    code = "CONFLICT"


class DatabaseError(BerundaError):
    status_code = 500
    code = "DATABASE_ERROR"


class AIServiceError(BerundaError):
    status_code = 503
    code = "AI_SERVICE_UNAVAILABLE"


class ExternalServiceError(BerundaError):
    status_code = 502
    code = "EXTERNAL_SERVICE_ERROR"
