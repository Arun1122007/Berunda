"""Berunda FastAPI application — Health, readiness, and status endpoints."""

from __future__ import annotations

import os
import time
from contextlib import asynccontextmanager

import sqlalchemy as sa
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    rag_router,
    risk_router,
)
from src.shared.config import load_config
from src.shared.logging import get_logger

logger = get_logger(__name__)
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup", {"version": "0.1.0"})
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
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="Berunda API",
    version="0.1.0",
    description="AI-Native Crime Intelligence Platform API",
    lifespan=lifespan,
)

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

try:
    load_config()
except Exception:
    pass


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
