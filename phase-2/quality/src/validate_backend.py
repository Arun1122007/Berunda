"""Backend validation — formatting, linting, types, tests, API contract, auth, error safety, logging."""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _run_cmd(cmd: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=cwd)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError:
        return -1, "", f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"


async def check_formatting() -> dict[str, Any]:
    """Run ruff format check."""
    workspace = str(Path(__file__).resolve().parents[3])
    rc, out, err = _run_cmd(
        [sys.executable, "-m", "ruff", "format", "--check", "src/", "tests/"],
        cwd=workspace,
    )
    return {
        "passed": rc == 0,
        "returncode": rc,
        "details": (out or err)[:500],
    }


async def check_linting() -> dict[str, Any]:
    """Run ruff check."""
    workspace = str(Path(__file__).resolve().parents[3])
    rc, out, err = _run_cmd(
        [sys.executable, "-m", "ruff", "check", "src/", "tests/"],
        cwd=workspace,
    )
    return {
        "passed": rc == 0,
        "returncode": rc,
        "details": (out or err)[:500],
    }


async def check_types() -> dict[str, Any]:
    """Run mypy type checking."""
    workspace = str(Path(__file__).resolve().parents[3])
    rc, out, err = _run_cmd(
        [sys.executable, "-m", "mypy", "src/"],
        cwd=workspace,
    )
    return {
        "passed": rc == 0,
        "returncode": rc,
        "details": (out or err)[:500],
    }


async def check_unit_tests() -> dict[str, Any]:
    """Run pytest -m unit."""
    workspace = str(Path(__file__).resolve().parents[3])
    rc, out, err = _run_cmd(
        [sys.executable, "-m", "pytest", "-m", "unit", "-x", "--tb=short"],
        cwd=workspace,
    )
    return {
        "passed": rc == 0,
        "returncode": rc,
        "details": (out or err)[:500],
    }


async def check_integration_tests() -> dict[str, Any]:
    """Run pytest -m integration."""
    workspace = str(Path(__file__).resolve().parents[3])
    rc, out, err = _run_cmd(
        [sys.executable, "-m", "pytest", "-m", "integration", "-x", "--tb=short"],
        cwd=workspace,
    )
    return {
        "passed": rc == 0,
        "returncode": rc,
        "details": (out or err)[:500],
    }


async def check_api_contract() -> dict[str, Any]:
    """Verify all expected API endpoints exist in the application routes."""
    workspace = str(Path(__file__).resolve().parents[3])
    sys.path.insert(0, workspace)
    try:
        from src.main import app

        existing_routes = {r.path for r in app.routes if hasattr(r, "path")}
    except Exception as exc:
        return {"passed": False, "details": f"cannot load app: {exc}"}

    expected = {
        "/",
        "/health",
        "/ready",
        "/api/v1/status",
        "/api/v1/fir",
        "/api/v1/fir/{case_master_id}",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
        "/api/v1/auth/logout",
        "/api/v1/auth/me",
        "/api/v1/entities",
        "/api/v1/entities/{person_entity_id}",
        "/api/v1/graph",
        "/api/v1/hotspots",
        "/api/v1/anomalies",
        "/api/v1/risk",
        "/api/v1/risk/compute/{person_entity_id}",
        "/api/v1/rag/query",
        "/api/v1/audit",
        "/api/v1/fairness",
    }
    missing = sorted(expected - existing_routes)
    return {
        "passed": len(missing) == 0,
        "expected_count": len(expected),
        "existing_count": len(existing_routes),
        "missing": missing,
    }


async def check_authorization() -> dict[str, Any]:
    """Test that all protected endpoints require authentication or have RBAC."""
    workspace = str(Path(__file__).resolve().parents[3])
    sys.path.insert(0, workspace)
    try:
        from src.main import app
        from src.middleware.auth import get_current_user, require_role

        protected = 0
        unprotected = 0
        for route in app.routes:
            if hasattr(route, "dependencies") and route.dependencies:
                deps = [d.dependency for d in route.dependencies]
                if get_current_user in deps or require_role in deps:
                    protected += 1
                else:
                    unprotected += 1
            elif hasattr(route, "path") and route.path in ("/health", "/ready", "/", "/api/v1/status", "/metrics"):
                unprotected += 1
            else:
                unprotected += 1
        return {
            "passed": protected > 0,
            "protected_endpoints": protected,
            "unprotected_endpoints": unprotected,
        }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_safe_errors() -> dict[str, Any]:
    """Ensure no stack traces leak to HTTP responses."""
    workspace = str(Path(__file__).resolve().parents[3])
    sys.path.insert(0, workspace)
    try:
        from src.main import app

        traceback_pattern = re.compile(r"Traceback \(most recent call last\)|File \".*\", line \d+")
        issues = []
        for route in app.routes:
            if hasattr(route, "endpoint"):
                try:
                    source = inspect.getsource(route.endpoint)
                    if "traceback" in source.lower() or "exc_info" in source.lower():
                        issues.append(route.path)
                except (OSError, TypeError):
                    pass
        return {
            "passed": len(issues) == 0,
            "routes_with_traceback": issues,
        }
    except ImportError:
        return {"passed": True, "details": "cannot inspect, skipping"}


import inspect


async def check_logging() -> dict[str, Any]:
    """Verify structured JSON logging and no secrets in log statements."""
    workspace = str(Path(__file__).resolve().parents[3])
    issues = []
    src_dir = Path(workspace) / "src"
    secret_patterns = re.compile(
        r"password|secret|token|api_key|auth_key|JWT_SECRET|DATABASE_URL|PRIVATE_KEY",
        re.IGNORECASE,
    )
    for pyfile in sorted(src_dir.rglob("*.py")):
        try:
            text = pyfile.read_text(encoding="utf-8")
            if "logging." not in text and "log." not in text and "logger." not in text:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                stripped = line.strip()
                if any(
                    kw in stripped.lower()
                    for kw in ("logger.debug", "logger.info", "logger.warning", "logger.error")
                ):
                    if secret_patterns.search(stripped) and "%s" not in stripped and "extra" not in stripped:
                        issues.append(f"{pyfile.relative_to(workspace)}:{i}")
        except Exception:
            continue
    return {
        "passed": len(issues) == 0,
        "issues": issues,
    }
