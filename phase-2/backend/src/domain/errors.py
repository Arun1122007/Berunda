from __future__ import annotations

from typing import Optional


class DomainError(Exception):
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    message: str = "An internal error occurred"

    def __init__(self, message: Optional[str] = None, status_code: Optional[int] = None, error_code: Optional[str] = None) -> None:
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        super().__init__(self.message)


class NotFoundError(DomainError):
    status_code: int = 404
    error_code: str = "NOT_FOUND"
    message: str = "The requested resource was not found"


class AuthenticationError(DomainError):
    status_code: int = 401
    error_code: str = "AUTHENTICATION_FAILED"
    message: str = "Authentication failed"


class AuthorizationError(DomainError):
    status_code: int = 403
    error_code: str = "FORBIDDEN"
    message: str = "You do not have permission to perform this action"


class ValidationError(DomainError):
    status_code: int = 422
    error_code: str = "VALIDATION_ERROR"
    message: str = "Validation failed"


class ConflictError(DomainError):
    status_code: int = 409
    error_code: str = "CONFLICT"
    message: str = "Resource already exists"
