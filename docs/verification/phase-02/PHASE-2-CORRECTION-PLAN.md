# Phase 2 Correction Plan

**Document ID:** BERUNDA-VER-P2-005
**Version:** 2.0 | **Status:** FINAL
**Date:** 2026-07-26

---

## 1. Recommended Approach: Phase 2.5 Remediation Sprint

Phase 2 verification has identified **24 blocking defects** (4 BLOCKER, 10 CRITICAL, 10 MAJOR) that must be resolved before Phase 3 work begins. Rather than incrementally fixing while adding new features, we recommend a **dedicated 2-week remediation sprint** focused solely on closing all BLOCKER and CRITICAL defects.

**Rationale:** Attempting to implement Phase 3 features on the current codebase would compound technical debt and risk cascading failures. The 4 blockers and 10 critical defects represent foundational architecture issues that impact every subsequent feature.

---

## 2. Sprint Structure

| Sprint | Duration | Focus | Defects |
|--------|----------|-------|---------|
| Sprint 0 | Days 1-2 | Prerequisites | ADR-012 (BLK-001), CatalystProvider (BLK-003), Test fixes (CRT-010) |
| Sprint 1 | Days 3-5 | Data Layer | P0 tables (BLK-004 + CRT-004/005/006/007), CaseMaster fields (MAJ-009), Caste FKs (MAJ-008) |
| Sprint 2 | Days 6-8 | Auth & Security | Role migration (BLK-002), Jurisdiction filter (MAJ-006), Refresh token (MAJ-010), Audit wiring (MAJ-005) |
| Sprint 3 | Days 9-11 | Backend Core | Repository pattern (CRT-001), Admin router (CRT-009), Orphan cleanup (CRT-008), Phase2 duplicate (MAJ-002) |
| Sprint 4 | Days 12-14 | AI & Cleanup | ER algorithm (CRT-003), Neo4j removal (CRT-002), Mock provider (MAJ-001), NER pipeline (MAJ-012), Stratus upload (MAJ-011), Env register (MAJ-004), CrimeNo (MAJ-013), OpenAPI lint (MAJ-007) |

---

## 3. Defect Resolution Plan

### 3.1 BLOCKER Defects (Must fix before any Phase 3 work)

| ID | Defect | Resolution Steps | Effort | Dependencies |
|----|--------|-----------------|--------|-------------|
| BLK-001 | ADR-012 not written | 1. Document AppSail deployment strategy as ADR-012 covering: FastAPI-on-AppSail rationale, Catalyst Functions vs AppSail choice, port mapping, health check configuration, environment variable injection, Stratus integration, and CI/CD pipeline | 0.5 day | None |
| BLK-002 | Wrong role model (3 roles vs 4) | 1. Create Alembic migration: alter `auth_User.role` to use enum with INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, ADMIN 2. Add data migration for existing users (admin->ADMIN, analyst->SCRB_ANALYST, officer->INVESTIGATOR) 3. Update `auth_models.py` Role enum 4. Update `middleware/auth.py` role checks 5. Update `phase2_backend/authorization.py` to use new role names 6. Update all router/endpoint role decorators 7. Update OpenAPI UserRole schema | 2 days | None |
| BLK-003 | CatalystProvider broken | 1. Option A (preferred): Re-implement using Zia SDK (`zcatalyst_zia`) for LLM calls 2. Option B: Create actual Catalyst Function at `/functions/llm-chat/execute` 3. Update `catalyst.py` to use real endpoint 4. Add error handling + fallback to MockProvider 5. Update env var register to reflect actual provider config | 2 days | None |
| BLK-004 | 4 P0 tables missing | 1. Create `int_AIExtractionQueue` in `int_models.py` (CaseID, ExtractedData JSON, Status, CreatedAt, ReviewedBy FK, ReviewedAt) 2. Create `int_ERMergeCandidate` in `int_models.py` (Entity1ID, Entity2ID, Score, Status, ReviewedBy FK, DecidedAt) 3. Create `src_EvidenceMaster` in `src_models.py` (EvidenceID, CaseID FK, FileName, FileHash, FileSize, MimeType, StoragePath, UploadedBy FK, UploadedAt) 4. Create `int_FIRProcessingState` in `int_models.py` (CaseID FK, CurrentStatus, ValidTransitions JSON, UpdatedBy FK, UpdatedAt) 5. Create Pydantic schemas in `src/schemas/extraction_schemas.py` and `merge_schemas.py` 6. Create Alembic migrations 7-10 7. Add audit events for each table | 2 days | None |

