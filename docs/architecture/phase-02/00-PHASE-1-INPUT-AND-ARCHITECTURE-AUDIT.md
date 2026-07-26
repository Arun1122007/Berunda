# 00 — Phase 1 Input and Architecture Audit

**Document ID:** BERUNDA-ARCH2-AUDIT-001
**Version:** 1.0 | **Status:** APPROVED — Phase 2 architecture baseline
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This document is the mandatory first step of Phase 2.
> No architecture decisions are finalised here.
> All decisions, conflicts, and gaps are recorded and resolved in subsequent Phase 2 documents.

---

## 1. Executive Summary

Phase 1 produced a complete product definition. The repository already contains substantial technical assets: a live FastAPI backend (11 routers, 23 services, 7 model files covering 35+ tables), a scaffolded React 18 + TypeScript frontend (15 feature modules), 11 approved ADRs, and a Catalyst deployment mapping. However four categories of technical gaps must be resolved before implementation can proceed:

1. **Implementation gaps:** Entity resolution (FEAT-022), FIR manual creation endpoint (FEAT-010), AI extraction queue (FEAT-020/021), and document upload (FEAT-011) are not implemented — only scaffolded or partially stubbed.
2. **Role/model mismatch:** Phase 1 finalised 4 roles (INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, ADMIN). Existing code references 3 roles: `admin`, `analyst`, `viewer`. This must be reconciled before any auth middleware is accepted.
3. **Missing tables:** The `int_` intelligence models lack: an AI extraction queue table, an entity resolution merge-candidate queue table, and an FIR document-processing state table. These are required for P0 features FEAT-020, FEAT-021, FEAT-022, and FEAT-023.
4. **Catalyst deployment gap:** Catalyst Functions are scaffolded as placeholder READMEs only. The FastAPI monolith is the actual implementation but is not deployable to Catalyst production without an AppSail wrapper or Node.js bridge.

**Phase 2 entry verdict: CONDITIONAL PROCEED.** Architecture design may proceed immediately. Implementation must be sequenced against the gaps identified in Section 15.

---

## 2. Phase 1 Documents Reviewed

| Document | Path | Status | Used In |
|----------|------|--------|---------|
| 00-CURRENT-STATE-AUDIT.md | `docs/product/phase-01/` | APPROVED | Sections 7, 8, 15 |
| 01-PROBLEM-STATEMENT-AND-VISION.md | `docs/product/phase-01/` | APPROVED | Sections 3, 4, 6 |
| 02-STAKEHOLDERS-AND-USER-ROLES.md | `docs/product/phase-01/` | APPROVED | Sections 6, 12 |
| 03-USER-JOURNEYS-AND-USE-CASES.md | `docs/product/phase-01/` | APPROVED | Sections 6, 10, 11 |
| 04-MVP-SCOPE-AND-PRIORITIZATION.md | `docs/product/phase-01/` | FROZEN | Sections 5, 6, 12, 13 |
| 05-FUNCTIONAL-REQUIREMENTS.md | `docs/product/phase-01/` | APPROVED | Sections 6, 10, 11 |
| 06-NON-FUNCTIONAL-REQUIREMENTS.md | `docs/product/phase-01/` | APPROVED | Sections 6, 11, 12 |
| 07-ACCEPTANCE-CRITERIA.md | `docs/product/phase-01/` | APPROVED | Section 13 |
| 08-DEMO-STORY-AND-SUCCESS-METRICS.md | `docs/product/phase-01/` | APPROVED | Section 16 |
| 09-REQUIREMENTS-TRACEABILITY-MATRIX.md | `docs/product/phase-01/` | APPROVED | Sections 5, 6 |
| 10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md | `docs/product/phase-01/` | ACTIVE | Sections 9, 15 |
| 11-PHASE-1-COMPLETION-REPORT.md | `docs/product/phase-01/` | FINAL | Summary |

---

## 3. Authoritative Requirements Baseline

The following Phase 1 requirements are adopted as the Phase 2 input baseline. No requirement is silently changed here.

### 3.1 Accepted Phase 1 Decisions

| Decision ID | Decision | Source |
|-------------|---------|--------|
| DEC-016 | 4 roles: INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, ADMIN | 02-STAKEHOLDERS |
| DEC-018 | CasteRef/ReligionRef excluded from INVESTIGATOR and SCRB_ANALYST API responses at ORM level | 02-STAKEHOLDERS, ADR-007 |
| DEC-006 | AI suggestions must not be auto-approved; human review gate required for all entity extraction | 05-FR, ADR-006 |
| DEC-013 | All demo data is synthetic; SYNTHETIC label required in all API responses and UI | 06-NFR, AGENTS.md |
| DEC-015 | Audit log is append-only; no UPDATE or DELETE permitted on gov_AuditLog | 06-NFR |

### 3.2 P0 Functional Requirements (selected critical items)

