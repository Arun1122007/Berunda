# Phase 2 Traceability Reconstruction

**Document ID:** BERUNDA-VER-P2-003
**Version:** 2.0 | **Status:** FINAL
**Date:** 2026-07-26

---

## 1. Purpose

Reconstruct traceability across Phase 2 architecture documents (design intent), the codebase (implementation reality), and OpenAPI spec (API contract). Identify gaps, orphans, and untraced requirements.

---

## 2. Traceability Key

| Symbol | Meaning |
|--------|---------|
| TRACED | Requirement present in design doc, code, and OpenAPI |
| PARTIAL | Present in design doc but missing from code or OpenAPI (annotated) |
| UNTRACED | Present in design doc, absent from both code and OpenAPI |
| ORPHAN | Present in code but absent from all design docs |
| DOC-ONLY | Documented in design, not implementable or deferred |

---

## 3. Feature-to-Implementation Traceability

### 3.1 Authentication & Authorization

| Requirement ID | Description | Design Doc | Code Status | OpenAPI Status | Verdict |
|---------------|-------------|-----------|-------------|---------------|---------|
| FR-AUTH-001 | Token-based auth (JWT access + refresh) | Doc 03 | Present in `auth_service.py` and `middleware/auth.py` | Present at `/api/v1/auth/login`, `/refresh`, `/logout` | TRACED |
| FR-AUTH-002 | Password-based login with bcrypt | Doc 03 | Present — `auth_service.py` uses `passlib.context.CryptContext` | Present at `/api/v1/auth/login` | TRACED |
| FR-AUTH-003 | 4-role RBAC (INVESTIGATOR/SCRB_ANALYST/COMPLIANCE/ADMIN) | Doc 07 SEC-002 | Code uses 3 roles (admin/analyst/officer); no enum constraint | OpenAPI has UserRole enum but with 3 values | UNTRACED |
| FR-AUTH-004 | Jurisdiction filter (INVESTIGATOR = own district only) | Doc 03 | PARTIAL — present in FIR router, absent from entity/graph/RAG/analytics services | PARTIAL — not enforced in all endpoints | PARTIAL |
| FR-AUTH-005 | Protected attribute exclusion (caste/religion) | Doc 07 SEC-003 | CasteRef/ReligionRef FKs not added to src_Accused | No endpoints for protected data filtering | UNTRACED |

### 3.2 FIR Management

| Requirement ID | Description | Design Doc | Code Status | OpenAPI Status | Verdict |
|---------------|-------------|-----------|-------------|---------------|---------|
| FR-FIR-001 | FIR CRUD (create/read/update/close) | Doc 03 | Present in `fir_router.py` — POST, GET, PUT, PATCH | Present at `/api/v1/firs` | TRACED |
| FR-FIR-002 | CrimeNo generation (YYYY/CRIME/XXXXX) | Doc 03 | CrimeNo generation not implemented — uses placeholder | OpenAPI shows CrimeNo as string but not validated | UNTRACED |
| FR-FIR-003 | Document upload to Catalyst Stratus | Doc 03 | Stratus not integrated; upload_document is a stub | Present at `/api/v1/firs/{fir_id}/documents` | PARTIAL |

### 3.3 Entity Resolution

| Requirement ID | Description | Design Doc | Code Status | OpenAPI Status | Verdict |
|---------------|-------------|-----------|-------------|---------------|---------|
| FR-AI-005 | Entity resolution (rule-based) | Doc 03, ADR-005 | Uses ML-based `learned_entity_resolution_service.py` (contradicts ADR-005). Rule-based `ml/entity_resolution.py` does not exist | Present at `/api/v1/entities/merge-queue` and `/approve/reject/defer` | UNTRACED |
| FR-AI-007 | AI extraction/entity merge | Doc 03 | NER pipeline scaffold only; merge endpoints exist but use wrong algorithm | Present at `/api/v1/firs/{fir_id}/extraction` | PARTIAL |

