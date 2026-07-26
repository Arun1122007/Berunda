"""Berunda FastAPI application — AI-Native Crime Intelligence Platform."""

from __future__ import annotations

import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import sqlalchemy as sa
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.config import settings
from src.database import dispose_engine, get_engine, wait_for_db
from src.middleware import CorrelationIDMiddleware, SecurityHeadersMiddleware
from src.exceptions import (
    BerundaError, NotFoundError, AuthenticationError, AuthorizationError,
    ValidationError, ConflictError, DatabaseError, AIServiceError,
)
from src.routers import (
    admin_router,
    ai_intelligence_router,
    analytics_router,
    anomaly_router,
    audit_router,
    auth_router,
    dashboard_router,
    entity_router,
    fairness_router,
    fir_router,
    geospatial_router,
    graph_router,
    hotspot_router,
    investigation_router,
    notification_router,
    persons_router,
    police_stations_router,
    rag_router,
    related_cases_router,
    report_router,
    risk_router,
    search_router,
    webhook_router,
)
from src.routers.rag_router import limiter
from src.shared.config import load_config
from src.shared.logging import get_logger

try:
    import prometheus_client
except ImportError:
    prometheus_client = None  # type: ignore[assignment]

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logger = get_logger(__name__)
_start_time = time.time()

tags_metadata = [
    {
        "name": "FIR",
        "description": "First Information Report CRUD — the core case record. Supports list, get, create, update, delete with district-scoped access for non-admin users.",
    },
    {
        "name": "Entity",
        "description": "Person entity resolution — list, search, merge duplicate identities across cases.",
    },
    {
        "name": "Graph",
        "description": "Entity relationship graph — traverse person-to-person connections with configurable depth and confidence thresholds.",
    },
    {
        "name": "Hotspot",
        "description": "Crime hotspot analysis — spatial clustering for geographic pattern detection.",
    },
    {
        "name": "Anomaly",
        "description": "Anomaly detection — identify unusual case patterns for investigation leads.",
    },
    {
        "name": "Risk",
        "description": "Risk scoring — compute recidivism, recency, and severity scores for persons of interest.",
    },
    {
        "name": "RAG",
        "description": "Retrieval-Augmented Generation — semantic search over FIR corpus with LLM-powered answers. Rate-limited to 5 req/min.",
    },
    {
        "name": "Fairness",
        "description": "Fairness audit — bias detection across demographic dimensions in case outcomes.",
    },
    {
        "name": "Audit",
        "description": "Audit log — immutable trail of data access and modifications for compliance.",
    },
    {
        "name": "Auth",
        "description": "Authentication & authorization — JWT login, registration, token refresh, logout, and role-based access control (admin/officer/analyst).",
    },
    {
        "name": "Investigation",
        "description": "Investigation workflow — notes, assignments, status transitions, supervisor reviews, and case timeline.",
    },
    {
        "name": "Dashboard",
        "description": "Role-specific operational dashboards — officer metrics and supervisor overview.",
    },
    {
        "name": "Search",
        "description": "FIR search — structured filters and semantic search with authorization filtering.",
    },
    {
        "name": "Related Cases",
        "description": "Related-case detection — candidate suggestion generation, human review, and relationship management.",
    },
    {
        "name": "Reports",
        "description": "Protected report generation — request, generate, and download authorized reports.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup", {"version": "0.4.0"})

    app.state.neo4j_service = None
    app.state.notification_service = None
    app.state.start_time = _start_time

    db_ok = await wait_for_db(retries=5, delay=2.0)
    app.state.db_connected = db_ok

    last_db_check = _start_time
    app.state.last_db_check = last_db_check

    if db_ok:
        from src.services.event_bus_service import get_event_bus
        from src.services.notification_service import NotificationService
        from src.services.webhook_service import get_webhook_service

        app.state.notification_service = NotificationService()
        app.state.webhook_service = get_webhook_service()

        event_bus = get_event_bus()
        event_bus.connect_notification_service(app.state.notification_service)
        event_bus.connect_webhook_service(app.state.webhook_service)
        logger.info("Notification service and Catalyst webhook service initialized and connected to EventBus")

    if settings.NEO4J_URI and settings.NEO4J_PASSWORD:
        from src.services.neo4j_service import Neo4jService

        neo = Neo4jService.get_instance()
        neo_ok = await neo.connect()
        app.state.neo4j_service = neo if neo_ok else None
        logger.info("Neo4j %s", "connected" if neo_ok else "unavailable")

    if prometheus_client is not None:
        try:
            pool = get_engine().pool
            DB_CONNECTIONS.set(pool.size() + pool.overflow())
        except Exception as exc:
            logger.warning("Failed to set DB_CONNECTIONS gauge", exc_info=exc)

    app.state.metrics_enabled = prometheus_client is not None
    app.state.active_session_count = 0

    yield

    logger.info("Application shutdown — cleaning up resources")
    if prometheus_client is not None:
        try:
            ACTIVE_SESSIONS.set(0)
            DB_CONNECTIONS.set(0)
        except Exception as exc:
            logger.warning("Failed to reset Prometheus gauges during shutdown", exc_info=exc)
    await dispose_engine()
    if app.state.neo4j_service:
        try:
            from src.services.neo4j_service import Neo4jService

            await Neo4jService.get_instance().close()
        except Exception as exc:
            logger.warning("Neo4j close error", exc_info=exc)


app = FastAPI(
    title="Berunda API",
    version="0.4.0",
    description="AI-Native Crime Intelligence Platform — real-time FIR management, entity resolution, risk scoring, anomaly detection, hotspot analysis, and RAG-powered case search.",
    lifespan=lifespan,
    contact={
        "name": "Berunda Team",
        "url": "https://github.com/Arun1122007/Berunda",
        "email": "team@berunda.gov.in",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
    servers=[
        {"url": "http://localhost:9000", "description": "Local development"},
        {"url": "https://api.berunda.example.com", "description": "Production"},
    ],
)

app.state.db_connected = False
app.state.neo4j_service = None
app.state.notification_service = None
app.state.start_time = 0.0


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version="3.1.0",
        description=app.description,
        routes=app.routes,
        tags=tags_metadata,
        contact=app.contact,
        license_info=app.license_info,
        servers=app.servers,
    )
    schema["info"]["x-logo"] = {"url": "https://berunda.example.com/logo.png"}
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi  # type: ignore[method-assign]
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]


