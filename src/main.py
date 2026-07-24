"""Berunda FastAPI application — AI-Native Crime Intelligence Platform."""

from __future__ import annotations

import os
import time
from contextlib import asynccontextmanager, suppress
from pathlib import Path
from typing import Any

import sqlalchemy as sa
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.database import get_engine
from src.routers import (
    anomaly_router,
    audit_router,
    auth_router,
    entity_router,
    fairness_router,
    fir_router,
    graph_router,
    hotspot_router,
    notification_router,
    rag_router,
    risk_router,
)
from src.routers.rag_router import limiter
from src.shared.config import load_config
from src.shared.logging import get_logger

try:
    import prometheus_client
except ImportError:
    prometheus_client = None  # Metrics disabled

# Load .env before any config reads environment variables
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logger = get_logger(__name__)
start_time = time.time()

tags_metadata = [
    {
        "name": "FIR",
        "description": "First Information Report CRUD — the core case record. Supports list, get, create, update, delete with district-scoped access for non-admin users.",  # noqa: E501
    },
    {
        "name": "Entity",
        "description": "Person entity resolution — list, search, merge duplicate identities across cases.",  # noqa: E501
    },
    {
        "name": "Graph",
        "description": "Entity relationship graph — traverse person-to-person connections with configurable depth and confidence thresholds.",  # noqa: E501
    },
    {
        "name": "Hotspot",
        "description": "Crime hotspot analysis — spatial clustering for geographic pattern detection.",  # noqa: E501
    },
    {
        "name": "Anomaly",
        "description": "Anomaly detection — identify unusual case patterns for investigation leads.",  # noqa: E501
    },
    {
        "name": "Risk",
        "description": "Risk scoring — compute recidivism, recency, and severity scores for persons of interest.",  # noqa: E501
    },
    {
        "name": "RAG",
        "description": "Retrieval-Augmented Generation — semantic search over FIR corpus with LLM-powered answers. Rate-limited to 5 req/min.",  # noqa: E501
    },
    {
        "name": "Fairness",
        "description": "Fairness audit — bias detection across demographic dimensions in case outcomes.",  # noqa: E501
    },
    {
        "name": "Audit",
        "description": "Audit log — immutable trail of data access and modifications for compliance.",  # noqa: E501
    },
    {
        "name": "Auth",
        "description": "Authentication & authorization — JWT login, registration, token refresh, logout, and role-based access control (admin/officer/analyst).",  # noqa: E501
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup", {"version": "0.4.0"})
    app.state.start_time = start_time
    db_ok = False
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            await conn.execute(sa.text("SELECT 1"))
        db_ok = True
        logger.info("Database connection verified")
    except Exception as exc:
        logger.warning("Database not available at startup", exc_info=exc)
    app.state.db_connected = db_ok

    from src.services.notification_service import NotificationService

    app.state.notification_service = NotificationService()
    logger.info("Notification service initialized")

    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="Berunda API",
    version="0.4.0",
    description="AI-Native Crime Intelligence Platform — real-time FIR management, entity resolution, risk scoring, anomaly detection, hotspot analysis, and RAG-powered case search.",  # noqa: E501
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


app.openapi = custom_openapi
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fir_router)
app.include_router(entity_router)
app.include_router(graph_router)
app.include_router(hotspot_router)
app.include_router(anomaly_router)
app.include_router(risk_router)
app.include_router(rag_router)
app.include_router(fairness_router)
app.include_router(audit_router)
app.include_router(auth_router)
app.include_router(notification_router)

with suppress(Exception):
    load_config()


if prometheus_client is not None:
    REQUEST_COUNT = prometheus_client.Counter(
        "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
    )
    REQUEST_DURATION = prometheus_client.Histogram(
        "http_request_duration_seconds", "HTTP request duration", ["method", "endpoint"]
    )
    ACTIVE_SESSIONS = prometheus_client.Gauge("active_sessions", "Current active sessions")
    DB_CONNECTIONS = prometheus_client.Gauge("db_connections_in_use", "DB connections in use")
    CELERY_QUEUE_DEPTH = prometheus_client.Gauge("celery_queue_depth", "Celery task queue depth")

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


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=exc, extra={"path": str(request.url)})
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred.",
            }
        },
    )


@app.get("/")
async def root():
    return {"service": "Berunda", "version": "0.1.0", "status": "running"}


@app.get("/health")
async def health():
    uptime_seconds = time.time() - start_time
    return {
        "status": "healthy",
        "version": "0.1.0",
        "uptime_seconds": uptime_seconds,
    }


@app.get("/ready")
async def readiness(request: Request):
    db_ok = getattr(request.app.state, "db_connected", False)
    return {
        "status": "ready" if db_ok else "degraded",
        "checks": {
            "python": True,
            "database": db_ok,
        },
    }


@app.get("/api/v1/status")
async def api_status():
    return {
        "api_version": "v1",
        "environment": os.environ.get("APP_ENV", "development"),
        "service": "Berunda",
        "status": "operational",
    }