### 3.4 Graph Analysis

| Requirement ID | Description | Design Doc | Code Status | OpenAPI Status | Verdict |
|---------------|-------------|-----------|-------------|---------------|---------|
| FR-AI-009 | Graph representation (NetworkX for MVP) | Doc 03, ADR-004 | `graph_service.py` and `graph_router.py` exist. `neo4j_service.py` also exists (contradicts ADR-004) | Present at `/api/v1/graph/{entity_id}` and `/shortest-path` | PARTIAL |
| FR-AI-010 | BFS hidden-link discovery | Doc 03 | Shortest-path endpoint exists. Frontend BFS UI not built. | Present at `/api/v1/graph/shortest-path` | PARTIAL |

### 3.5 RAG / AI Assistant

| Requirement ID | Description | Design Doc | Code Status | OpenAPI Status | Verdict |
|---------------|-------------|-----------|-------------|---------------|---------|
| FR-AI-003 | RAG query on case corpus | Doc 06 | `rag_service.py` and `rag_router.py` working | Present at `/api/v1/rag/query` | TRACED |
| FR-AI-011 | AI provider abstraction | Doc 06 | 3 providers exist (OpenAI, Groq, Catalyst). Mock provider missing | Not applicable | PARTIAL |
| FR-AI-012 | Deterministic mock for demo | Doc 06 | `mock_provider.py` does not exist | Not applicable | UNTRACED |

### 3.6 Hotspot / Anomaly / Risk

| Requirement ID | Description | Design Doc | Code Status | OpenAPI Status | Verdict |
|---------------|-------------|-----------|-------------|---------------|---------|
| FR-AI-006 | Hotspot identification | Doc 03 | `hotspot_router.py` exists | Present at `/api/v1/hotspot` | TRACED |
| FR-AI-004 | Anomaly detection | Doc 03 | `anomaly_router.py` exists | Present at `/api/v1/anomaly` | TRACED |
| FR-AI-008 | Risk scoring | Doc 03 | `risk_router.py` exists | Present at `/api/v1/risk/{entity_id}` and `/batch-compute` | TRACED |

### 3.7 Fairness & Audit

| Requirement ID | Description | Design Doc | Code Status | OpenAPI Status | Verdict |
|---------------|-------------|-----------|-------------|---------------|---------|
| FR-AI-002 | Fairness check | Doc 06 | `fairness_router.py` exists | Present at `/api/v1/fairness/check` and `/dashboard` | TRACED |
| FR-AUD-001 | Audit logging | Doc 07 | `audit_router.py` exists. Services do not call `audit_service.log_event()` | Present at `/api/v1/audit-logs` | PARTIAL |

### 3.8 Admin & Search

| Requirement ID | Description | Design Doc | Code Status | OpenAPI Status | Verdict |
|---------------|-------------|-----------|-------------|---------------|---------|
| FEAT-081 | User management | Doc 03 | `admin_router.py` does not exist | Present at `/api/v1/admin/users` | UNTRACED |
| FR-FIR-005 | Global search | Doc 03 | `search` endpoint exists | Present at `/api/v1/search` | TRACED |
| FEAT-091 | Dashboard | Doc 03 | `dashboard` endpoint exists | Present at `/api/v1/dashboard` | TRACED |

---

## 4. ADR-to-Implementation Traceability