@app.exception_handler(BerundaError)
@app.exception_handler(NotFoundError)
@app.exception_handler(AuthenticationError)
@app.exception_handler(AuthorizationError)
@app.exception_handler(ValidationError)
@app.exception_handler(ConflictError)
@app.exception_handler(DatabaseError)
@app.exception_handler(AIServiceError)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    cid = getattr(request.state, "correlation_id", None)

    if isinstance(exc, BerundaError):
        status = exc.status_code
        code = exc.code
        message = exc.message
        detail = exc.detail
        log_level = "warning" if status < 500 else "error"
    else:
        status = 500
        code = "INTERNAL_ERROR"
        message = "An unexpected error occurred."
        detail = {}
        log_level = "error"

    extra = {"path": str(request.url), "correlation_id": cid}
    if log_level == "error":
        logger.error("Exception: %s", exc, extra=extra)
    else:
        logger.warning("Exception: %s", exc, extra=extra)

    return JSONResponse(
        status_code=status,
        content={
            "error": {"code": code, "message": message, **({"detail": detail} if detail else {})}
        },
    )


cors_origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/dashboard", StaticFiles(directory="public", html=True), name="dashboard")

app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

for r in [
    fir_router,
    entity_router,
    graph_router,
    hotspot_router,
    anomaly_router,
    risk_router,
    fairness_router,
    audit_router,
    auth_router,
    admin_router,
    ai_intelligence_router,
    investigation_router,
    analytics_router,
    geospatial_router,
    report_router,
    police_stations_router,
    persons_router,
    notification_router,
    webhook_router,
    related_cases_router,
    search_router,
    rag_router,
    dashboard_router,
]:
    app.include_router(getattr(r, "router", r))  # type: ignore[arg-type]


try:
    load_config()
except Exception:
    logger.warning("YAML config load failed — using env vars only", exc_info=True)


if prometheus_client is not None:
    REQUEST_COUNT = prometheus_client.Counter(
        "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
    )
    REQUEST_DURATION = prometheus_client.Histogram(
        "http_request_duration_seconds", "HTTP request duration", ["method", "endpoint"]
    )
    ACTIVE_SESSIONS = prometheus_client.Gauge("active_sessions", "Current active sessions")
    DB_CONNECTIONS = prometheus_client.Gauge("db_connections_in_use", "DB connections in use")

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        REQUEST_COUNT.labels(
            method=request.method, endpoint=request.url.path, status=response.status_code
        ).inc()
        REQUEST_DURATION.labels(method=request.method, endpoint=request.url.path).observe(duration)
        return response

    @app.get("/metrics", include_in_schema=False)
    async def metrics():
        return Response(
            media_type="text/plain",
            content=prometheus_client.generate_latest().decode("utf-8"),
        )


@app.get("/")
async def root():
    return {"service": "Berunda", "version": "0.1.0", "status": "running"}


@app.get("/health")
async def health(request: Request):
    uptime_seconds = time.time() - _start_time
    db_live = False
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            await conn.execute(sa.text("SELECT 1"))
        db_live = True
    except Exception as exc:
        logger.debug("Health check DB connection failed: %s", exc)
    checks = {
        "python": True,
        "database": db_live,
        "uptime_seconds": uptime_seconds,
    }
    neo = getattr(request.app.state, "neo4j_service", None)
    if neo:
        checks["neo4j"] = True
    overall = "healthy" if db_live else "degraded"
    return {
        "status": overall,
        "version": "0.4.0",
        "checks": checks,
    }


@app.get("/ready")
async def readiness(request: Request):
    db_ok = getattr(request.app.state, "db_connected", False)
    checks = {
        "python": True,
        "database": db_ok,
    }
    neo = getattr(request.app.state, "neo4j_service", None)
    if neo:
        checks["neo4j"] = neo.enabled
    overall = "ready" if db_ok else "degraded"
    return {
        "status": overall,
        "checks": checks,
    }


@app.get("/api/v1/status")
async def api_status():
    return {
        "api_version": "v1",
        "environment": os.environ.get("APP_ENV", "development"),
        "service": "Berunda",
        "status": "operational",
    }
