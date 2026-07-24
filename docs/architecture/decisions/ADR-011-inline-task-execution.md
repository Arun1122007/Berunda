# ADR-011: Inline Task Execution Pattern (Phase 1)

**Status:** APPROVED
**Date:** 2026-07-24
**Classification:** INTERNAL
**Owner:** Architecture Lead

---

## Context

The Phase 1 architecture specifies Celery + Redis for background task execution (risk scoring, anomaly detection, notifications). Three task modules exist in `src/tasks/` with Celery `@shared_task` decorators, and `src/worker.py` configures a Celery app with a Redis broker and beat scheduler.

The following issues were encountered:
1. **Celery is not installed** in the development environment — `pip list` shows no `celery` package
2. **Redis is not running** in local dev — Docker Compose provides `redis:7-alpine` but it is not started by default and CI tests use SQLite (no Redis)
3. **Task methods referenced non-existent service methods** — `risk_scoring.py` called `RiskService.compute_sync()` (doesn't exist), `anomaly.py` called `svc.detect_anomalies()` (didn't exist)
4. **Test suite failed on Celery import** — `ModuleNotFoundError: No module named 'celery'` during `_trigger_post_fir_tasks`

## Decision

Replace Celery-based background task dispatch with direct inline async execution.

### What Changed

| Before | After |
|--------|-------|
| `from celery import shared_task` decorator on every task | Plain Python functions with inner `async _run()` + `asyncio.run()` |
| `task.delay(case_master_id)` for dispatch | `task(case_master_id)` direct call |
| Celery Beat for periodic scheduling (6h anomaly scan, 24h risk recompute) | Removed — no periodic scheduling in Phase 1 |
| Redis as Celery broker | No broker dependency |
| `src/worker.py` Celery app config | `celery_app = None` with try/except ImportError (graceful fallback) |

### Rationale

1. **Demo constraints** — The Hack2Skill Datathon demo operates with ~2,000 synthetic records. All background tasks complete within seconds. Async parallelism is unnecessary.
2. **Infrastructure simplicity** — Removing the Redis dependency eliminates a Docker service, a configuration variable, and a potential local-dev failure point.
3. **Graceful degradation** — FIR creation calls tasks inline; if the task fails (e.g., database unavailable), the FIR creation still succeeds. The error is logged but does not block the response.
4. **Celery remains optional** — `src/worker.py` still imports Celery if the package is installed. A production deployment with Redis can re-enable Celery by installing the package and setting `CELERY_BROKER_URL`.

## Consequences

### Positive
- Zero-infrastructure background tasks — works with any database backend (SQLite, PostgreSQL)
- Simpler local development — no Redis process needed
- Immediate task execution — no broker latency
- Test suite no longer requires Celery mock or Redis fixture

### Negative
- No task retry mechanism — if a task fails, it is not retried automatically
- No task queue — concurrent task dispatch blocks the request handler until completion
- No periodic scheduling — the 6-hour anomaly scan and 24-hour risk recompute are inactive
- Not suitable for production scale — beyond ~10K records, inline execution could cause request timeouts

### Mitigation
- For Phase 1 demo scale (2,000 records), all tasks complete in under 2 seconds
- FIR creation endpoint wraps task dispatch in `try/except` with logging — the HTTP response is never blocked by task failure
- Phase 2 can reintroduce Celery by installing the package, launching a Redis container, and swapping `task()` → `task.delay()` — the task code remains unchanged

## Compliance

This ADR does not contradict any existing ADR. ADR-001 (Phase 1 Architectural Style) specifies "Modular Functions + API Gateway" but does not mandate Celery. ADR-002 (Catalyst Deployment Boundaries) lists Redis as a dependency but this ADR replaces it with inline execution for Phase 1, consistent with ADR-008's MVP-vs-Target-State scoping.

The validated architecture document (`phase-1-validated-architecture.md`) and the risk register must be updated to reflect this decision.