| ADR | Title | Implementation Status |
|-----|-------|---------------------|
| ADR-001 | Phase 1 Architectural Style | Applied — FastAPI modular structure |
| ADR-002 | Catalyst Deployment Boundaries | PARTIAL — CatalystProvider broken; no staging deploy |
| ADR-003 | Source of Record vs Intelligence Layer | Applied — src_ vs int_ table separation |
| ADR-004 | Graph Representation (NetworkX, no Neo4j) | VIOLATED — `neo4j_service.py` exists |
| ADR-005 | Entity Resolution Approach (rule-based) | VIOLATED — `learned_entity_resolution_service.py` uses ML |
| ADR-006 | RAG and NL Query Safety | Applied — `rag_service.py` with guardrails |
| ADR-007 | Sensitive Field Exclusion | PARTIAL — designed but not wired in service layer |
| ADR-008 | MVP vs Target State | Applied — MVP scope documented |
| ADR-009 | Dual-Language Bootstrap | Applied — FastAPI (dev) + Catalyst target |
| ADR-010 | Service-AI Separation Contract | Applied — separate `services/` and `ai/` directories |
| ADR-011 | Inline Task Execution | Applied — no Celery/Redis dependency |
| ADR-012 | AppSail-Primary Deployment | NOT WRITTEN — referenced but file missing |

---

## 5. Traceability Summary

| Category | Total | TRACED | PARTIAL | UNTRACED | ORPHAN | DOC-ONLY |
|----------|-------|--------|---------|----------|--------|----------|
| Features (unique FR/FEAT) | 20 | 10 | 5 | 5 | 0 | 0 |
| ADRs | 12 | 6 | 2 | 0 | 0 | 1 (ADR-012) |
| Routers | 15 | 9 | 0 | 1 (admin) | 5 | 0 |
| OpenAPI endpoints | 38 | 30 | 5 | 3 | 0 | 0 |
| **Total Checkpoints** | **85** | **55 (65%)** | **12 (14%)** | **9 (11%)** | **5 (6%)** | **1 (1%)** |

---

## 6. Orphan Code (No Design Intent)

| Orphan | File | Est. Effort to Remove |
|--------|------|----------------------|
| Offender router | `src/routers/offender_router.py` | 0.5 day |
| Socioeconomic router | `src/routers/socioeconomic_router.py` | 0.5 day |
| AI Assistant router | `src/routers/ai_assistant_router.py` | 0.5 day |
| Ingestion router | `src/routers/ingestion_router.py` | 1 day |
| Notification router | `src/routers/notification_router.py` | 0.5 day |
| Phase2 duplicate scaffold | `src/phase2_backend/` | 1 day |
| Socioeconomic frontend | `apps/web/src/features/socioeconomic/` | 0.5 day |
| Neo4j service | `src/services/neo4j_service.py` | 1 day (contents to migrate to NetworkX) |

---

## 7. API Endpoint Coverage

| Endpoint Group | OpenAPI | Code (router exists) | Match |
|---------------|---------|---------------------|-------|
| Auth (login/refresh/logout) | 3 endpoints | `auth_router.py` | MATCH |
| FIRs (CRUD + ai-analysis + documents + extraction + status + related-cases) | 10 endpoints | `fir_router.py` | MATCH |
| Entities (list/get/merge-queue/merge-approve/reject/defer) | 6 endpoints | `entity_router.py` | MATCH |
| Graph (entity-detail/shortest-path) | 2 endpoints | `graph_router.py` | MATCH |
| Search | 1 endpoint | internal to `fir_router.py` or search | NOT FOUND |
| Hotspot (list/district) | 2 endpoints | `hotspot_router.py` | MATCH |
| Anomaly | 1 endpoint | `anomaly_router.py` | MATCH |
| Risk (entity/batch) | 2 endpoints | `risk_router.py` | MATCH |
| RAG query | 1 endpoint | `rag_router.py` | MATCH |
| Fairness (check/dashboard) | 2 endpoints | `fairness_router.py` | MATCH |
| Audit logs (list/detail) | 2 endpoints | `audit_router.py` | MATCH |
| Dashboard | 1 endpoint | internal | NOT FOUND |
| Admin (users list/create/role/deactivate) | 4 endpoints | `admin_router.py` | MISSING |
| Health (health/ready) | 2 endpoints | `main.py` | MATCH |

*End of PHASE-2-TRACEABILITY-RECONSTRUCTION.md*
