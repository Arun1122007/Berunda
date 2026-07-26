# 02 — Environment and Configuration Report

**Document ID:** BERUNDA-IMPL3-ENV-001
**Version:** 1.0 | **Status:** FINAL
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

## 1. Objective
Establish and document a consistent, secure, repeatable development foundation across backend and frontend environments according to the Phase 2 architectural constraints.

## 2. Repository Structure
The monorepo is divided strictly into `apps` (for application frontends/backends), `src` (for primary Python backend modules), `data` (synthetic generation), and `docs` (architecture).

```text
D:\Hack2Skill\Berunda\
├── apps/
│   └── web/                   # Vite React SPA (Frontend)
├── src/                       # FastAPI Backend
│   ├── alembic/               # Database migrations
│   ├── models/                # SQLAlchemy models
│   ├── routers/               # API endpoints
│   ├── services/              # Core business logic
│   └── shared/                # Security & Config helpers
├── docs/                      # Phase 2 & 3 Architecture
├── data/                      # Synthetic bounds, seeds
└── tests/                     # Test suites (unit, db, api)
```

## 3. Runtime Versions & Dependency Strategy
| Component | Runtime | Strategy | Manifest |
|---|---|---|---|
| Backend | Python 3.11+ | `pip` strict locking | `requirements.txt` |
| Frontend | Node.js 18+ | `npm` standard lock | `apps/web/package.json` |

### Key Dependencies
* **Backend:** `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `spacy`, `scikit-learn` (ADR-011 enforces removal of Celery/Redis).
* **Frontend:** `react 18`, `vite`, `maplibre-gl`, `cytoscape` (defined in `apps/web/package.json`).

## 4. Environment Variables
Centralized configuration is driven by `src/config.py` using `pydantic_settings`.

A secure placeholder `.env.example` has been established defining:
* `APP_ENV`: `development` / `production`
* `LOG_LEVEL`: Application logging granularity.
* `DATABASE_URL`: Connection string (SQLite locally).
* `JWT_SECRET_KEY`: Required 256-bit hex signing key.
* `OPENAI_API_KEY`, `GROQ_API_KEY`: Secrets for AI fallback.
* `DEFAULT_AI_PROVIDER`: Typically `mock` in dev.
* `CORS_ORIGINS`: Allowed cross-origin boundaries.

**Secret-handling Rules:**
* Real secrets are NEVER committed to git.
* `git-secrets` must be run pre-commit.
* Secrets are loaded at runtime only, never embedded in JS bundles unless prefixed with `VITE_` (and containing safe public config).

## 5. Local Developer Workflow (Makefile)
A unified `Makefile` ensures developers can bootstrap efficiently:
* `make install`: Installs Python and Node dependencies.
* `make dev-backend`: Runs FastAPI on port 9000.
* `make dev-frontend`: Runs Vite on port 5173.
* `make lint`: Ruff (Python) & ESLint (Node).
* `make typecheck`: Mypy (Python) & tsc (Node).
* `make test`: Pytest suites.
* `make seed-demo`: Bootstraps SQLite database with synthetic records.

## 6. Backend Bootstrap Validation
FastAPI is configured with:
* Root metadata at `/` and `/api/v1/status`
* Health endpoints at `/health` and `/ready`
* Structured Error Responses mapping custom `BerundaError` to unified JSON schemas.
* Correlation IDs automatically added to all requests (`CorrelationIDMiddleware`).

## 7. Frontend Bootstrap Validation
The Vite React shell is configured with:
* TypeScript (`tsc`) for static analysis.
* Vitest configured alongside ESLint and TailwindCSS.
* Start command: `npm run dev`.

## 8. Remaining Blockers
* Implementation of `alembic` migration bridging current `src/models` state to final Phase 2 designs.
* Implementation of the Phase 3 `scripts/data/generate_synthetic.py` seed script to populate SQLite.

*Status: READY FOR DATABASE FOUNDATION.*