### 3.2 CRITICAL Defects (Must fix before Phase 3 — high impact)

| ID | Defect | Resolution Steps | Effort | Dependencies |
|----|--------|-----------------|--------|-------------|
| CRT-001 | No repository pattern | 1. Create `src/repositories/base.py` with async CRUD base class 2. Create `src/repositories/fir_repository.py`, `person_repository.py`, `entity_repository.py` 3. Create `src/dependencies.py` with dependency injection for repositories 4. One-by-one, refactor each router to use Repository DI 5. Remove direct `AsyncSession`/`get_session` imports from all routers 6. Verify no `AsyncSession` references remain in router files | 4 days | None |
| CRT-002 | Neo4j contradicts ADR-004 | 1. Remove `src/services/neo4j_service.py` 2. Migrate any needed graph operations to NetworkX in `src/services/graph_service.py` 3. Ensure all graph endpoints use PostgreSQL + NetworkX per ADR-004 4. Remove Neo4j references from env var register | 1 day | None |
| CRT-003 | ER uses wrong algorithm | 1. Create `src/ml/entity_resolution.py` with: Soundex-based name blocking, weighted scoring (name 0.4, DOB 0.3, address 0.2, crime_head 0.1), configurable threshold 2. Remove `learned_entity_resolution_service.py` 3. Update entity resolution route to use new service 4. Add unit tests for blocking + scoring | 2 days | BLK-004 (int_ERMergeCandidate table) |
| CRT-004 | int_AIExtractionQueue missing | Same as BLK-004 step 1 | Included in BLK-004 | BLK-004 |
| CRT-005 | int_ERMergeCandidate missing | Same as BLK-004 step 2 | Included in BLK-004 | BLK-004 |
| CRT-006 | src_EvidenceMaster missing | Same as BLK-004 step 3 | Included in BLK-004 | BLK-004 |
| CRT-007 | int_FIRProcessingState missing | Same as BLK-004 step 4 | Included in BLK-004 | BLK-004 |
| CRT-008 | Orphan routers + missing admin | 1. Remove `offender_router.py` (archive to `archive/` if needed) 2. Remove `socioeconomic_router.py` 3. Remove `ai_assistant_router.py` 4. Remove `ingestion_router.py` 5. Remove `notification_router.py` 6. Create `admin_router.py` with: GET /admin/users, POST /admin/users, PATCH /admin/users/{id}/role, POST /admin/users/{id}/deactivate | 2 days | BLK-002 (role model) |
| CRT-009 | admin_router missing | Same as CRT-008 step 6 | Included in CRT-008 | BLK-002 |
| CRT-010 | Pytest failures | 1. Diagnose FileNotFoundError in integration tests 2. Fix endpoint health check responses 3. Fix Alembic revision count assertions 4. Ensure all tests pass | 2 days | All code fixes above |

### 3.3 MAJOR Defects (Should fix before Phase 3)

