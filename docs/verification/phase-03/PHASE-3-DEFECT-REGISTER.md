# Phase 3 Defect Register — Project Berunda

> **Document ID:** BERUNDA-VERIF3-DEFECTS-001 | **Version:** 1.0 | **Status:** FINAL  
> **Classification:** INTERNAL | **Owner:** Independent Verification Team  
> **Date:** 2026-07-26  

---

## 1. Summary of Defects

| Severity | Count | Open | In Progress | Resolved / Closed |
|---|---|---|---|---|
| **BLOCKER** | 2 | 2 | 0 | 0 |
| **CRITICAL** | 1 | 1 | 0 | 0 |
| **MAJOR** | 1 | 1 | 0 | 0 |
| **MINOR** | 1 | 1 | 0 | 0 |
| **OBSERVATION** | 2 | 2 | 0 | 0 |
| **TOTAL** | **7** | **7** | **0** | **0** |

---

## 2. Blocker Defects

### [P3V-BLK-001] Architectural Contradiction: Repository Pattern Bypassed in FastAPI Routers & Services
- **Status**: OPEN
- **Category**: Backend Architecture / Data Access
- **Target File / Component**: `src/routers/fir_router.py` (line 74), `src/routers/auth_router.py`, `src/routers/entity_router.py`, `src/services/fir_service.py` (line 19).
- **Description**: Authoritative Phase 2 Architecture (ADR-004 and ADR-008) mandates that all data access occur through the Repository Pattern (`FIRRepository` interface, injected via `src/dependencies.py` -> `get_fir_repo`). This decoupling is required to switch dynamically between local SQLite development and Zoho Catalyst Data Store (ZCQL) in production. However, all active FastAPI route handlers and business services directly import SQLAlchemy ORM (`AsyncSession`, `select(CaseMaster)`, `session.execute`), completely bypassing `src/repositories/` and `src/dependencies.py`.
- **Evidence**: Static inspection and `grep_search` across `src/` confirm that `get_fir_repo` and `get_auth_repo` are never imported or invoked in any router or service file.
- **Impact**: Blocks deployment to Zoho Catalyst Data Store. Violates mandatory architecture governance; code cannot run in the production hackathon environment.
- **Required Remediation**: Refactor all route handlers in `src/routers/` and service constructors in `src/services/` to accept `repo: FIRRepository = Depends(get_fir_repo)` instead of raw SQLAlchemy `AsyncSession` instances.

---

### [P3V-BLK-002] Broken AI Provider Integration: Non-existent Catalyst QuickML/Zia Endpoint
- **Status**: OPEN
- **Category**: AI Foundation / External Integration
- **Target File / Component**: `src/ai/providers/catalyst.py` (lines 70, 135, 155).
- **Description**: The `CatalystProvider` AI adapter executes HTTP POST requests against `/functions/llm-chat/execute` and `/functions/llm-embed/execute`. These paths represent arbitrary, non-existent endpoints that do not correspond to any Zoho Catalyst AppSail function, Zoho QuickML API, or Zia AI SDK in this codebase or Zoho's official documentation.
- **Evidence**: Inspection of `src/ai/providers/catalyst.py` reveals hardcoded REST paths to `/functions/llm-chat/execute` without an accompanying backend serverless function or Zoho Zia SDK binding.
- **Impact**: When `AI_PROVIDER=catalyst` is configured in production, all AI FIR extraction, entity resolution suggestions, and RAG embeddings fail with HTTP 404/500 errors.
- **Required Remediation**: Re-implement `CatalystProvider` using the official Python SDK (`zcatalyst-sdk`) to invoke verified Zoho Zia or QuickML model endpoints, or deploy an authenticated intermediary Catalyst Serverless Function.

---

## 3. Critical Defects