| FR-ID | Requirement Summary | Owner Module |
|-------|-------------------|-------------|
| FR-AUTH-001 | JWT login, HS256, 15min access / 7day refresh | auth |
| FR-AUTH-003 | RBAC — 4 roles — enforced at API layer | auth |
| FR-AUTH-004 | Jurisdiction scoping at ORM query level for INVESTIGATOR | firs, entities, graph, rag |
| FR-AUTH-005 | CasteRef/ReligionRef excluded at ORM SELECT level for non-COMPLIANCE | entities, firs |
| FR-FIR-001 | Manual FIR creation — all required fields — CrimeNo generated | firs |
| FR-FIR-002 | CrimeNo auto-generation — format: DC/SC/YEAR/SEQ — UNIQUE constraint | firs |
| FR-FIR-003 | FIR document upload — PDF/JPEG/PNG ≤ 10 MB — MIME validation — SHA-256 hash | firs, evidence |
| FR-AI-001 | NER extraction from BriefFacts — spaCy English — persons, vehicles, locations | ai |
| FR-AI-003 | Human review/correction/approval of AI extraction — no auto-approve | entities, ai |
| FR-AI-005 | Cross-case entity resolution — rule-based blocking + weighted scoring | entities |
| FR-AI-006 | Merge candidate review — officer approve/reject/defer | entities |
| FR-AI-009 | Relationship graph — Cytoscape.js frontend — NetworkX backend | graph |
| FR-AI-010 | Hidden-link BFS — depth ≤ 5 hops | graph |
| FR-AI-011 | RAG query — jurisdictionally scoped — OpenAI/Groq/Mock | rag |
| FR-AI-014 | Risk scoring — scikit-learn — 4 approved features | risk |
| FR-AI-016 | Fairness check — programmatic — blocks scoring on FAIL | risk, fairness |
| FR-RPT-001 | Geospatial hotspot heatmap — MapLibre GL | analytics |
| FR-RPT-004 | Anomaly detection — z-score — AnomalyAlert table | analytics |
| FR-AUD-001 | Append-only audit log — every sensitive action | audit |
| FR-AUD-002 | Audit log query — COMPLIANCE/ADMIN all; INVESTIGATOR own only | audit |

---

## 4. Authoritative ADR Baseline

All 11 existing ADRs are APPROVED and binding. No ADR may be superseded without a new ADR.

| ADR | Title | Location | Binding Decisions |
|-----|-------|---------|-----------------|
| ADR-001 | Phase 1 Architectural Style | `docs/architecture/ADR/` | Modular Functions + API Gateway; no Kubernetes; no event bus in MVP |
| ADR-002 | Catalyst Deployment Boundaries | `docs/architecture/ADR/` | All services run within Catalyst; no external cloud; Catalyst Auth, Data Store, Stratus, Functions, AppSail, API Gateway |
| ADR-003 | Source of Record vs Intelligence Layer | `docs/architecture/ADR/` | `src_` tables = police record source of truth; `int_` tables = derived intelligence; never update `src_` from AI output |
| ADR-004 | Graph Representation | `docs/architecture/ADR/` | Phase 1 uses relational join tables (`int_RelationshipEdge`); NetworkX in-memory for BFS; Neo4j deferred to Phase 3+ |
| ADR-005 | Entity Resolution Approach | `docs/architecture/ADR/` | Rule-based blocking (Soundex) + weighted scoring; no ML-based auto-merge; human review required for all candidates |
| ADR-006 | RAG and NLQ Safety | `docs/architecture/ADR/` | LLM answers must be grounded in retrieved chunks; answer must include citations; hallucination guardrails active |
| ADR-007 | Sensitive Field Exclusion | `docs/architecture/ADR/` | CasteRef/ReligionRef excluded from INVESTIGATOR/SCRB_ANALYST at ORM query level; COMPLIANCE sees aggregate only |
| ADR-008 | MVP vs Target State | `docs/architecture/ADR/` | MVP uses FastAPI + React; Catalyst Functions are deployment wrappers; Neo4j, Celery, event bus are Phase 3+ |
| ADR-009 | Dual-Language Bootstrap | `docs/architecture/decisions/` | Python FastAPI = primary local dev runtime; Node.js Catalyst Functions = production deployment target |
| ADR-010 | Service-to-AI Separation Contract | `docs/architecture/decisions/` | AI providers accessed only through adapter; services must not directly call LLM providers |
| ADR-011 | Inline Task Execution | `docs/architecture/decisions/` | FastAPI BackgroundTasks for inline async; Celery/Redis deferred to Phase 3+ |

### ADRs Required in Phase 2 (new decisions needed)

| ARCH-DEC-ID | Decision Required |
|-------------|-----------------|
| ARCH-DEC-001 | Finalise demo deployment: FastAPI on AppSail vs Node.js Functions for all 11 routers |
| ARCH-DEC-002 | AI extraction queue: in-memory, Redis, or Data Store table |
| ARCH-DEC-003 | Entity resolution merge queue: Data Store table (int_ERMergeCandidate) |
| ARCH-DEC-004 | Role reconciliation: rename existing 3-role code to 4-role Phase 1 model |
| ARCH-DEC-005 | File upload pipeline: streaming to Stratus vs stage-and-hash |
| ARCH-DEC-006 | RAG corpus indexing: in-memory FAISS vs Catalyst NoSQL vector storage |
| ARCH-DEC-007 | FIR document OCR: Catalyst Zia vs Tesseract (offline) vs skip OCR / text-only extraction |

---

## 5. P0 and P1 Feature Inventory (Technical View)

### Group A — Platform Foundation

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-001 | JWT auth | ✅ `auth_service.py` + `middleware/auth.py` | ✅ `features/auth/` | `auth_User`, `auth_RefreshToken` | Role names mismatch (admin/analyst/viewer vs 4 P1 roles) |
| FEAT-002 | RBAC (4 roles) | ⚠ `require_role()` in middleware — 3 roles only | ⚠ `ProtectedRoute` uses 3 roles | None | **BLOCKER:** 3-role to 4-role migration required |
| FEAT-003 | Jurisdiction scoping | ⚠ `fir_service.py` has `DistrictID` filter — partial | ⚠ Not enforced consistently | `src_District`, `src_Unit` | Must extend to entities, graph, RAG, analytics |
| FEAT-004 | Audit logging | ✅ `audit_service.py` + `gov_models.py` | ✅ `features/audit/` | `gov_AuditLog` | Missing AI events in current service impl |
| FEAT-005 | Session/JWT expiry | ✅ `auth_service.py` — refresh endpoint exists | ✅ | `auth_RefreshToken` | Refresh token single-use not enforced |
| FEAT-006 | Error handling | ✅ `exceptions.py` + global handler in `main.py` | ⚠ Partial | None | Frontend error boundaries incomplete |
| FEAT-007 | Health endpoints | ✅ `/health`, `/ready` in `main.py` | — | None | None |

