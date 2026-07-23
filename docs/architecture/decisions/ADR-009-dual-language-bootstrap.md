# ADR-009: Dual-Language Bootstrap Strategy

**Status:** APPROVED
**Date:** 2026-07-20

---

## Context

The Berunda repository contains both Python modules (`src/ai`, `src/ml`, `src/pipelines`, `src/shared`) and Node.js applications (`apps/web`, `apps/api`, `apps/worker`). The Phase 1 bootstrap must create a runnable minimum application that validates the architecture before full feature development begins.

The choices are:
1. Bootstrap a Python FastAPI server (since the ML/AI modules are Python)
2. Bootstrap a Node.js Express/Fastify server (since the API functions are Node.js)
3. Bootstrap both — a minimal FastAPI backend with health endpoints AND a minimal Express API

## Decision

Bootstrap a **Python FastAPI server** as the primary health/readiness endpoint provider, with a **Node.js Express server** as the secondary API entry point.

Rationale:
- Python is the primary language for ML/AI components, which are the core differentiator
- The test infrastructure (`tests/conftest.py`) already references `src.main` (FastAPI)
- The middleware code in `apps/api` (Node.js) is Catalyst-specific and cannot run locally without the Catalyst SDK
- A FastAPI server provides native health checks, OpenAPI docs, and async support
- Docker Compose is configured for `api` (Node.js) but the Node.js API has no server entry point (`index.js` referenced in Dockerfile does not exist)
- FastAPI runs on uvicorn which is in the Python ecosystem already installed

## Alternatives Considered

1. **Pure Node.js Express** — Rejected because the Catalyst SDK is required for actual data operations; without it the API is a stub that duplicates the test scenario
2. **Pure Python FastAPI** — Rejected because the frontend build requires Node.js and the workspace architecture documents both
3. **No local server** — Rejected because Phase 1 requires a runnable application

## Consequences

- Positive: FastAPI provides automatic OpenAPI docs at `/docs`
- Positive: FastAPI async support aligns with Python 3.13+ capabilities
- Positive: Health endpoints are trivial to implement and test
- Positive: Existing pytest fixtures for `async_client` will work immediately
- Negative: We now maintain two API entry points (Python FastAPI locally, Node.js Catalyst in production)
- Negative: API routes must be duplicated across both environments or abstracted

## Security Impact

- Health endpoints expose no sensitive data
- Root endpoint returns minimal system info (version only)
- No authentication on health endpoints (by design)

## Operational Impact

- Local dev: `make dev` starts FastAPI on port 8000 + Vite on port 5173
- Production: Catalyst Functions handle all routing
- CI: Python tests run against FastAPI; Node tests run against components

## Reversal Strategy

When Catalyst Functions can be fully emulated locally, the FastAPI bootstrap can be replaced with a Catalyst SDK-based local server. For now, FastAPI provides the quickest path to a runnable application.