| ID | Defect | Resolution Steps | Effort | Dependencies |
|----|--------|-----------------|--------|-------------|
| MAJ-001 | Mock provider missing | 1. Create `src/ai/providers/mock_provider.py` with 3 pre-scripted demo responses: entity extraction, risk score, RAG answer 2. Register in provider_registry.py 3. Add auto-fallback in case real providers fail | 0.5 day | None |
| MAJ-002 | phase2_backend duplicate | 1. Merge `authorization.py` into `src/middleware/auth.py` 2. Merge `repositories.py` if non-duplicative 3. Merge `domain.py` if non-duplicative 4. Remove `src/phase2_backend/` directory | 1 day | CRT-001 |
| MAJ-003 | Socioeconomic frontend orphan | 1. Remove `apps/web/src/features/socioeconomic/` 2. Remove navigation references 3. Verify no imports break | 0.5 day | None |
| MAJ-004 | Env var register stale | 1. Remove CELERY_BROKER_URL, CELERY_RESULT_BACKEND entries 2. Remove NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD entries 3. Update token expiry to 15min/24h to match Phase 2 design 4. Add CATALYST_* entries for actual deployment | 0.5 day | None |
| MAJ-005 | Audit not wired | 1. Add `audit_service.log_event()` calls in: auth_service (login/logout), fir_service (CRUD), entity_service (merge decisions), AI provider (extraction/analysis) 2. Verify gov_AuditLog stores all required events 3. Add audit event types for AI actions (missing per doc 00) | 1 day | None |
| MAJ-006 | Jurisdiction filter incomplete | 1. Add district_id filter to entity_service list queries 2. Add district_id filter to graph_service entity queries 3. Add district_id filter to rag_service context retrieval 4. Add district_id filter to analytics/hotspot/anomaly queries | 1 day | None |
| MAJ-007 | OpenAPI not linted | 1. Install `@redocly/cli` or `prance` 2. Run lint: `npx @redocly/cli lint docs/api/openapi.yaml` 3. Fix all reported errors/warnings 4. Add lint step to CI pipeline | 0.5 day | None |
| MAJ-008 | Caste/Religion FKs missing | 1. Add `CasteRef` FK to `src_Accused` in `src_models.py` (nullable->src_CasteMaster) 2. Add `ReligionRef` FK to `src_Accused` (nullable->src_ReligionMaster) 3. Create Alembic migration 4. Update Pydantic schemas to exclude from non-COMPLIANCE responses | 0.5 day | BLK-002 (COMPLIANCE role) |
| MAJ-009 | CaseMaster missing fields | 1. Add `Status` String column to `src_CaseMaster` (values: Draft/Registered/UnderInvestigation/Closed/Archived) 2. Add `CreatedBy` FK to `auth_User.UserID` 3. Add `CreatedAt` DateTime with server_default 4. Add `UpdatedAt` DateTime with onupdate 5. Create Alembic migration | 0.5 day | None |
| MAJ-010 | Refresh token single-use | 1. In `auth_service.refresh_token()`: mark old refresh token as revoked 2. Issue new refresh token 3. Verify old refresh token cannot be reused 4. Add audit event for token reuse attempt | 0.5 day | None |
| MAJ-011 | Stratus upload not integrated | 1. Install Catalyst Stratus SDK 2. Implement `upload_to_stratus()` in `fir_service.py` 3. Create `src_EvidenceMaster` table (see BLK-004) 4. Update `POST /firs/{fir_id}/documents` to store file 5. Add file type/size validation | 1 day | BLK-004 (EvidenceMaster table) |
| MAJ-012 | NER pipeline scaffold | 1. Download spaCy `en_core_web_md` model 2. Implement full pipeline: text cleaning, sentence segmentation, NER with crime-specific entity types 3. Wire into extraction endpoint 4. Add unit tests | 1 day | BLK-004 (int_AIExtractionQueue) |
| MAJ-013 | CrimeNo generation | 1. Implement sequence-based CrimeNo: `YYYY/CRIME/{district_code}/{5-digit-seq}` 2. Add sequence table or use DB sequence 3. Wire into FIR creation endpoint 4. Update OpenAPI CrimeNo format validation | 0.5 day | None |
| MAJ-014 | Open Catalyst questions | 1. Compile ARCH-OQ-001 to 005 into single document 2. Submit to Catalyst platform team 3. Document answers and any architecture changes required 4. Update affected ADRs if answers change decisions | 0.5 day | None |