### Group B — FIR Management

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-010 | Create FIR manually | ⚠ `fir_router.py` + `fir_service.py` — CRUD exists but incomplete field set | ⚠ `features/cases/` scaffold | `src_CaseMaster`, `src_Inv_OccuranceTime` | BriefFacts not mapped; CrimeNo generation not implemented |
| FEAT-011 | Upload FIR document | ⚠ Upload stub in `fir_router.py` — Stratus not integrated | ⚠ `features/ingestion/` scaffold | `src_EvidenceMaster` (MISSING from models) | **BLOCKER:** EvidenceMaster table missing; Stratus integration not done |
| FEAT-012 | CrimeNo auto-generation | ❌ Not implemented — `CrimeNo` field exists but no generation logic | — | `src_CaseMaster` | **BLOCKER:** sequence generation required |
| FEAT-013 | FIR detail (multi-tab) | ⚠ Single GET exists; relations not all loaded | ⚠ Scaffold | Multiple | Relationship loading incomplete |
| FEAT-014 | Global search | ⚠ `entity_router.py` has search; no cross-entity search | ⚠ No cross-entity search UI | Multiple | Cross-entity search service missing |
| FEAT-015 | FIR status lifecycle | ⚠ Status field exists; no transition enforcement | ⚠ No state machine UI | `src_CaseMaster`, `src_CaseStatusMaster` | Status machine not enforced |

### Group C — Entity and AI

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-020 | NER extraction (spaCy) | ⚠ `pipelines/` scaffold — spaCy not loaded in production path | ⚠ No extraction queue UI | **MISSING: extraction queue table** | **BLOCKER:** no AI extraction queue; no extraction result persistence |
| FEAT-021 | Human review/approve | ❌ Not implemented | ❌ | MISSING | **BLOCKER:** requires extraction queue table |
| FEAT-022 | Entity resolution (rule-based) | ⚠ `learned_entity_resolution_service.py` — ML-based stub, not rule-based per ADR-005 | ❌ | `int_PersonEntity`, `int_PersonEntityLink` | **BLOCKER:** algorithm not matching ADR-005 spec; merge candidate queue missing |
| FEAT-023 | Merge review UI | ❌ Not implemented | ❌ | **MISSING: int_ERMergeCandidate** | **BLOCKER** |
| FEAT-024 | PersonEntity profile | ⚠ `entity_router.py` GET /entities/{id} | ⚠ `features/entities/` scaffold | `int_PersonEntity` | Alias list, linked cases not fully assembled |
| FEAT-025 | Vehicle entity (P1) | ⚠ `int_VehicleLink` model exists | ⚠ Scaffold | `int_VehicleLink` | No vehicle-specific router |
| FEAT-026 | Location extraction (P1) | ⚠ Part of NER pipeline | ⚠ | MISSING: no OccurrencePlace location table | Table missing |

### Group D — Graph

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-030 | Relationship graph (Cytoscape.js) | ✅ `graph_service.py` + `graph_router.py` | ✅ `features/graph/` scaffold | `int_RelationshipEdge` | Cytoscape.js integration not verified end-to-end |
| FEAT-031 | Hidden-link BFS | ✅ `graph_analytics_service.py` — NetworkX BFS | ⚠ No UI for BFS trigger | `int_RelationshipEdge` | UI for BFS path selection missing |

### Group E — Analytics

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-040 | Hotspot heatmap | ✅ `hotspot_service.py` + `hotspot_router.py` | ✅ `features/hotspot/` | `int_HotspotLayer` | MapLibre integration not end-to-end verified |
| FEAT-041 | District drill-down | ⚠ Partial in hotspot service | ⚠ | `src_District`, `src_Unit` | Station-level breakdown endpoint missing |
| FEAT-042 | Crime type/date filter | ⚠ Partial | ⚠ | `src_CrimeHead` | Filter params not all wired |
| FEAT-043 | Anomaly detection | ✅ `anomaly_service.py` + `anomaly_router.py` | ✅ `features/anomalies/` | `int_AnomalyAlert` | z-score logic implemented — not end-to-end verified with seed data |

### Group F — AI Assistance

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-050 | RAG query | ✅ `rag_service.py` + `rag_router.py` | ✅ `features/rag/` | `int_RAGCorpusChunk` | Jurisdiction scoping on chunk retrieval not implemented |
| FEAT-054 | RAG citation | ✅ Citation included in rag_service response | ✅ | Same | Verify citation field in response schema |
| FEAT-055 | AI confidence display | ⚠ Confidence stored but not in review UI | ❌ | Extraction queue (MISSING) | Depends on FEAT-020/021 extraction queue |
| FEAT-056 | MockProvider fallback | ✅ `ai/providers/` — MockProvider exists | ✅ Banner scaffold | None | Verify auto-fallback trigger |

