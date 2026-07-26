# Phase 3 Correction Plan — Project Berunda

> **Document ID:** BERUNDA-VERIF3-CORRECT-001 | **Version:** 1.0 | **Status:** ACTIVE  
> **Classification:** INTERNAL | **Owner:** Engineering Lead & Verification Team  
> **Date:** 2026-07-26  

---

## 1. Executive Summary

This Correction Plan defines the mandatory remediation roadmap required to resolve the 7 open defects identified during the Phase 3 Independent Verification Audit (`BERUNDA-VERIF3-001`). 

### Mandatory Governance Gate Rule
**No new Phase 4 feature development (e.g., advanced predictive ML models, Neo4j graph algorithms, or multi-jurisdictional analytics) may commence until all BLOCKER and CRITICAL defects defined in this plan are verified as resolved and closed.**

---

## 2. Remediation Roadmap & Action Items

### 2.1 Blocker Defect Remediation

#### [ACT-01] Refactor Routers & Services to Inject Repository Abstraction
- **Defect Reference**: **P3V-BLK-001** (Repository Pattern Bypassed)
- **Owner Workstream**: Workstream C (Backend Core)
- **Target Files**: 
  - `src/routers/*.py` (`fir_router.py`, `auth_router.py`, `entity_router.py`, etc.)
  - `src/services/*.py` (`fir_service.py`, `auth_service.py`, etc.)
- **Exact Modification Required**:
  1. In all route handlers in `src/routers/`, replace `session: AsyncSession = Depends(get_session)` with `repo: FIRRepository = Depends(get_fir_repo)`.
  2. Update `FIRService` and domain service constructors to receive the repository interface (`self.repo: FIRRepository`) instead of raw SQLAlchemy sessions.
  3. Replace raw SQLAlchemy ORM calls in services (e.g., `self.session.execute(select(CaseMaster))`) with interface method invocations (`await self.repo.get_by_id(case_id)`).
- **Verification Criterion**: 
  - `grep_search` across `src/routers/` for `AsyncSession` or `get_session` returns zero matches.
  - Automated integration tests pass when running against `SQLiteFIRRepository` in CI.

#### [ACT-02] Re-implement Catalyst AI Provider with Zoho Zia SDK
- **Defect Reference**: **P3V-BLK-002** (Broken AI Provider Endpoint)
- **Owner Workstream**: Workstream D (AI & ML Pipeline)
- **Target File**: `src/ai/providers/catalyst.py`
- **Exact Modification Required**:
  1. Remove hardcoded HTTP POST invocations targeting `/functions/llm-chat/execute`.
  2. Import and initialize the official Zoho SDK (`import zcatalyst_sdk`).
  3. Implement `complete()` and `stream()` methods using `zcatalyst_sdk.zia().get_ml_service()` or an authenticated Catalyst AppSail SDK binding.
- **Verification Criterion**: 
  - Executing an AI extraction request with `AI_PROVIDER=catalyst` against a live Zoho Catalyst sandbox returns valid, schema-compliant JSON without 404/500 errors.

---

### 2.2 Critical Defect Remediation

#### [ACT-03] Complete Phase 3 Implementation Reports & Verify Test Suite
- **Defect Reference**: **P3V-CRT-001** (Missing Reports 07-10 & Unverified Test Claims)
- **Owner Workstream**: Workstream A (Architecture & Governance)
- **Target Directory**: `docs/implementation/phase-03/`
- **Exact Modification Required**:
  1. Author and commit `07-TESTING-AND-SECURITY-REPORT.md`, documenting unit, integration, and security test coverage.
  2. Author and commit `08-CI-AND-CATALYST-DEPLOYMENT-REPORT.md`, detailing AppSail container configuration and environment variable mappings.
  3. Author and commit `09-IMPLEMENTATION-TRACEABILITY-MATRIX.md`, mapping Phase 2 ADRs to Phase 3 files.
  4. Author and commit `10-PHASE-3-COMPLETION-REPORT.md`, providing final sign-off.
  5. Execute `pytest` across the test suite in an environment with compiled wheels and embed the terminal execution log.
- **Verification Criterion**: 
  - All 10 Phase 3 implementation reports exist in repository history and contain verified execution transcripts.

---

### 2.3 Major Defect Remediation

#### [ACT-04] Bind FIR Document Uploads to Stratus Storage Abstraction
- **Defect Reference**: **P3V-MAJ-001** (Stratus Storage Unintegrated)
- **Owner Workstream**: Workstream C (Backend Core)
- **Target Files**: `src/services/fir_service.py`, `src/routers/fir_router.py`
- **Exact Modification Required**:
  1. Inject `FileStorage` adapter into `FIRService` constructor via `src/dependencies.py`.
  2. In document upload endpoints, stream incoming multipart file bytes to `await self.storage.save_file(...)` and store the returned bucket URI in `src_EvidenceMaster.FileURI`.
- **Verification Criterion**: 
  - Uploading a sample FIR document via `POST /api/v1/fir/{id}/evidence` successfully creates an entry in `src_EvidenceMaster` and writes file contents to the configured Stratus storage bucket.

---

### 2.4 Minor & Observation Remediation

#### [ACT-05] Consolidate Alembic Migration Revision Numbering
- **Defect Reference**: **P3V-MIN-001**
- **Owner Workstream**: Workstream C (Database & Storage)
- **Target Directory**: `src/alembic/versions/`
- **Exact Modification Required**:
  1. Rename `edce56cd43ea_phase3_p0_tables.py` to `007_phase3_p0_tables.py` and update its `down_revision` pointer to `"006"`.
  2. Merge or archive redundant hash migrations to ensure a clean, linear numbering sequence (`001` through `007`).
- **Verification Criterion**: 
  - Executing `alembic history` outputs a linear, unbroken migration chain from base to head.

#### [ACT-06] Add Root Task Runner / Makefile
- **Defect Reference**: **P3V-OBS-002**
- **Owner Workstream**: Workstream A (DevSecOps)
- **Target File**: `Makefile` (Root Workspace)
- **Exact Modification Required**:
  1. Create a root `Makefile` defining `test`, `lint`, `build-web`, and `run-dev` targets that automatically invoke the correct virtual environment binaries.
- **Verification Criterion**: 
  - Running `make test` from workspace root executes backend pytest and frontend build without path errors.

---

## 3. Phase 4 Eligibility & Re-Audit Criteria

Upon completion of Action Items **ACT-01**, **ACT-02**, and **ACT-03**, the Engineering Lead will request a formal Re-Audit. Once independent verification confirms zero open Blocker or Critical defects, Phase 3 will transition from **FAIL** to **PASS**, authorizing the commencement of Phase 4 workstreams.