### [P3V-CRT-001] Missing Mandatory Phase 3 Implementation Reports & Unverified Test Blockers
- **Status**: OPEN
- **Category**: Documentation & Governance
- **Target File / Component**: `docs/implementation/phase-03/`.
- **Description**: Governance rules require a 10-report suite for Phase 3 completion. While reports 00 through 06 exist, reports 07 (`TESTING-AND-SECURITY-REPORT.md`), 08 (`CI-AND-CATALYST-DEPLOYMENT-REPORT.md`), 09 (`IMPLEMENTATION-TRACEABILITY-MATRIX.md`), and 10 (`PHASE-3-COMPLETION-REPORT.md`) are missing from the repository. Furthermore, reports 04 and 06 assert that pytest execution was impossible due to Windows lacking C++ build tools for `numpy`/`spacy`, but independent verification confirmed standard pre-compiled binary wheels are readily available and installable.
- **Evidence**: `list_dir` on `docs/implementation/phase-03/` shows only 7 files (00 to 06).
- **Impact**: Leaves verification claims unsubstantiated, breaking traceability and audit readiness.
- **Required Remediation**: Author and commit reports 07, 08, 09, and 10, populated with genuine test logs and runtime execution evidence.

---

## 4. Major Defects

### [P3V-MAJ-001] FIR Service Document Handling Bypasses Stratus Storage Abstraction
- **Status**: OPEN
- **Category**: Storage / FIR Ingestion
- **Target File / Component**: `src/services/fir_service.py`, `src/routers/fir_router.py`.
- **Description**: Although `StratusFileStorage` and `LocalFileStorage` adapters are cleanly implemented in `src/repositories/`, the core FIR creation and file ingestion workflows do not utilize them to persist scanned FIR documents or evidence records (`src_EvidenceMaster`).
- **Evidence**: Explicit acknowledgment in `04-BACKEND-FOUNDATION-REPORT.md` (Section 8): "Remaining: Bind the `src_EvidenceMaster` file upload handling explicitly to the Stratus adapter."
- **Impact**: File uploads remain in an unintegrated or mocked state, preventing document persistence in Zoho Catalyst Stratus buckets.
- **Required Remediation**: Integrate `StratusFileStorage` (via dependency injection) into `FIRService.create_fir` and evidence attachment endpoints.

---

## 5. Minor Defects

### [P3V-MIN-001] Mixed Alembic Revision Numbering Conventions
- **Status**: OPEN
- **Category**: Database Migrations
- **Target File / Component**: `src/alembic/versions/`.
- **Description**: The migration scripts mix sequential numbering (`001_initial_schema.py` through `006_seed_users.py`) with unnumbered git-hash prefixes (`edce56cd43ea_phase3_p0_tables.py`, `ffff29081afe_phase2_initial_schema.py`).
- **Evidence**: Directory inspection of `src/alembic/versions/`.
- **Impact**: Can cause revision tree divergence or confusion during automated CI/CD database provisioning.
- **Required Remediation**: Renumber hash migrations to follow the sequential numbering scheme and verify clean `down_revision` pointers.

---

## 6. Observations & Technical Debt

### [P3V-OBS-001] Reliance on In-Memory/SQLite Vector Similarity in Development
- **Status**: OPEN
- **Category**: RAG / Retrieval
- **Target File / Component**: `src/ai/retrieval/vector_stores.py`.
- **Description**: Local development relies on numpy/scikit-learn cosine similarity over in-memory arrays or SQLite, which does not validate the production ZCQL/pgvector query syntax required by Catalyst.
- **Remediation**: Provide an automated test harness that validates ZCQL vector search syntax against a mock Catalyst Stratus endpoint.

### [P3V-OBS-002] Absence of Centralized Task Runner / Root Makefile
- **Status**: OPEN
- **Category**: DevSecOps / Developer Experience
- **Target File / Component**: Root workspace (`D:\Hack2Skill\Berunda`).
- **Description**: Executing tests, linting, and frontend builds requires manual directory navigation and invocation of os-specific scripts (e.g., `.venv\Scripts\pip`, `npm.cmd`).
- **Remediation**: Add a root-level `package.json`, `Makefile`, or `justfile` with standardized cross-platform targets (`test`, `lint`, `build`, `dev`).