### Group G — Risk and Fairness

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-060 | Risk scoring (scikit-learn) | ✅ `risk_service.py` + `risk_router.py` | ✅ `features/risk/` | `int_RiskScore`, `int_RiskScoreFeatureImportance` | Feature list not enforced against approved 4 features |
| FEAT-061 | Feature importance | ✅ `int_RiskScoreFeatureImportance` table | ⚠ | Same | Top-5 display in UI missing |
| FEAT-062 | Fairness check | ✅ `fairness_service.py` | ✅ `features/` | `gov_FairnessCheckResult` (check model) | Fairness check does not halt scoring on FAIL |
| FEAT-063 | Fairness dashboard | ✅ `fairness_router.py` | ⚠ | Same | SCRB_ANALYST read-only not enforced |
| FEAT-064 | Protected-field access control | ⚠ ADR-007 documented; `auth.py` partial | ❌ Not at ORM level | `src_Accused` has no CasteRef/ReligionRef | CasteMaster/ReligionMaster exist in src_; Accused lacks FK — not wired to CasteRef |

### Group H — Governance

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-080 | Audit log view | ✅ `audit_router.py` | ✅ `features/audit/` | `gov_AuditLog` | Own-only filter for INVESTIGATOR not enforced |
| FEAT-081 | User management | ✅ `auth_router.py` — register endpoint | ⚠ `features/admin/` scaffold | `auth_User` | Role assignment, deactivation, unlock not all wired |

### Group I — Infrastructure

| FEAT-ID | Name | Backend Status | Frontend Status | DB Tables | Gap |
|---------|------|---------------|----------------|---------|-----|
| FEAT-090 | Catalyst Functions deployment | ❌ Placeholder READMEs only | — | — | **BLOCKER:** production deployment path not yet valid |
| FEAT-091 | Catalyst Data Store schema | ❌ Schema mapping document exists; not deployed | — | All tables | **BLOCKER:** must deploy to Catalyst project before demo |
| FEAT-092 | Synthetic seed data | ✅ `scripts/data/generate_synthetic.py` | — | All | Planted patterns must be validated against AC-SEED-001 |

---

## 6. Technical Capability Mapping

Full mapping from Phase 1 FR → technical component:

| FR-ID | Backend Module | Frontend Module | DB Entity | AI Component | Catalyst Service | Security Control |
|-------|--------------|----------------|---------|------------|----------------|----------------|
| FR-AUTH-001 | `routers/auth_router.py` + `services/auth_service.py` | `features/auth/LoginPage` | `auth_User`, `auth_RefreshToken` | None | Catalyst Auth (or self-hosted JWT) | NFR-SEC-001, NFR-SEC-003 |
| FR-AUTH-003 | `middleware/auth.py` → `require_role()` | `app/ProtectedRoute` | `auth_User.role` | None | None (app-layer) | ADR-007 |
| FR-AUTH-004 | `services/fir_service.py`, `entity_service.py`, `rag_service.py` | All views | `src_Unit`, `src_District` | None | None | FR-AUTH-004 |
| FR-AUTH-005 | `models/src_models.py` ORM SELECT omission | None | `src_Accused`, `src_Victim`, `src_ComplainantDetails` | None | None | ADR-007, DEC-018 |
| FR-FIR-001 | `routers/fir_router.py` + `services/fir_service.py` | `features/cases/NewFIRForm` | `src_CaseMaster`, `src_Inv_OccuranceTime` | NER trigger | Data Store | FR-AUTH-003 |
| FR-FIR-002 | `services/fir_service.py` — generate_crime_no() | None | `src_CaseMaster.CrimeNo` | None | Data Store UNIQUE constraint | None |
| FR-FIR-003 | `routers/fir_router.py` POST /upload + `services/fir_service.py` | `features/ingestion/UploadPage` | `src_EvidenceMaster` | OCR (Zia or Tesseract) | Stratus | File MIME validation |
| FR-AI-001 | `pipelines/ner_pipeline.py` + `services/entity_service.py` | `features/cases/ExtractionReview` | `int_AIExtractionQueue` (MISSING) | spaCy en_core_web_md | AppSail (Python runtime) | NFR-AI-002 |
| FR-AI-003 | `services/entity_service.py` — approve/reject | `features/entities/MergeReview` | `int_AIExtractionQueue`, `int_PersonEntity` | None | Data Store | NFR-AI-002 |
| FR-AI-005 | `services/entity_service.py` — entity_resolution() | None | `int_ERMergeCandidate` (MISSING) | Soundex + weighted scorer | AppSail | ADR-005 |
| FR-AI-006 | `routers/entity_router.py` + `services/entity_service.py` | `features/entities/MergeReviewPage` | `int_ERMergeCandidate` | None | Data Store | FR-AUTH-004 |
| FR-AI-009 | `services/graph_service.py` | `features/graph/GraphCanvas` | `int_RelationshipEdge` | NetworkX | AppSail | FR-AUTH-004 |
| FR-AI-010 | `services/graph_analytics_service.py` | `features/graph/GraphCanvas` → BFS panel | `int_RelationshipEdge` | NetworkX BFS | AppSail | FR-AUTH-004 |
| FR-AI-011 | `services/rag_service.py` + `routers/rag_router.py` | `features/rag/AskBerunda` | `int_RAGCorpusChunk` | OpenAI/Groq/Mock + embedding | Functions or AppSail | ADR-006, FR-AUTH-004 |
| FR-AI-014 | `services/risk_service.py` + `routers/risk_router.py` | `features/risk/RiskPanel` | `int_RiskScore`, `int_RiskScoreFeatureImportance` | scikit-learn | AppSail | ADR-007 |
| FR-AI-016 | `services/fairness_service.py` | `features/` fairness page | `gov_FairnessCheckResult` | None | Data Store | ADR-007 |
| FR-RPT-001 | `services/hotspot_service.py` + `hotspot_router.py` | `features/hotspot/HotspotMap` | `int_HotspotLayer` | None | Functions | None |
| FR-RPT-004 | `services/anomaly_service.py` + `anomaly_router.py` | `features/anomalies/AlertBadge` | `int_AnomalyAlert` | z-score | Functions | None |
| FR-AUD-001 | `services/audit_service.py` | None (write-only) | `gov_AuditLog` | None | Data Store | NFR-AUT-001 |
| FR-AUD-002 | `routers/audit_router.py` + `services/audit_service.py` | `features/audit/AuditLogPage` | `gov_AuditLog` | None | Data Store | FR-AUTH-003 |

