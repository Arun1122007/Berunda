"""Complete CI checklist — runs ALL quality checks and returns pass/fail for each."""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from quality.src.validate_functional import (
    check_acceptance_criteria,
    check_invalid_input,
    check_unauthorized,
    check_forbidden,
    check_not_found,
)
from quality.src.validate_backend import (
    check_formatting,
    check_linting,
    check_types,
    check_unit_tests,
    check_integration_tests,
    check_api_contract,
    check_authorization,
    check_safe_errors,
    check_logging,
)
from quality.src.validate_database import (
    check_clean_migration,
    check_constraints,
    check_indexes,
    check_seed_data,
    check_reset,
    check_sensitive_data,
)
from quality.src.validate_security import (
    check_secrets,
    check_auth_behavior,
    check_authz_behavior,
    check_input_validation,
    check_cors,
    check_headers,
    check_rate_limiting,
    check_request_size,
)
from quality.src.validate_reliability import (
    check_startup,
    check_health,
    check_readiness,
    check_graceful_shutdown,
)
from quality.src.validate_performance import (
    check_n_plus_one,
    check_indexes_used,
    check_bundle_size,
)


async def all_checks(client: Any = None, db_session: Any = None) -> dict[str, dict[str, Any]]:
    """Run ALL validation checks and return pass/fail for each.

    Returns:
        dict of check_name -> {"passed": bool, "details": str, "duration_ms": float}
    """
    results: dict[str, dict[str, Any]] = {}

    check_fns = {
        # Functional
        "acceptance_criteria": lambda: check_acceptance_criteria(client),
        "invalid_input": lambda: check_invalid_input(client),
        "unauthorized": lambda: check_unauthorized(client),
        "forbidden": lambda: check_forbidden(client),
        "not_found": lambda: check_not_found(client),
        # Backend
        "formatting": check_formatting,
        "linting": check_linting,
        "types": check_types,
        "unit_tests": check_unit_tests,
        "integration_tests": check_integration_tests,
        "api_contract": check_api_contract,
        "authorization": lambda: check_authorization(),
        "safe_errors": check_safe_errors,
        "logging": check_logging,
        # Database
        "clean_migration": lambda: check_clean_migration(db_session),
        "constraints": lambda: check_constraints(db_session),
        "indexes": lambda: check_indexes(db_session),
        "seed_data": lambda: check_seed_data(db_session),
        "reset": lambda: check_reset(db_session),
        "sensitive_data": lambda: check_sensitive_data(db_session),
        # Security
        "secrets": check_secrets,
        "auth_behavior": lambda: check_auth_behavior(client),
        "authz_behavior": lambda: check_authz_behavior(client),
        "input_validation": lambda: check_input_validation(client),
        "cors": check_cors,
        "headers": lambda: check_headers(client),
        "rate_limiting": check_rate_limiting,
        "request_size": check_request_size,
        # Reliability
        "startup": lambda: check_startup(client),
        "health": lambda: check_health(client),
        "readiness": lambda: check_readiness(client),
        "graceful_shutdown": check_graceful_shutdown,
        # Performance
        "n_plus_one": lambda: check_n_plus_one(db_session),
        "indexes_used": lambda: check_indexes_used(db_session),
        "bundle_size": check_bundle_size,
    }

    for name, fn in check_fns.items():
        start = time.monotonic()
        try:
            result = await asyncio.wait_for(fn(), timeout=120)
            if isinstance(result, dict):
                passed = result.pop("passed", False)
                results[name] = {
                    "passed": passed,
                    "details": result,
                    "duration_ms": round((time.monotonic() - start) * 1000, 1),
                }
            else:
                results[name] = {
                    "passed": bool(result),
                    "duration_ms": round((time.monotonic() - start) * 1000, 1),
                }
        except asyncio.TimeoutError:
            results[name] = {
                "passed": False,
                "details": "timeout after 120s",
                "duration_ms": round((time.monotonic() - start) * 1000, 1),
            }
        except Exception as exc:
            results[name] = {
                "passed": False,
                "details": str(exc),
                "duration_ms": round((time.monotonic() - start) * 1000, 1),
            }

    return results


def format_results(results: dict[str, dict[str, Any]]) -> str:
    """Format checklist results as a human-readable table."""
    lines = []
    lines.append("=" * 80)
    lines.append("BERUNDA QUALITY CHECKLIST — RESULTS")
    lines.append("=" * 80)
    lines.append("")

    categories = {
        "Functional": ["acceptance_criteria", "invalid_input", "unauthorized", "forbidden", "not_found"],
        "Backend": ["formatting", "linting", "types", "unit_tests", "integration_tests", "api_contract", "authorization", "safe_errors", "logging"],
        "Database": ["clean_migration", "constraints", "indexes", "seed_data", "reset", "sensitive_data"],
        "Security": ["secrets", "auth_behavior", "authz_behavior", "input_validation", "cors", "headers", "rate_limiting", "request_size"],
        "Reliability": ["startup", "health", "readiness", "graceful_shutdown"],
        "Performance": ["n_plus_one", "indexes_used", "bundle_size"],
    }

    passed = failed = skipped = 0
    for cat, names in categories.items():
        lines.append(f"\n[{cat}]")
        lines.append("-" * 80)
        for name in names:
            r = results.get(name, {})
            p = r.get("passed", False)
            detail = r.get("details", {})
            ms = r.get("duration_ms", 0)
            icon = "PASS" if p else ("SKIP" if isinstance(detail, dict) and detail.get("detail", "").startswith("no") else "FAIL")
            if icon == "PASS":
                passed += 1
            elif icon == "FAIL":
                failed += 1
            else:
                skipped += 1
            d_str = ""
            if isinstance(detail, dict):
                d_str = "; ".join(f"{k}={v}" for k, v in sorted(detail.items()) if v)
            lines.append(f"  [{icon}] {name:25s} ({ms:>7.1f}ms) {d_str[:100]}")

    lines.append("")
    lines.append("=" * 80)
    lines.append(f"SUMMARY: {passed} passed, {failed} failed, {skipped} skipped")
    lines.append("=" * 80)
    return "\n".join(lines)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(all_checks())
        print(format_results(results))
        total = len(results)
        failed_count = sum(1 for r in results.values() if not r.get("passed", False))
        sys.exit(1 if failed_count > 0 else 0)
    finally:
        loop.close()
