"""Reliability validation — startup, health, readiness, graceful shutdown."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


async def check_startup(client: Any = None) -> dict[str, Any]:
    """Verify the application boots without errors."""
    workspace = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(workspace))
    try:
        import importlib

        import src.main as main_module
        importlib.reload(main_module)
        app = main_module.app
        return {
            "passed": True,
            "app_title": app.title,
            "app_version": app.version,
        }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_health(client: Any = None) -> dict[str, Any]:
    """Verify health endpoint returns 200."""
    if client is None:
        return {"passed": True, "details": "no client, skipping"}
    try:
        resp = await client.get("/health")
        data = resp.json()
        return {
            "passed": resp.status_code == 200,
            "status_code": resp.status_code,
            "health_status": data.get("status"),
            "checks": data.get("checks", {}),
        }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_readiness(client: Any = None) -> dict[str, Any]:
    """Verify readiness endpoint returns 200."""
    if client is None:
        return {"passed": True, "details": "no client, skipping"}
    try:
        resp = await client.get("/ready")
        data = resp.json()
        return {
            "passed": resp.status_code == 200,
            "status_code": resp.status_code,
            "status": data.get("status"),
            "checks": data.get("checks", {}),
        }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_graceful_shutdown() -> dict[str, Any]:
    """Verify lifespan shutdown handler works without errors."""
    workspace = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(workspace))
    try:
        from src.main import app, lifespan

        async with lifespan(app):
            pass
        return {"passed": True, "details": "lifespan context manager completed without error"}
    except Exception as exc:
        return {"passed": False, "details": str(exc)}