---

## 7. Existing Technical Assets

### 7.1 Backend (`src/`)

| Asset | Type | Completeness | Notes |
|-------|------|-------------|-------|
| `src/main.py` | FastAPI app entry point | ✅ Complete | 11 routers, CORS, health, rate limiting |
| `src/middleware/auth.py` | JWT decode + role check | ⚠ Partial | 3 roles; must add SCRB_ANALYST, COMPLIANCE |
| `src/models/src_models.py` | Source police tables | ✅ Complete | 22 ORM classes — CaseMaster, Accused, Victim, etc. |
| `src/models/int_models.py` | Intelligence tables | ⚠ Partial | Missing: AIExtractionQueue, ERMergeCandidate, EvidenceMaster, OccurrencePlace |
| `src/models/gov_models.py` | Governance tables | ⚠ Partial | AuditLog exists; FairnessCheckResult needs verification |
| `src/models/ai_models.py` | AI suggestion tables | ⚠ Check needed | May overlap with missing extraction queue |
| `src/models/auth_models.py` | Auth tables | ✅ Complete | User + RefreshToken |
| `src/services/fir_service.py` | FIR CRUD | ⚠ Partial | No CrimeNo generation; BriefFacts not queued for NER |
| `src/services/entity_service.py` | Entity resolution | ⚠ Partial | Uses ML approach not ADR-005 rule-based |
| `src/services/graph_service.py` | Graph construction | ✅ Functional | NetworkX graph from RelationshipEdge |
| `src/services/graph_analytics_service.py` | BFS shortest path | ✅ Functional | Needs end-to-end test |
| `src/services/rag_service.py` | RAG query | ✅ Functional | MockProvider path verified |
| `src/services/risk_service.py` | Risk scoring | ✅ Functional | Feature list not validated against approved 4 |
| `src/services/anomaly_service.py` | z-score anomaly | ✅ Functional | Not tested with seed data |
| `src/services/fairness_service.py` | Fairness check | ✅ Functional | Scoring halt-on-fail not wired |
| `src/services/audit_service.py` | Audit logging | ✅ Functional | Missing events for AI actions |
| `src/services/auth_service.py` | Auth lifecycle | ✅ Functional | Refresh token single-use not enforced |
| `src/pipelines/` | NER, entity pipelines | ⚠ Scaffold | spaCy model loading path needs verification |
| `src/alembic/` | DB migrations | ✅ 6 versions | Must add AIExtractionQueue, ERMergeCandidate, EvidenceMaster |
| `src/database.py` | SQLAlchemy async engine | ✅ Complete | PostgreSQL (prod) / SQLite (dev) |
| `src/config.py` | Settings (Pydantic) | ✅ Complete | All env vars documented in .env.example |

### 7.2 Frontend (`apps/web/`)

| Asset | Type | Completeness | Notes |
|-------|------|-------------|-------|
| `apps/web/src/features/auth/` | Login/auth UI | ✅ Scaffolded | Route guards exist |
| `apps/web/src/features/cases/` | FIR list and detail | ⚠ Scaffold | New FIR form not built |
| `apps/web/src/features/entities/` | Entity profile, merge | ⚠ Scaffold | Merge review UI not built |
| `apps/web/src/features/graph/` | Cytoscape.js canvas | ⚠ Scaffold | Graph renders; BFS UI not built |
| `apps/web/src/features/hotspot/` | MapLibre heatmap | ⚠ Scaffold | Map renders; drill-down not built |
| `apps/web/src/features/anomalies/` | Alert badges | ⚠ Scaffold | Badge display not integrated |
| `apps/web/src/features/rag/` | Ask Berunda | ⚠ Scaffold | Citation display not verified |
| `apps/web/src/features/risk/` | Risk score panel | ⚠ Scaffold | Feature importance bar chart not built |
| `apps/web/src/features/audit/` | Audit log view | ⚠ Scaffold | Own-only filter for INVESTIGATOR not wired |
| `apps/web/src/features/admin/` | User management | ⚠ Scaffold | Role change, deactivate not built |
| `apps/web/src/features/analytics/` | Trend charts | ⚠ Scaffold | P1 feature — behind P0 |
| `apps/web/src/features/reports/` | Reports | ⚠ Scaffold | P2 stretch |
| `apps/web/src/features/ingestion/` | Document upload | ⚠ Scaffold | Stratus upload not integrated |
| `apps/web/src/features/socioeconomic/` | **REJECTED** | ❌ | Not in MVP scope; remove from navigation |
| `apps/web/src/features/dashboard/` | Role dashboards | ⚠ Scaffold | Role-specific content not built |

### 7.3 Catalyst Deployment Assets

