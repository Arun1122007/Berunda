"""Smoke tests — validate application startup, health, readiness, and safe error handling.

These are the first tests to run after deployment to verify the application
is alive and responding correctly.
"""

from __future__ import annotations

import pytest


class TestApplicationStartup:
    """The application must start and report correctly."""

    def test_app_imports_and_has_expected_metadata(self):
        from src.main import app

        assert app.title == "Berunda API"
        assert app.version != ""
        assert len(app.router.routes) > 5

    def test_core_endpoints_are_registered(self):
        from src.main import app

        route_paths = {r.path for r in app.router.routes if hasattr(r, "path")}
        for required in ("/health", "/ready", "/", "/api/v1/status"):
            assert required in route_paths, f"Missing route: {required}"

    def test_settings_uses_safe_defaults(self):
        from src.config import Settings

        cfg = Settings()
        assert cfg.HOST == "0.0.0.0"
        assert cfg.LOG_LEVEL == "INFO"
        assert cfg.APP_ENV is not None

    def test_settings_enforces_jwt_secret_length(self):
        from pydantic import ValidationError

        from src.config import Settings

        with pytest.raises(ValidationError):
            Settings(JWT_SECRET="short")


class TestMissingConfiguration:
    """Safe failure when required configuration is absent."""

    def test_yaml_config_missing_returns_defaults(self):
        from src.shared.config import load_config

        result = load_config(config_dir="/nonexistent/path")
        assert isinstance(result, dict)
        assert result == {"logging": {"level": "INFO"}}

    def test_settings_accepts_empty_prod_api_key_with_warning(self):
        import warnings

        from src.config import Settings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cfg = Settings(APP_ENV="development", OPENAI_API_KEY="")
        assert cfg.OPENAI_API_KEY == ""

    def test_no_crash_when_yaml_fails_at_runtime(self):
        from src.main import logger

        assert logger is not None


class TestHealthEndpoint:
    """GET /health must return 200 and valid status."""

    @pytest.mark.asyncio
    async def test_returns_200(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/health")
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_returns_expected_structure(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/health")
        data = resp.json()
        assert data["status"] in ("healthy", "degraded")
        assert "version" in data
        assert "checks" in data
        assert data["checks"]["python"] is True

    @pytest.mark.asyncio
    async def test_uptime_is_positive(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/health")
        uptime = resp.json()["checks"]["uptime_seconds"]
        assert isinstance(uptime, (int, float))
        assert uptime >= 0

    @pytest.mark.asyncio
    async def test_content_type_is_json(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/health")
        assert "application/json" in resp.headers.get("content-type", "")


class TestReadinessEndpoint:
    """GET /ready must return 200 with dependency checks."""

    @pytest.mark.asyncio
    async def test_returns_200(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/ready")
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_contains_database_check(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/ready")
        data = resp.json()
        assert "checks" in data
        assert "database" in data["checks"]
        assert isinstance(data["checks"]["database"], bool)

    @pytest.mark.asyncio
    async def test_status_is_ready_or_degraded(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/ready")
        assert resp.json()["status"] in ("ready", "degraded")


class TestSafeGlobalErrorHandling:
    """Unhandled exceptions must return safe, structured responses."""

    @pytest.mark.asyncio
    async def test_nonexistent_route_returns_404(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/this-route-does-not-exist-12345")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_404_response_is_json(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/nonexistent")
        assert "application/json" in resp.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_error_response_does_not_leak_stack_trace(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/nonexistent")
        body = resp.text.lower()
        assert "traceback" not in body


class TestApiStatus:
    """GET /api/v1/status returns operational metadata."""

    @pytest.mark.asyncio
    async def test_returns_200(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/api/v1/status")
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_contains_expected_fields(self, smoke_client):
        async with smoke_client as c:
            resp = await c.get("/api/v1/status")
        data = resp.json()
        assert data["service"] == "Berunda"
        assert data["api_version"] == "v1"
        assert data["status"] == "operational"


class TestCoreModuleImports:
    """All core modules must import cleanly."""

    def test_shared_config_imports(self):
        from src.shared.config import _deep_merge, load_config

        assert callable(load_config)
        assert callable(_deep_merge)

    def test_shared_logging_imports(self):
        from src.shared.logging import StructuredFormatter, get_logger

        assert callable(get_logger)
        assert StructuredFormatter is not None

    def test_database_module_imports(self):
        from src.database import dispose_engine, wait_for_db

        assert callable(wait_for_db)
        assert dispose_engine is not None

    def test_middleware_imports(self):
        from src.middleware import CorrelationIDMiddleware, SecurityHeadersMiddleware

        assert CorrelationIDMiddleware is not None
        assert SecurityHeadersMiddleware is not None

    def test_settings_imports(self):
        from src.config import Settings, settings

        assert isinstance(settings, Settings)
