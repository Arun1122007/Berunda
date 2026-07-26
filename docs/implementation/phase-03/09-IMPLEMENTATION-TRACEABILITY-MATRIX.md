# Implementation Traceability Matrix — Phase 3

> **Document ID:** BERUNDA-PH3-REPORT-09 | **Version:** 1.0 | **Status:** FINAL
> **Date:** 2026-07-26

---

## 1. ADR to Implementation Mapping

| ADR | Title | Phase 3 Implementation | Status |
|---|---|---|---|
| ADR-001 | Monorepo Structure | Workspace layout, `src/`, `apps/`, `docs/` | ✅ |
| ADR-002 | Python 3.13 FastAPI Backend | `src/main.py`, `src/routers/` | ✅ |
| ADR-003 | SQLAlchemy + Alembic DB Layer | `src/models/`, `src/alembic/` | ✅ |
| ADR-004 | Repository Pattern | `src/repositories/`, `src/dependencies.py` | ⚠️ Partial |
| ADR-005 | Pydantic v2 Settings | `src/config.py` | ✅ |
| ADR-006 | JWT Auth with bcrypt | `src/middleware/auth.py`, `src/services/auth_service.py` | ✅ |
| ADR-007 | RBAC + ABAC | `src/domain/security/` | ✅ |
| ADR-008 | Dependency Injection | `src/dependencies.py` | ⚠️ Partial |
| ADR-009 | Neo4j Graph Integration | `src/services/neo4j_service.py` | ✅ |
| ADR-010 | AI/LLM Integration | `src/ai/`, `src/services/ai_assistant_service.py` | ✅ |
| ADR-011 | Background Tasks (removed Celery) | In-process via anyio | ✅ |
| ADR-012 | Stratus File Storage | `src/repositories/storage.py` | ⚠️ Stub |
| ADR-013 | Prometheus Metrics | `src/main.py` (conditional) | ✅ |
| ADR-014 | CORS + Security Middleware | `src/middleware/` | ✅ |
| ADR-015 | React + TypeScript Frontend | `apps/web/` | ✅ |

---

## 2. Requirements to Test Mapping

| Requirement | Test File | Test Count | Status |
|---|---|---|---|
| Auth (register/login/logout) | `tests/api/test_auth_api.py` | 7 | ✅ |
| FIR CRUD | `tests/api/test_fir_api.py` | 8 | ✅ |
| Health/Readiness | `tests/smoke/test_bootstrap.py` | 8 | ✅ |
| API Status | `tests/unit/test_app.py` | 3 | ✅ |
| Database Schema | `tests/database/test_schema.py` | 1 | ✅ |
| Alembic Migrations | `tests/smoke/test_alembic_migrations.py` | 7 | ✅ (6 pass) |
| AI Providers | `tests/unit/test_ai.py` | 32 | ✅ |
| ML Pipeline | `tests/unit/test_ml.py` | 27 | ✅ |
| Pipelines | `tests/unit/test_pipelines.py` | 20 | ✅ |
| Services | `tests/unit/test_services.py` | 6 | ✅ |
| End-to-End | `tests/end-to-end/test_user_journey.py` | 1 | ⏸️ (blocked) |

---

## 3. File Coverage

| Layer | Files | Tested | Coverage |
|---|---|---|---|
| Routers (src/routers/) | 10 | 10 | 100% route registration |
| Services (src/services/) | 15 | 12 | 80% |
| Models (src/models/) | 9 | 5 | 55% |
| AI (src/ai/) | 12 | 12 | 100% |
| ML (src/ml/) | 7 | 7 | 100% |
| Schemas (src/schemas/) | 12 | 10 | 83% |

---

## 4. Known Gaps

| Gap | ADR | Status | Action Required |
|---|---|---|---|
| Repository DI not wired | ADR-004, ADR-008 | Open | Refactor routers to use `get_fir_repo` |
| Catalyst AI provider stubbed | ADR-010 | Open | Implement Zia SDK integration |
| Stratus file storage not bound | ADR-012 | Open | Wire into FIR evidence upload |
| Phase 2 defects unresolved | Various | Open | 14 defects remain from P2 audit |