| Asset | Status | Notes |
|-------|--------|-------|
| `apps/api/` | ⚠ Placeholder | Node.js Catalyst Functions scaffold — READMEs only; no implementation |
| `apps/worker/` | ⚠ Placeholder | Catalyst Worker scaffold |
| `docs/architecture/catalyst-service-mapping.md` | ✅ | Mapping of all Catalyst services; use as reference |
| `docs/database/CATALYST_DATASTORE_SCHEMA_MAPPING.md` | ✅ | 35+ table Catalyst schema — approved for deployment |

---

## 8. Architecture Conflicts

| CONFLICT-ID | Conflict | Source A | Source B | Resolution Required |
|-------------|---------|---------|---------|-------------------|
| ARCH-CONF-001 | **Role model mismatch** — code uses 3 roles (`admin`, `analyst`, `viewer`); Phase 1 mandates 4 (`INVESTIGATOR`, `SCRB_ANALYST`, `COMPLIANCE`, `ADMIN`) | `middleware/auth.py` | Phase 1 doc 02 | ARCH-DEC-004: rename roles; add COMPLIANCE and SCRB_ANALYST |
| ARCH-CONF-002 | **`socioeconomic` frontend module** exists in `apps/web/src/features/` but is not in the MVP scope | `apps/web/src/features/socioeconomic/` | `04-MVP-SCOPE` P3 deferred | Remove from navigation; do not build |
| ARCH-CONF-003 | **Entity resolution service uses ML** (`learned_entity_resolution_service.py`) but ADR-005 mandates rule-based blocking + weighted scoring | `services/learned_entity_resolution_service.py` | ADR-005 | ARCH-DEC: implement rule-based service; ML service is Phase 2+ |
| ARCH-CONF-004 | **Neo4j service reference** in `main.py` lifespan — Neo4j deferred to Phase 3+ per ADR-004 and ADR-008 | `src/main.py` lines 115-121 | ADR-004, ADR-008 | Remove Neo4j init from lifespan for MVP; keep as conditional optional |
| ARCH-CONF-005 | **`src_EvidenceMaster` table missing from ORM models** — FIR document upload (FEAT-011) requires it | `src/models/` — no EvidenceMaster | FR-FIR-003 | Add Alembic migration; add ORM model |
| ARCH-CONF-006 | **AI extraction queue missing** — NER output has no persistence table between extraction and officer review | `src/models/` — no extraction queue | FR-AI-001, FR-AI-003 | ARCH-DEC-002: add `int_AIExtractionQueue` table |
| ARCH-CONF-007 | **Merge candidate queue missing** — entity resolution has no candidate storage | `src/models/` — no ERMergeCandidate | FR-AI-005, FR-AI-006 | ARCH-DEC-003: add `int_ERMergeCandidate` table |
| ARCH-CONF-008 | **CasteRef/ReligionRef not mapped on Accused** — `src_Accused` ORM model lacks CasteRef FK despite `src_CasteMaster` existing | `src/models/src_models.py` Accused class | ADR-007, FR-AUTH-005 | Add CasteRef/ReligionRef FK to Accused (optional, nullable); enforce ORM-level exclusion |
| ARCH-CONF-009 | **RAG jurisdiction scoping absent** — `rag_service.py` retrieves chunks without district filter | `services/rag_service.py` | FR-AI-011, FR-AUTH-004 | Add `TenantDistrictID` filter to chunk retrieval query (column already exists in `int_RAGCorpusChunk`) |
| ARCH-CONF-010 | **Fairness check does not halt risk scoring** — `fairness_service.py` computes and stores result but does not block `risk_service.py` | `services/fairness_service.py` | FR-AI-016 | Wire fairness gate into risk scoring batch trigger |

---

## 9. Missing Technical Decisions

| ARCH-DEC-ID | Decision Required | Context | Options | Recommendation | Blocking Feature | ADR Required? |
|-------------|-----------------|---------|---------|---------------|-----------------|--------------|
| ARCH-DEC-001 | Demo deployment: FastAPI on AppSail vs Node.js Functions | ADR-009 permits dual; ADR-002 requires Catalyst | A: FastAPI on AppSail (proven); B: Node.js Functions (untested) | **A — AppSail** for all ML-heavy routes (graph, risk, RAG, NER); Functions for lightweight CRUD | FEAT-090 | Yes |
| ARCH-DEC-002 | AI extraction queue storage | Between NER run and officer review, where do suggestions live? | A: `int_AIExtractionQueue` DB table; B: Redis temp storage; C: In-memory dict | **A — DB table** — demo reliability; persists across restarts | FEAT-020, FEAT-021 | No (implement) |
| ARCH-DEC-003 | Entity resolution merge queue storage | Merge candidates between pipeline run and officer review | A: `int_ERMergeCandidate` DB table; B: Redis | **A — DB table** — same rationale | FEAT-022, FEAT-023 | No (implement) |
| ARCH-DEC-004 | Role name reconciliation | Code uses admin/analyst/viewer; Phase 1 uses 4 different names | A: Rename in code; B: Map at middleware | **A — rename in code** — avoids dual mapping complexity | FEAT-002 | No (config change) |
| ARCH-DEC-005 | File upload pipeline | Upload to Stratus with or without streaming | A: Stream directly to Stratus; B: Buffer → validate → Stratus | **B — buffer+validate** — MIME check requires content inspection | FEAT-011 | No |
| ARCH-DEC-006 | RAG vector index | Where do embeddings live for similarity search? | A: In-process FAISS; B: `int_RAGCorpusChunk.Embedding` (pgvector); C: Catalyst NoSQL | **A — FAISS in-process on AppSail** for demo scale (≤5000 FIRs) | FEAT-050 | No |
| ARCH-DEC-007 | OCR for FIR document | How to extract text from uploaded PDF/image? | A: Catalyst Zia (unverified availability); B: Tesseract offline; C: Python PDF text extraction only (no image OCR) | **C for MVP** — PyPDF2 for PDFs; skip image OCR; mark as gap for Phase 2 | FEAT-011 | No |

