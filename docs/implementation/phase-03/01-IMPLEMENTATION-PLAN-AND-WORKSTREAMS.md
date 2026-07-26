# 01 — Implementation Plan and Workstreams

**Document ID:** BERUNDA-IMPL3-PLAN-001
**Version:** 1.0 | **Status:** FINAL
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

## 1. Objective
Define the parallelizable workstreams and sequential order of operations to implement the Phase 3 MVP vertical slice safely, reliably, and strictly within the approved Phase 2 architecture boundaries.

## 2. Dependency Graph

```text
Configuration foundation (Workstream A)
        |
        +---- Database and storage (Workstream B)
        |
        +---- Backend foundation (Workstream C)
        |
        +---- Frontend foundation (Workstream D)
        |
        +---- AI prototype (Workstream E)
                    |
                    v
           Core vertical slice
                    |
                    v
          Integration and quality gate (Workstream F)
```

## 3. Workstreams

### Workstream A — Platform and Configuration
* **Environment configuration**: Creation of secure `.env.example` templates and Catalyst-ready variables.
* **Secret handling**: Refinement of `.gitignore` and centralized pydantic configuration handling.
* **Local development**: Tooling via `Makefile` (commands: `install`, `dev-backend`, `test`, `lint`, `seed`).
* **Logging**: Application-level JSON logging format for backend routers (no PII leak).
* **Dependency management**: Locked `requirements.txt` for backend, `package.json` for frontend.

### Workstream B — Database and Storage
* **Catalyst Data Store schema**: Alignment of `src/models` with Phase 2 definitions (e.g. `int_AIExtractionQueue`, `int_ERMergeCandidate`).
* **Migrations**: Generation of Alembic migration scripts bridging current schema state to Phase 2 end-state.
* **Indexes & Constraints**: Adding unique constraints on `CrimeNo` and jurisdiction boundaries (`DistrictID`).
* **Stratus storage**: Setup mock directories (`data/uploads`) supporting Catalyst Stratus file upload APIs.
* **Seed data & Reset**: Idempotent Python scripts enforcing `DataSource=SYNTHETIC` logic.

### Workstream C — Backend
* **FastAPI application foundation**: Refine core `src/main.py` router structure.
* **Authentication/Authorization integration**: Enforce JWT and Role-Based Access Controls across routes.
* **FIR APIs**: Implement `fir_service` (CRUD logic, jurisdiction filtering).
* **Audit logging**: `gov_AuditLog` event creation hook integration.

### Workstream D — Frontend
* **Application shell**: Setup `react-router-dom` definitions based on Phase 2 routing constraints.
* **Authentication screens**: Integration of login, context handling, and role-based protective routes.
* **Dashboard shell & FIR Forms**: Integration with backend APIs.
* **FIR review UI**: AI suggestions and queue management interface.

### Workstream E — AI and Data
* **AI extraction contract**: Implement the interface between spaCy NER models and the extraction queue.
* **Processing pipeline**: FastAPI background tasks triggering on FIR creation.
* **Human-review flow**: Service layer implementations handling `APPROVE`, `REJECT`, `EDIT`.
* **Mock Provider**: Integration of LLM fallback for safe demo operations.

### Workstream F — QA and Integration
* **Contract tests**: Validating FastAPI outputs against `docs/api/openapi.yaml`.
* **Integration & E2E tests**: Seed data validations and role-boundary verifications.
* **CI quality gates**: Local checks before Catalyst deployment.

## 4. Required Implementation Sequence

1. **Repository cleanup and dependency verification** (Workstream A).
2. **Environment templates and configuration validation** (Workstream A).
3. **Database and storage setup** (Workstream B).
4. **Backend application foundation** (Workstream C).
5. **Frontend application foundation** (Workstream D).
6. **Authentication and authorization** (Workstream C & D).
7. **Core FIR CRUD** (Workstream C & D).
8. **File upload** (Workstream C & B).
9. **AI extraction prototype** (Workstream E).
10. **Human-review workflow** (Workstream D & E).
11. **End-to-end integration** (All).
12. **Tests and CI** (Workstream F).
13. **Catalyst development deployment** (Workstream A).
14. **Final Phase 3 audit** (Workstream F).