### 3.4 MINOR Defects (Fix when convenient)

| ID | Defect | Resolution Steps | Effort | Dependencies |
|----|--------|-----------------|--------|-------------|
| MIN-001 | `/firs` path naming | Evaluate rename to `/firs`; update OpenAPI and docs | 0.25 day | None |
| MIN-002 | JWT key rotation | Document rotation procedure in security docs | 0.25 day | None |
| MIN-003 | E2E manual only | Add Playwright if time permits | 1 day | None |
| MIN-004 | catalyst_config.json ref | Update doc to reference catalyst.json | 0.1 day | None |
| MIN-005 | ERD notation | Consider IE notation for consistency | 0.25 day | None |
| MIN-006 | Health endpoint mismatch | Align OpenAPI with doc 09 (204 vs 200) | 0.1 day | None |
| MIN-007 | Stratus placeholder URLs | Replace with actual project IDs | 0.1 day | MAJ-011 |
| MIN-008 | Path template inconsistency | Standardize `{fir_id}` vs `{id}` across docs | 0.25 day | None |

---

## 4. Effort Summary

| T-Shirt Size | Person-Days | Defects |
|-------------|-------------|---------|
| Small (< 0.5 day) | ~5 | 2 BLOCKER components + 8 MAJOR sub-items + all MINOR |
| Medium (0.5-1 day) | ~8 | 2 BLOCKER sub-items, CRT-002/008/009, MAJ-002/005/006/011/012 |
| Large (2-4 days) | ~10 | BLK-002/003/004, CRT-001/003/010 |
| **Total** | **~23 person-days** | **36 defects** |

---

## 5. Go/No-Go Gates

### Gate 1: Pre-Sprint Checks (Day 0)

- [ ] All team members agree on sprint scope
- [ ] Phase 2 architecture docs are final and approved
- [ ] 5 open Catalyst questions submitted to platform team

### Gate 2: Sprint Complete (Day 14)

- [ ] All 4 BLOCKER defects: RESOLVED
- [ ] All 10 CRITICAL defects: RESOLVED
- [ ] All 14 MAJOR defects: RESOLVED
- [ ] Pytest suite: PASS
- [ ] OpenAPI lint: PASS
- [ ] Role model: 4 roles enforced in code + DB
- [ ] All P0 tables: exist in DB with migrations
- [ ] Repository pattern: all 15 routers use DI
- [ ] Entity resolution: rule-based per ADR-005
- [ ] Mock provider: exists and tested
- [ ] Catalyst staging deploy: HEALTHY

### Gate 3: Phase 3 Entry (After Sprint)

- [ ] All 10 Go/No-Go criteria from Readiness Matrix: SATISFIED
- [ ] Phase 3 architecture work may commence

---

## 6. Risk Register for Sprint

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Catalyst platform answers contradict assumptions | Medium | High | Submit questions early (Gate 1); have FastAPI fallback ready |
| Role migration breaks existing auth | Medium | High | Rollback migration script; test on staging first |
| Repository refactor introduces regressions | High | High | Refactor one router at a time; run tests after each |
| Catalyst platform availability | Low | High | Develop and test locally; deploy when platform available |
| Sprint takes longer than 2 weeks | Medium | Medium | Prioritize BLOCKER + CRITICAL; defer MAJOR if needed |

---

## 7. Post-Sprint Handoff

After the 2-week remediation sprint, the team should have:

1. **Clean architecture**: Repository pattern in use, no dead code, no ADR violations
2. **Correct auth**: 4 roles, jurisdiction-filtered, audited
3. **Complete data layer**: All P0 tables, migrations, schemas
4. **Working AI**: Rule-based ER, proper NER, mock provider, functioning RAG
5. **Deployable**: Catalyst integration working, ADR-012 documented, staging live
6. **Testable**: Passing pytest suite, linted OpenAPI, CI pipeline

Only then should Phase 3 (event-driven mesh, circuits, CQRS) begin.

*End of PHASE-2-CORRECTION-PLAN.md*
