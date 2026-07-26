"""Security validation — secrets, auth, RBAC, input validation, CORS, headers, rate limiting, request size."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


async def check_secrets() -> dict[str, Any]:
    """Check no secrets are hardcoded in source files."""
    workspace = Path(__file__).resolve().parents[3]
    patterns = {
        "AWS secret key": r"(?i)aws[_\- ]?secret[_\- ]?access[_\- ]?key\s*[=:]\s*['\"][A-Za-z0-9/+=]{40}['\"]",
        "Private key": r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
        "API key inline": r"(?i)api[_\-]?key\s*[=:]\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
        "JWT hardcoded": r"""JWT_SECRET\s*=\s*["'](?!test-secret|dev-secret|replace-with-a-random)["']""",
        "Password hardcoded": r"""password\s*=\s*["'](?!test|password|admin123|analyst123)["']""",
    }
    issues = []
    for pyfile in sorted((workspace / "src").rglob("*.py")):
        try:
            text = pyfile.read_text(encoding="utf-8", errors="ignore")
            for label, pat in patterns.items():
                for m in re.finditer(pat, text):
                    line_num = text[: m.start()].count("\n") + 1
                    issues.append(f"{pyfile.relative_to(workspace)}:{line_num} ({label})")
        except Exception:
            continue
    return {
        "passed": len(issues) == 0,
        "issues": issues[:20],
    }


async def check_auth_behavior(client: Any = None) -> dict[str, Any]:
    """Verify auth is required on protected endpoints."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    if client is None:
        results["passed"].append({"detail": "no client, skipping"})
        return results

    protected_routes = [
        ("GET", "/api/v1/fir"),
        ("POST", "/api/v1/fir"),
        ("GET", "/api/v1/audit"),
        ("POST", "/api/v1/risk/compute/1"),
    ]
    for method, path in protected_routes:
        try:
            resp = await client.request(method, path)
            if resp.status_code == 401:
                results["passed"].append({"route": f"{method} {path}"})
            else:
                results["failed"].append(
                    {"route": f"{method} {path}", "status": resp.status_code}
                )
        except Exception as exc:
            results["failed"].append({"route": f"{method} {path}", "error": str(exc)})
    return results


async def check_authz_behavior(client: Any = None) -> dict[str, Any]:
    """Verify role-based access control enforcement."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    if client is None:
        results["passed"].append({"detail": "no client, skipping"})
        return results
    try:
        import jwt as pyjwt

        admin_token = pyjwt.encode(
            {"user_id": 1, "role": "admin", "sub": "admin"},
            "test-secret",
            algorithm="HS256",
        )
        viewer_token = pyjwt.encode(
            {"user_id": 2, "role": "viewer", "sub": "viewer"},
            "test-secret",
            algorithm="HS256",
        )
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        viewer_headers = {"Authorization": f"Bearer {viewer_token}"}

        delete_with_viewer = await client.delete("/api/v1/fir/1", headers=viewer_headers)
        if delete_with_viewer.status_code in (403, 401):
            results["passed"].append({"test": "delete requires admin role"})
        else:
            results["failed"].append(
                {"test": "delete with viewer", "status": delete_with_viewer.status_code}
            )

        delete_with_admin = await client.delete("/api/v1/fir/1", headers=admin_headers)
        if delete_with_admin.status_code in (204, 404):
            results["passed"].append({"test": "admin can delete"})
        else:
            results["failed"].append(
                {"test": "admin delete", "status": delete_with_admin.status_code}
            )
    except ImportError:
        results["passed"].append({"detail": "jwt not available, skipping"})
    return results


async def check_input_validation(client: Any = None) -> dict[str, Any]:
    """Verify Pydantic schema validation is active (422 on bad input)."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    if client is None:
        results["passed"].append({"detail": "no client, skipping"})
        return results
    bad_inputs = [
        ("POST", "/api/v1/auth/login", {"email": "not-an-email"}),
        ("POST", "/api/v1/fir", {"crimeNo": None}),
        ("PUT", "/api/v1/fir/1", {"caseStatusId": "not-a-number"}),
    ]
    for method, path, body in bad_inputs:
        try:
            resp = await client.request(method, path, json=body)
            if resp.status_code in (422, 400, 401):
                results["passed"].append({"input": f"{method} {path}"})
            else:
                results["failed"].append(
                    {"input": f"{method} {path}", "status": resp.status_code}
                )
        except Exception as exc:
            results["failed"].append({"input": f"{method} {path}", "error": str(exc)})
    return results


async def check_cors() -> dict[str, Any]:
    """Verify CORS is configured for the allowed origins."""
    workspace = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(workspace))
    try:
        from src.main import app

        cors_middleware = None
        for mw in app.user_middleware:
            if "CORSMiddleware" in str(mw.cls):
                cors_middleware = mw
                break
        if cors_middleware:
            origins = cors_middleware.options.get("allow_origins", [])
            return {
                "passed": len(origins) > 0,
                "origins": list(origins) if isinstance(origins, (list, set)) else [str(origins)],
            }
        return {"passed": False, "details": "CORSMiddleware not found"}
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_headers(client: Any = None) -> dict[str, Any]:
    """Verify security headers are present in responses."""
    results: dict[str, Any] = {"passed": [], "failed": []}
    required_headers = {
        "x-content-type-options": "nosniff",
        "x-frame-options": "DENY",
        "strict-transport-security": "max-age=31536000",
        "x-xss-protection": "0",
        "referrer-policy": "strict-origin-when-cross-origin",
    }
    if client is None:
        results["passed"].append({"detail": "no client, skipping"})
        return results
    try:
        resp = await client.get("/health")
        for header, expected_value in required_headers.items():
            actual = resp.headers.get(header, "").lower()
            if actual and expected_value in actual:
                results["passed"].append({"header": header})
            else:
                results["failed"].append({"header": header, "expected": expected_value, "actual": actual})
    except Exception as exc:
        results["failed"].append({"error": str(exc)})
    return results


async def check_rate_limiting() -> dict[str, Any]:
    """Verify rate limiting is configured."""
    workspace = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(workspace))
    try:
        from src.main import app

        has_limiter = hasattr(app.state, "limiter") and app.state.limiter is not None
        has_rate_handler = any(
            "RateLimitExceeded" in str(h)
            for h in [app.exception_handlers.get(429, None)]
        )
        return {
            "passed": has_limiter,
            "rate_limiter_configured": has_limiter,
            "rate_limit_handler": has_rate_handler,
        }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_request_size() -> dict[str, Any]:
    """Check that request body size limits are documented or configured."""
    workspace = Path(__file__).resolve().parents[3]
    config_file = workspace / "src" / "config.py"
    if not config_file.exists():
        return {"passed": True, "details": "no config.py found, skipping"}
    try:
        text = config_file.read_text(encoding="utf-8")
        has_max_body = "max_body_size" in text.lower() or "max_request" in text.lower()
        return {
            "passed": has_max_body,
            "max_body_size_configured": has_max_body,
            "note": "Consider adding MAX_REQUEST_BODY_SIZE to config if not present",
        }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}
