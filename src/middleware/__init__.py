"""Middleware — auth, correlation, security headers, audit."""

from __future__ import annotations

import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.middleware.auth import AuthDependency, get_current_user, require_role
from src.shared.logging import get_correlation_filter


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Inject/generate X-Request-ID and propagate to structured logging."""

    async def dispatch(self, request: Request, call_next) -> Response:
        cid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.correlation_id = cid
        get_correlation_filter().set_correlation_id(cid)
        response = await call_next(request)
        response.headers["X-Request-ID"] = cid
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to every response."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "0"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


__all__ = [
    "AuthDependency",
    "CorrelationIDMiddleware",
    "SecurityHeadersMiddleware",
    "get_current_user",
    "require_role",
]
