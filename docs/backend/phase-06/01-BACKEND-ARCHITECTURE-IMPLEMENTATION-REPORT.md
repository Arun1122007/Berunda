# Phase 6 — Backend Architecture Implementation Report

## 1. Architecture Overview

The Berunda backend follows a layered architecture with clear separation of concerns:

```
Presentation Layer (FastAPI Routers)
    ↓
Application Layer (Services)
    ↓
Domain Layer (Validators, Lifecycle, Entities)
    ↓
Repository Layer (Abstract Interfaces)
    ↓
Data Access Layer (SQLite/Catalyst Adapters)
```

## 2. Module Structure

```
src/
├── main.py                    # FastAPI application entry point
├── config.py                  # Pydantic Settings
├── database.py                # Async SQLAlchemy engine + session
├── exceptions.py              # Domain exception hierarchy
├── dependencies.py            # FastAPI dependency injection
├── domain/                    # NEW — Domain logic
│   ├── fir_lifecycle.py       # FIR status state machine
│   ├── source_document.py     # Source document preservation
│   └── idempotency.py        # Idempotency key management
├── routers/                   # 24 API router modules
│   ├── fir_router.py          # FIR CRUD
│   ├── auth_router.py         # Authentication
│   ├── investigation_router.py # Notes, assignments, reviews
│   ├── search_router.py       # FIR search
│   ├── audit_router.py        # Audit log query
│   ├── dashboard_router.py    # Metrics
│   ├── report_router.py       # Report generation
│   ├── police_stations_router.py  # NEW — Station listing
│   ├── persons_router.py      # NEW — Person listing per FIR
│   └── ... (15 more)
├── services/                  # Business logic
│   ├── fir_service.py         # FIR operations
│   ├── auth_service.py        # Authentication
│   ├── audit_service.py       # Audit logging
│   └── ... (30+ services)
├── models/                    # SQLAlchemy ORM models
│   ├── src_models.py          # Source schema (CaseMaster, etc.)
│   ├── int_models.py          # Intelligence schema
│   ├── auth_models.py         # Authentication schema
│   ├── gov_models.py          # Governance schema
│   └── ai_models.py           # AI schema
├── repositories/              # Data access layer
│   ├── core.py                # Abstract repository interfaces
│   ├── sqlite_adapter.py      # SQLite implementations
│   ├── catalyst_adapter.py    # Catalyst implementations
│   └── factory.py             # Environment-aware factory
├── middleware/
│   └── auth.py                # JWT authentication + RBAC
├── ai/                        # AI agent framework
├── ml/                        # ML training/inference
└── tasks/                     # Celery background tasks
```

## 3. Layered Enforcement

| Rule | Status |
|------|--------|
| Routes delegate to services | ✅ Enforced |
| Services use repositories | ✅ Enforced |
| Authorization in middleware | ✅ Enforced |
| Business rules in domain layer | ✅ NEW: fir_lifecycle.py |
| Audit in centralized service | ✅ Enforced |
| AI provider abstraction | ✅ Enforced |
| No circular dependencies | ✅ Verified |

## 4. API Versioning

All routes are under `/api/v1/` prefix. Health endpoints are unversioned.

## 5. Newly Added Modules (Phase 6)

| Module | Purpose |
|--------|---------|
| `domain/fir_lifecycle.py` | Explicit state machine with 10 states and validated transitions |
| `domain/source_document.py` | Source type enum, validation rules, FIRSource dataclass |
| `domain/idempotency.py` | Idempotency key generation, in-memory store, scope enum |
| `routers/police_stations_router.py` | Station listing, detail, district listing |
| `routers/persons_router.py` | Complainants, victims, accused, act-sections per FIR |
| `tests/phase6/test_fir_lifecycle.py` | 30 unit tests covering lifecycle, source docs, idempotency |
| `tests/phase6/test_phase6_full_workflow.py` | 30 integration tests (36 unit + improved patterns) |
