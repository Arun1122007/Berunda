import pytest
from fastapi import HTTPException

import sys
from pathlib import Path
_root = str(Path(__file__).parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

from src.domain.errors import (
    DomainError,
    NotFoundError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    ConflictError,
)
from src.transport.handlers import _error_to_http
from src.infrastructure.middleware import ErrorHandlerMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class TestErrorMappingUtility:
    def test_not_found_returns_404(self):
        exc = NotFoundError("FIR not found")
        http = _error_to_http(exc)
        assert http.status_code == 404
        assert http.detail["error_code"] == "NOT_FOUND"
        assert http.detail["message"] == "FIR not found"

    def test_authentication_returns_401(self):
        exc = AuthenticationError("Invalid credentials")
        http = _error_to_http(exc)
        assert http.status_code == 401
        assert http.detail["error_code"] == "AUTHENTICATION_FAILED"

    def test_authorization_returns_403(self):
        exc = AuthorizationError("Not allowed")
        http = _error_to_http(exc)
        assert http.status_code == 403
        assert http.detail["error_code"] == "FORBIDDEN"

    def test_validation_returns_422(self):
        exc = ValidationError("Invalid input")
        http = _error_to_http(exc)
        assert http.status_code == 422
        assert http.detail["error_code"] == "VALIDATION_ERROR"

    def test_conflict_returns_409(self):
        exc = ConflictError("Already exists")
        http = _error_to_http(exc)
        assert http.status_code == 409
        assert http.detail["error_code"] == "CONFLICT"

    def test_generic_domain_error_returns_500(self):
        exc = DomainError("Unexpected error")
        http = _error_to_http(exc)
        assert http.status_code == 500
        assert http.detail["error_code"] == "INTERNAL_ERROR"

    def test_custom_error_code_respected(self):
        exc = DomainError("Custom", status_code=400, error_code="BAD_REQUEST")
        http = _error_to_http(exc)
        assert http.status_code == 500

    def test_detail_includes_both_fields(self):
        exc = NotFoundError("Missing")
        http = _error_to_http(exc)
        detail = http.detail
        assert "error_code" in detail
        assert "message" in detail


class FakeApp:
    def __init__(self, handler):
        self._handler = handler

    async def __call__(self, scope, receive, send):
        raise NotImplementedError


class TestErrorHandlerMiddleware:
    @pytest.mark.asyncio
    async def test_domain_error_caught(self):
        middleware = ErrorHandlerMiddleware(app=None)

        async def call_next(request):
            raise NotFoundError("Resource not found")

        request = Request(scope={"type": "http", "method": "GET", "path": "/test", "headers": []})
        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 404
        body = response.body.decode()
        assert "NOT_FOUND" in body
        assert "Resource not found" in body

    @pytest.mark.asyncio
    async def test_authentication_error_caught(self):
        middleware = ErrorHandlerMiddleware(app=None)

        async def call_next(request):
            raise AuthenticationError("Bad token")

        request = Request(scope={"type": "http", "method": "GET", "path": "/test", "headers": []})
        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_authorization_error_caught(self):
        middleware = ErrorHandlerMiddleware(app=None)

        async def call_next(request):
            raise AuthorizationError("Forbidden")

        request = Request(scope={"type": "http", "method": "GET", "path": "/test", "headers": []})
        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_validation_error_caught(self):
        middleware = ErrorHandlerMiddleware(app=None)

        async def call_next(request):
            raise ValidationError("Bad input")

        request = Request(scope={"type": "http", "method": "GET", "path": "/test", "headers": []})
        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_conflict_error_caught(self):
        middleware = ErrorHandlerMiddleware(app=None)

        async def call_next(request):
            raise ConflictError("Duplicate")

        request = Request(scope={"type": "http", "method": "GET", "path": "/test", "headers": []})
        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_unhandled_exception_returns_500(self):
        middleware = ErrorHandlerMiddleware(app=None)

        async def call_next(request):
            raise RuntimeError("Something broke")

        request = Request(scope={"type": "http", "method": "GET", "path": "/test", "headers": []})
        response = await middleware.dispatch(request, call_next)

        assert response.status_code == 500
        body = response.body.decode()
        assert "INTERNAL_ERROR" in body