---

## 10. Data Dependencies

### Missing Tables (must add before P0 implementation)

| Table | Purpose | Required For | Priority |
|-------|---------|-------------|---------|
| `int_AIExtractionQueue` | Holds NER suggestions awaiting officer review | FEAT-020, FEAT-021 | P0 |
| `int_ERMergeCandidate` | Holds entity resolution candidates awaiting officer decision | FEAT-022, FEAT-023 | P0 |
| `src_EvidenceMaster` | Links uploaded file to case; stores hash, Stratus path | FEAT-011 | P0 |
| `src_OccurrencePlace` | Structured location extracted from FIR | FEAT-026 (P1) | P1 |
| `int_FIRProcessingState` | Tracks upload → OCR → NER → review state | FEAT-011, FEAT-020 | P0 |

### Existing Tables Requiring Schema Changes

| Table | Required Change | Required For |
|-------|---------------|-------------|
| `src_Accused` | Add nullable `CasteRef` FK → `src_CasteMaster`, `ReligionRef` FK → `src_ReligionMaster` | ADR-007, FR-AUTH-005 |
| `src_Victim` | Same as Accused | ADR-007 |
| `src_ComplainantDetails` | Already has `CasteID` and `ReligionID` — add FK enforcement | ADR-007 |
| `auth_User` | Add `role` field using 4-role enum: INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, ADMIN | FEAT-002 |
| `int_PersonEntity` | Confirm aliases JSON field exists or add it | FEAT-024 |

---

## 11. AI Dependencies

| AI Capability | Feature | Technology | Status | Gap |
|--------------|---------|-----------|--------|-----|
| Named Entity Recognition | FEAT-020 | spaCy en_core_web_md | ⚠ Pipeline scaffold — model download not in Docker image | Must verify spaCy model is loaded in AppSail runtime |
| Entity resolution scoring | FEAT-022 | Custom rule-based (Soundex + weighted) | ❌ Not implemented — ML stub exists | Must implement ADR-005 algorithm |
| Graph BFS | FEAT-031 | NetworkX | ✅ Implemented | End-to-end test required |
| Risk scoring | FEAT-060 | scikit-learn LogisticRegression | ✅ Implemented | Feature list must be validated |
| Fairness check | FEAT-062 | Custom Python — feature list inspection | ✅ Implemented | Scoring halt-on-fail not wired |
| RAG query | FEAT-050 | OpenAI/Groq/Mock + FAISS | ✅ Implemented | Jurisdiction scoping on chunk retrieval missing |
| RAG embedding | FEAT-050 | OpenAI text-embedding-3-small / Groq | ✅ `embedding_service.py` | Verify cost and rate limit |
| RAG MockProvider | FEAT-056 | Static response library | ✅ Implemented | Pre-scripted responses for 3 rehearsed questions needed |
| OCR | FEAT-011 | Catalyst Zia or Tesseract | ❌ Not integrated | MVP: skip image OCR; use PyPDF2 text extraction only |
| Anomaly detection | FEAT-043 | scipy z-score / custom | ✅ Implemented | Must verify with seed data |

---

## 12. Security Dependencies

| Security Requirement | Current State | Gap |
|---------------------|-------------|-----|
| bcrypt password hashing (NFR-SEC-001) | ✅ `auth_service.py` uses bcrypt | None |
| HTTPS enforcement (NFR-SEC-002) | ⚠ Not enforced in dev; Catalyst AppSail/API GW enforces in prod | Document that dev is HTTP-only |
| JWT HS256 + 256-bit key (NFR-SEC-003) | ✅ Implemented | Key rotation strategy not documented |
| Pydantic input validation (NFR-SEC-004) | ✅ All routers use Pydantic schemas | MIME check for uploads needs content inspection |
| No secrets in code (NFR-SEC-005) | ✅ .env.example has placeholders only | CI secret scan recommended |
| CasteRef/ReligionRef ORM exclusion (ADR-007) | ⚠ Documented; not yet ORM-level | Must implement before demo |
| Protected-characteristic refusal in RAG (FR-AUTH-005 + AC-RAG-003) | ❌ Not implemented | Add guardrail to `guardrails_service.py` |
| Audit log immutability (NFR-AUT-001) | ⚠ No DELETE endpoint; DB-level DENY not confirmed | Add DB permission check in deployment |
| Rate limiting on RAG endpoint (FR-SRCH-001 + rag_router) | ✅ `slowapi` 5 req/min on `/api/v1/rag` | None |

---

## 13. Catalyst Dependencies

