"""Berunda Phase 2 Backend — Clean Architecture FastAPI Application."""

from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.infrastructure.logging import setup_logging
from src.infrastructure.middleware import CorrelationIDMiddleware, ErrorHandlerMiddleware, SecurityHeadersMiddleware
from src.transport.routes import auth_router, fir_router

setup_logging()
logger = logging.getLogger(__name__)
_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Berunda Phase 2 Backend starting", extra={"version": "0.2.0"})
    yield
    logger.info("Berunda Phase 2 Backend shutting down")


app = FastAPI(
    title="Berunda API — Phase 2",
    version="0.2.0",
    description="FIR Case Management Backend — Clean Architecture with domain-driven design, RBAC, and structured error responses.",
    lifespan=lifespan,
    contact={
        "name": "Berunda Team",
        "url": "https://github.com/Arun1122007/Berunda",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Local development"},
    ],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(ErrorHandlerMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    cid = getattr(request.state, "correlation_id", str(uuid.uuid4()))
    logger.warning("Validation error: %s path=%s", exc.errors(), request.url.path)
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed",
                "detail": {"fields": exc.errors()},
                "requestId": cid,
            }
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    cid = getattr(request.state, "correlation_id", str(uuid.uuid4()))
    logger.exception("Unhandled exception: %s path=%s", exc, request.url.path)
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


app.include_router(fir_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"service": "Berunda", "version": "0.2.0", "phase": "2", "status": "running"}


@app.get("/health")
async def health():
    uptime = time.time() - _start_time
    return {"status": "healthy", "version": "0.2.0", "uptime_seconds": uptime}


@app.get("/api/v1/status")
async def api_status():
    return {
        "api_version": "v1",
        "environment": "development",
        "service": "Berunda",
        "status": "operational",
    }
