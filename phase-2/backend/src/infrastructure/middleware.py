from __future__ import annotations
import uuid
import logging
from typing import Callable, Awaitable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.types import ASGIApp

from src.domain.errors import DomainError

logger = logging.getLogger(__name__)


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        correlation_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = correlation_id
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Cache-Control"] = "no-store"
        return response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    ERROR_MAP: dict[str, int] = {
        "NOT_FOUND": 404,
        "AUTHENTICATION_FAILED": 401,
        "FORBIDDEN": 403,
        "VALIDATION_ERROR": 422,
        "CONFLICT": 409,
    }

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        try:
            return await call_next(request)
        except DomainError as e:
            status = self.ERROR_MAP.get(e.error_code, 500)
            cid = getattr(request.state, "correlation_id", str(uuid.uuid4()))
            logger.warning("Domain error: code=%s message=%s path=%s", e.error_code, e.message, request.url.path)
            return JSONResponse(
                status_code=status,
                content={
                    "error": {
                        "code": e.error_code,
                        "message": e.message,
                        "detail": {},
                        "requestId": cid,
                    }
                },
            )
        except Exception as e:
            cid = getattr(request.state, "correlation_id", str(uuid.uuid4()))
            logger.exception("Unhandled error: %s path=%s", str(e), request.url.path)
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": "An unexpected error occurred",
                        "detail": {},
                        "requestId": cid,
                    }
                },
            )