| Catalyst Service | Required For | Current State | Risk |
|-----------------|-------------|--------------|------|
| Catalyst Data Store | All database operations | Schema mapping exists; not deployed | High — must deploy Day 1 |
| Catalyst Stratus | File upload (FEAT-011) | Not integrated | Medium — PyPDF2 fallback for text-only |
| Catalyst AppSail | FastAPI Python runtime | Not deployed | High — required for demo |
| Catalyst API Gateway | Routing + auth throttle | Not deployed | Medium — local CORS + FastAPI handles locally |
| Catalyst Functions (Node.js) | Production lightweight CRUD | Placeholder READMEs | High — blocked on ARCH-DEC-001 |
| Catalyst Auth | JWT auth (optional — self-hosted JWT preferred) | Not integrated | Low — self-hosted JWT is primary per ADR-009 |
| Catalyst Zia | OCR for image uploads | Not evaluated | Low — MVP skips image OCR per ARCH-DEC-007 |
| Catalyst QuickML | AutoML for risk scoring | Not evaluated | Low — scikit-learn is fallback |
| Catalyst Job Scheduling | Nightly batch (anomaly + risk) | Not deployed | Medium — inline BackgroundTasks used per ADR-011 |
| Catalyst Pipelines (CI/CD) | Automated deployment | GitHub Actions active; Catalyst Pipelines not set up | Low — GitHub Actions sufficient |

---

## 14. External Integration Dependencies

| Integration | Required For | Status | MVP Plan |
|------------|-------------|--------|---------|
| OpenAI API | FEAT-050 RAG query | Configured; key needed | MockProvider fallback always available |
| Groq API | FEAT-050 RAG query (alternative) | Configured | Same as OpenAI |
| spaCy model download | FEAT-020 NER | Model not in container | Add to AppSail Dockerfile / requirements |
| MapLibre GL JS | FEAT-040 hotspot map | ✅ Included in frontend | Tile server: use free OpenStreetMap tiles |
| Cytoscape.js | FEAT-030 graph | ✅ Included in frontend | None |
| Recharts | FEAT-044-046 analytics charts | ✅ Included in frontend | None |
| CCTNS | UC-020 | 🔒 Future-restricted — legal MOU required | Never in MVP |
| Open-Meteo | Weather correlation | Not critical for MVP | Skip for MVP |
| Overpass API (OSM) | Police station boundaries | Not critical for MVP | Skip for MVP |

---

## 15. Phase 2 Blockers

These 8 items block Phase 2 implementation from starting safely:

| BLOCKER-ID | Description | Blocks | Resolution |
|-----------|-------------|--------|-----------|
| BLK-001 | 3-role to 4-role migration in `middleware/auth.py` and `auth_models.py` | All RBAC features | ARCH-DEC-004; Day 1 |
| BLK-002 | `int_AIExtractionQueue` table missing | FEAT-020, FEAT-021, FEAT-023 | ARCH-DEC-002; add Alembic migration; Day 2 |
| BLK-003 | `int_ERMergeCandidate` table missing | FEAT-022, FEAT-023 | ARCH-DEC-003; add Alembic migration; Day 2 |
| BLK-004 | `src_EvidenceMaster` ORM model missing | FEAT-011 | Add to `src_models.py` + migration; Day 2 |
| BLK-005 | CrimeNo generation not implemented | FEAT-012 | Add `generate_crime_no()` to `fir_service.py`; Day 2 |
| BLK-006 | RAG jurisdiction scoping absent | FEAT-050 (P0) | Add district filter to `rag_service.py`; Day 3 |
| BLK-007 | Entity resolution rule-based algorithm not implemented | FEAT-022 (P0) | Implement Soundex blocking + weighted scorer in `entity_service.py`; Day 2-3 |
| BLK-008 | Fairness check does not halt risk scoring | FEAT-062 (P0) | Wire `fairness_service.check()` result into `risk_service.batch_compute()`; Day 3 |

---

## 16. Recommended Architecture Work Sequence

```
Day 1:  Deploy Catalyst project + schema (FEAT-091)
        Role migration: 3→4 roles (BLK-001)
        Add missing DB tables via Alembic (BLK-002, 003, 004)
        Fix start-here.md navigation (CONFLICT-003 from Phase 1)

Day 2:  Implement CrimeNo generation (BLK-005)
        Implement FIR manual creation endpoint fully (FEAT-010)
        Implement FIR status lifecycle state machine (FEAT-015)
        Begin entity resolution rule-based algorithm (BLK-007)
        Implement AI extraction pipeline + queue (BLK-002)

Day 3:  Complete entity resolution + merge candidate queue (BLK-003, 007)
        Implement human review/approve/reject endpoints (FEAT-021, 023)
        Add RAG jurisdiction scoping (BLK-006)
        Wire fairness gate into risk scoring (BLK-008)
        Begin FIR document upload (FEAT-011)

Day 4:  Complete FIR upload + MIME validation + hash (FEAT-011)
        Implement global search (FEAT-014)
        Implement PersonEntity canonical profile (FEAT-024)
        FIR detail multi-tab view (FEAT-013)

Day 5:  Complete graph BFS UI (FEAT-031 frontend)
        Hotspot map district drill-down (FEAT-041)
        Anomaly alert badge integration (FEAT-043 frontend)
        Validate seed data planted patterns (AC-SEED-001)

Day 6:  Risk score feature importance display (FEAT-061 frontend)
        Fairness dashboard COMPLIANCE/SCRB_ANALYST views (FEAT-063)
        Ask Berunda pre-scripted MockProvider responses
        Audit log own-only filter (FEAT-080)

Day 7:  AppSail deployment + API Gateway routing
        End-to-end integration tests (P0 acceptance criteria)
        User management ADMIN screen (FEAT-081)

Day 8:  Full demo rehearsal — all 15 DEMO-STEP items
        P0 gap closure
        Fallback video recording

Day 9:  Scope freeze — bug fixes only
Day 10: Second demo rehearsal + polish
Day 11: Submission
```

---

*End of 00-PHASE-1-INPUT-AND-ARCHITECTURE-AUDIT.md*
