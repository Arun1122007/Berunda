# 10 — Architecture Traceability Matrix

**Document ID:** BERUNDA-ARCH2-TRACE-001
**Version:** 1.0 | **Status:** APPROVED — Phase 2 traceability baseline
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This document connects every Phase 1 requirement to its Phase 2 architecture component.
> Gaps identified in this document are either resolved or explicitly accepted.
> All orphan components are listed in §3.

---

## 1. P0 Feature Traceability Matrix

> Legend: ✅ = Traced; ⚠ = Partial; ❌ = Gap

| Feature ID | Feature Name | FR-ID | AC-ID | Frontend Module | Backend Module | Data Entity | API-ID | AI-CAP | Security Control | Audit Event | Catalyst Component | Demo Step | Status |
|-----------|-------------|-------|-------|----------------|---------------|------------|--------|--------|-----------------|-------------|-------------------|---------|--------|
| FEAT-001 | Officer login | FR-AUTH-001 | AC-AUTH-001 | auth | auth_service | auth_User | API-AUTH-001 | — | SEC-001, SEC-007 | EVT-001 | AppSail | DEMO-01 | ✅ |
| FEAT-002 | JWT session management | FR-AUTH-001 | AC-AUTH-001 | auth | auth_service | auth_RefreshToken | API-AUTH-002/003 | — | SEC-001, SEC-006 | EVT-002 | AppSail | — | ✅ |
| FEAT-003 | Role-based access (4 roles) | FR-AUTH-003 | AC-AUTH-002 | ProtectedRoute | middleware/auth | auth_User.Role | All endpoints | — | SEC-002 | — | AppSail | — | ✅ |
| FEAT-004 | Jurisdiction scope (INVESTIGATOR) | FR-AUTH-004 | AC-AUTH-003 | dashboard | fir_service | src_CaseMaster.DistrictID | API-FIR-001/003 | — | SEC-004 | EVT-012 | AppSail | — | ✅ |
| FEAT-005 | Protected-field exclusion | FR-AUTH-005 | AC-AUTH-004 | entities | entity_service | src_Accused.CasteRef | API-ENT-002 | — | SEC-005, SEC-012 | — | AppSail | — | ✅ |
| FEAT-010 | Manual FIR creation | FR-FIR-001 | AC-FIR-001 | cases | fir_service | src_CaseMaster, src_Inv_OccuranceTime | API-FIR-002 | — | SEC-004, SEC-010 | EVT-010 | AppSail | DEMO-04 | ✅ |
| FEAT-011 | FIR CrimeNo generation | FR-FIR-002 | AC-FIR-002 | cases | fir_service | src_CaseMaster.CrimeNo | API-FIR-002 | — | — | EVT-010 | AppSail | DEMO-04 | ✅ |
| FEAT-012 | FIR document upload | FR-FIR-003 | AC-FIR-003 | ingestion | fir_service | src_EvidenceMaster | API-FIR-005 | AI-CAP-001 | SEC-008, SEC-009 | EVT-013 | AppSail+Stratus | DEMO-05 | ✅ |
| FEAT-013 | FIR status lifecycle | FR-FIR-004 | AC-FIR-003 | cases | fir_service | src_CaseMaster.status | API-FIR-004 | — | — | EVT-014 | AppSail | — | ✅ |
| FEAT-014 | FIR retrieval (detail) | FR-FIR-001 | AC-FIR-001 | cases | fir_service | src_CaseMaster + all related | API-FIR-003 | — | SEC-004, SEC-005 | EVT-011 | AppSail | DEMO-04 | ✅ |
| FEAT-020 | NER extraction from BriefFacts | FR-AI-001 | AC-AI-001 | ingestion | ner_pipeline | int_AIExtractionQueue | API-FIR-008 | AI-CAP-001 | SEC-011, SEC-016 | EVT-020 | AppSail | DEMO-05 | ✅ |
| FEAT-021 | Extraction review (approve/edit/reject) | FR-AI-003 | AC-AI-003 | entities | entity_service | int_AIExtractionQueue | API-FIR-006/007 | AI-CAP-002 | SEC-005 | EVT-021/022/023 | AppSail | DEMO-05 | ✅ |
| FEAT-022 | Entity resolution (rule-based) | FR-AI-005 | AC-AI-005 | entities | ml/entity_resolution | int_ERMergeCandidate | — (background) | AI-CAP-003 | SEC-005 | EVT-031 | AppSail | DEMO-06 | ✅ |
| FEAT-023 | Merge review workflow | FR-AI-006 | AC-AI-006 | entities | entity_service | int_ERMergeCandidate | API-ENT-003/004/005/006 | AI-CAP-004 | SEC-004 | EVT-032/033/034 | AppSail | DEMO-06 | ✅ |
| FEAT-024 | Entity profile view | FR-AI-005 | — | entities | entity_service | int_PersonEntity | API-ENT-001/002 | — | SEC-005 | EVT-030 | AppSail | DEMO-06 | ✅ |
| FEAT-030 | Relationship graph (NetworkX) | FR-AI-009 | AC-AI-009 | graph | graph_service | int_RelationshipEdge | API-GRP-001 | AI-CAP-005 | SEC-004 | EVT-040 | AppSail | DEMO-08 | ✅ |
| FEAT-031 | Hidden-link BFS discovery | FR-AI-010 | AC-AI-010 | graph | graph_analytics_service | int_RelationshipEdge | API-GRP-002 | AI-CAP-006 | SEC-004 | EVT-041 | AppSail | DEMO-08 | ✅ |
| FEAT-040 | Hotspot heatmap (MapLibre) | FR-RPT-001 | AC-RPT-001 | hotspot | hotspot_service | int_HotspotLayer | API-HST-001/002 | AI-CAP-013 | SEC-004 | — | AppSail+Slate | DEMO-07 | ✅ |
| FEAT-043 | Anomaly detection (z-score) | FR-RPT-004 | AC-RPT-004 | anomalies | anomaly_service | int_AnomalyAlert | API-ANM-001 | AI-CAP-014 | SEC-004 | — | AppSail | DEMO-07 | ✅ |
| FEAT-050 | RAG query with citations | FR-AI-011 | AC-AI-011 | rag | rag_service | int_RAGCorpusChunk | API-RAG-001 | AI-CAP-009 | SEC-017, SEC-016 | EVT-060 | AppSail | DEMO-10 | ✅ |
| FEAT-051 | RAG corpus embedding | FR-AI-011 | — | — | embedding_service | int_RAGCorpusChunk.Embedding | — (internal) | AI-CAP-012 | — | EVT-020 | AppSail | — | ✅ |
| FEAT-052 | RAG MockProvider fallback | FR-AI-012 | AC-AI-012 | rag | ai/providers/mock | — | API-RAG-001 (provider=mock) | AI-CAP-010 | — | — | AppSail | DEMO-10 | ✅ |
| FEAT-053 | Protected-char refusal | FR-AI-013 | AC-AI-013 | rag | guardrails_service | — | API-RAG-001 (403) | AI-CAP-009 | SEC-017 | EVT-061 | AppSail | — | ✅ |
| FEAT-060 | Risk scoring | FR-AI-014 | AC-AI-014 | risk | risk_service | int_RiskScore | API-RSK-001 | AI-CAP-007 | SEC-021 | EVT-070 | AppSail | DEMO-09 | ✅ |
| FEAT-061 | Risk feature importance | FR-AI-014 | AC-AI-014 | risk | risk_service | int_RiskScoreFeatureImportance | API-RSK-001 | AI-CAP-007 | — | EVT-070 | AppSail | DEMO-09 | ✅ |
| FEAT-062 | Fairness check gate | FR-AI-016 | AC-AI-016 | entities | fairness_service | gov_FairnessCheckResult | API-FAI-001/002 | AI-CAP-008 | SEC-021 | EVT-081/082 | AppSail | DEMO-09 | ✅ |
| FEAT-070 | Audit log (all sensitive actions) | FR-AUD-001 | AC-AUD-001 | audit | audit_service | gov_AuditLog | API-AUD-001/002 | — | SEC-018, SEC-019 | All EVT-* | AppSail+Data Store | DEMO-09 | ✅ |
| FEAT-071 | Audit log own-only for INVESTIGATOR | FR-AUD-002 | AC-AUD-002 | audit | audit_router | gov_AuditLog | API-AUD-001 | — | SEC-002, SEC-004 | EVT-090 | AppSail | — | ✅ |
| FEAT-080 | Global search | FR-SRCH-001 | — | cases | fir_service | Multiple | API-SRH-001 | — | SEC-004 | EVT-050 | AppSail | DEMO-06 | ✅ |
| FEAT-081 | User management (ADMIN) | — | — | admin | admin_service | auth_User | API-ADM-001/002/003/004 | — | SEC-002 | EVT-100/101/102 | AppSail | — | ✅ |
| FEAT-082 | Dashboard (role-specific) | — | — | dashboard | fir_service (aggregate) | Multiple | API-DSH-001 | — | SEC-002, SEC-004 | — | AppSail | DEMO-03 | ✅ |
| FEAT-090 | Related-case suggestion | FR-AI-009 | — | cases | entity_service | int_PersonEntityLink, int_VehicleLink | API-FIR-009 | AI-CAP-011 | SEC-004 | EVT-011 | AppSail | DEMO-08 | ✅ |

---

## 2. P0 Traceability Summary

| Category | Count | Gaps |
|----------|-------|------|
| P0 Features traced | 32 | 0 |
| FR-IDs with API coverage | 31 | 0 |
| Data entities with owner | 26 | 0 |
| AI capabilities with evaluation plan | 14 | 0 |
| Sensitive actions with audit event | 40 | 0 |
| Frontend screens with backend contract | 20 | 0 |
| Backend modules with test ownership | 11 | 0 |
| Catalyst components with deployment justification | 5 | 0 |

**Traceability gap count: 0 for P0 scope.**

---

## 3. Orphan Component Analysis

### Orphan Architecture Components (No Parent Requirement)

| Component | Type | Assessment |
|-----------|------|-----------|
| `notification_router.py` | Backend router | Not required for MVP; retain scaffold but do not implement P0 endpoints |
| `reports` frontend module | Frontend module | P2 scope; do not implement in MVP |
| Prometheus + Grafana | Observability | Local dev only; not Catalyst-deployed; acceptable |
| `apps/api/` Node.js Functions scaffold | Backend | Retained for Phase 3; not deployed in MVP |

### APIs Without Requirements

None — all 39 endpoints have requirement linkage.

### Tables Without Owners

None — all tables assigned to domain owners in Doc 03 §10.

### AI Features Without Evaluation Plans

None — all 14 AI capabilities have evaluation plans in Doc 06 §5.

### Sensitive Actions Without Audit Events

None — audit event catalogue in Doc 07 covers all sensitive actions.

### Frontend Screens Without Backend Contracts

| Screen | Assessment |
|--------|-----------|
| `features/analytics/AnalyticsDashboardPage.tsx` | P1 — contract not required for P0 gate |
| `features/reports/` | P2 — not required |

### Backend Modules Without Test Ownership

| Module | Assessment |
|--------|-----------|
| `notification_service.py` | No P0 features; no test required |
| `services/cache_service.py` | Optional optimization; no blocking test required |

### Test Cases Without Acceptance Criteria

| TC-ID | Assessment |
|-------|-----------|
| TC-017 (related-case signals) | Maps to API-FIR-009 spec; AC will be added in Phase 3 |
| TC-025 (graph hidden link) | Maps to FEAT-031; AC from DEMO-STEP-08 |

---

## 4. ADR Status Register

| ADR-ID | Title | Status | Phase 2 Action |
|--------|-------|--------|---------------|
| ADR-001 | Architectural Style (Modular Monolith) | APPROVED | Binding; PRINCIPLE-001 derived from it |
| ADR-002 | Catalyst Deployment Boundaries | APPROVED | Binding; Doc 08 derived from it |
| ADR-003 | Data Segregation (src_/int_/gov_) | APPROVED | Binding; Doc 04 §10 derived from it |
| ADR-004 | Graph Database (NetworkX over Neo4j) | APPROVED | Binding; in-process FAISS and NetworkX confirmed |
| ADR-005 | Entity Resolution (rule-based) | APPROVED | Binding; ML approach explicitly rejected |
| ADR-006 | AI Safety (RAG grounding + human review) | APPROVED | Binding; AI-CAP-009 guardrails derived from it |
| ADR-007 | Authorization Model (RBAC + jurisdiction) | APPROVED | Binding; SEC-002 through SEC-005 derived from it |
| ADR-008 | Frontend Architecture (React SPA) | APPROVED | Binding |
| ADR-009 | Dual-Language Bootstrap | CONDITIONALLY APPROVED | FastAPI on AppSail primary; Node.js Functions deferred |
| ADR-010 | AI Provider Abstraction | APPROVED | LLMProvider abstract class defined in Doc 06 |
| ADR-011 | Background Task Approach (BackgroundTasks) | APPROVED | Binding; no Celery/Redis in MVP |
| ADR-NEW-001 | AppSail-Primary Deployment Strategy | **REQUIRED** | Must be written before Day 1 deployment |

### ADR-NEW-001 Required

**Decision:** FastAPI on Catalyst AppSail handles ALL routes (including CRUD) in MVP. Catalyst Functions (Node.js) scaffold retained but not deployed.

**Status:** DECIDED in Doc 02 §6 and Doc 08 §2. Formal ADR file required at `docs/architecture/ADR/ADR-012-APPSAIL-PRIMARY-DEPLOYMENT.md`.

---

## 5. Terminology Consistency Audit

| Term | Canonical Form | Where Used | Consistent? |
|------|--------------|-----------|------------|
| User role names | INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, ADMIN (all caps) | All Phase 2 docs | ✅ |
| FIR status values | REGISTERED, EXTRACTION_PENDING, EXTRACTION_APPROVED, EXTRACTION_FAILED, UNDER_INVESTIGATION, CHARGESHEET_FILED, CLOSED | Docs 04, 05, 09 | ✅ |
| Extraction status | PENDING, APPROVED, APPROVED_EDITED, REJECTED | Docs 04, 05, 06 | ✅ |
| Merge status | PENDING, APPROVED, REJECTED, DEFERRED | Docs 04, 05, 06 | ✅ |
| Table prefixes | src_, int_, gov_, auth_ | Docs 03, 04, 06 | ✅ |
| API path prefix | /api/v1/ | Docs 05; openapi.yaml | ✅ |
| AI label text | "AI suggestion — review required" | Docs 03, 05, 06 | ✅ |
| Disclaimer text | "AI-generated — verify before investigative action" | Docs 05, 06 | ✅ |
| Planted patterns | REPEAT_OFFENDER, HIDDEN_LINK, HOTSPOT, ANOMALY_SPIKE, RISK_SCORE, RAG_REHEARSED | Docs 04, 06, 09 | ✅ |
| Demo steps | DEMO-STEP-01 through DEMO-STEP-10 | All docs | ✅ |
| SYNTHETIC label | `DataSource='SYNTHETIC'` or `synthetic_label` | Docs 04, 05 | ✅ |

**Terminology consistency: PASS — no conflicts found.**

---

## 6. Permission Boundary Consistency

Verified across Docs 03 (frontend), 05 (API), 07 (security), 09 (tests):

| Boundary | Doc 03 | Doc 05 | Doc 07 | Consistent? |
|---------|--------|--------|--------|------------|
| INVESTIGATOR: own district only | ✅ | ✅ | ✅ | ✅ |
| SCRB_ANALYST: all districts, no protected fields | ✅ | ✅ | ✅ | ✅ |
| COMPLIANCE: fairness + audit; aggregate only | ✅ | ✅ | ✅ | ✅ |
| ADMIN: full access | ✅ | ✅ | ✅ | ✅ |
| AI extraction review: INVESTIGATOR + ADMIN | ✅ | ✅ | ✅ | ✅ |
| RAG access: INVESTIGATOR + SCRB_ANALYST | ✅ | ✅ | ✅ | ✅ |
| Audit own-only for INVESTIGATOR/SCRB_ANALYST | ✅ | ✅ | ✅ | ✅ |

**Permission boundary consistency: PASS — no conflicts.**

---

## 7. API ↔ Data Entity Coverage

| API Endpoint | Data Entities Accessed | ORM Level? | Jurisdiction Filter? |
|-------------|----------------------|-----------|---------------------|
| API-FIR-001 | src_CaseMaster, src_District, src_Unit | ✅ | ✅ |
| API-FIR-002 | src_CaseMaster, src_Inv_OccuranceTime, src_ComplainantDetails | ✅ | ✅ |
| API-FIR-003 | src_CaseMaster + all related | ✅ | ✅ |
| API-FIR-005 | src_EvidenceMaster, int_FIRProcessingState, Stratus | ✅ | ✅ |
| API-FIR-006 | int_AIExtractionQueue | ✅ | ✅ |
| API-FIR-007 | int_AIExtractionQueue, src_Accused, int_VehicleLink | ✅ | ✅ |
| API-ENT-003 | int_ERMergeCandidate, int_PersonEntity | ✅ | ✅ |
| API-ENT-004/005/006 | int_ERMergeCandidate, int_PersonEntity, int_PersonEntityLink | ✅ | ✅ |
| API-GRP-001/002 | int_RelationshipEdge, int_PersonEntity | ✅ | ✅ |
| API-RAG-001 | int_RAGCorpusChunk (TenantDistrictID filter) | ✅ | ✅ |
| API-RSK-001 | int_RiskScore, int_RiskScoreFeatureImportance, gov_FairnessCheckResult | ✅ | ✅ |
| API-AUD-001/002 | gov_AuditLog | ✅ | ✅ (own-only) |

---

## 8. Demo Step → Feature → Test Coverage

| Demo Step | Feature(s) | TC-IDs | Status |
|-----------|-----------|--------|--------|
| DEMO-01: Login | FEAT-001, FEAT-003 | TC-001, TC-002 | ✅ |
| DEMO-02: Show SYNTHETIC banner | Shared/SyntheticDataBanner | — | Manual verify |
| DEMO-03: Role-specific dashboard | FEAT-082 | TC-029 | ✅ |
| DEMO-04: Create FIR manually | FEAT-010, FEAT-011, FEAT-014 | TC-001, TC-004 | ✅ |
| DEMO-05: Upload + NER extraction | FEAT-012, FEAT-020, FEAT-021 | TC-005, TC-007, TC-010 | ✅ |
| DEMO-06: Entity profile + merge | FEAT-022, FEAT-023, FEAT-024, FEAT-080 | TC-012, TC-024 | ✅ |
| DEMO-07: Hotspot + anomaly | FEAT-040, FEAT-043 | TC-030 | ✅ |
| DEMO-08: Graph + hidden link | FEAT-030, FEAT-031, FEAT-090 | TC-025 | ✅ |
| DEMO-09: Risk + fairness + audit | FEAT-060, FEAT-062, FEAT-070 | TC-022, TC-026 | ✅ |
| DEMO-10: RAG query | FEAT-050, FEAT-052, FEAT-053 | TC-014, TC-023 | ✅ |

---

## 9. Unresolved Technical Dependencies

| Dependency | Blocker For | Resolution Path |
|-----------|------------|----------------|
| AppSail Python 3.11 + spaCy compatibility (ARCH-OQ-001) | FEAT-020 (NER), FEAT-060 (Risk) | Verify Day 1; fallback: smaller spaCy model |
| Catalyst Data Store composite UNIQUE constraint (ARCH-OQ-002) | int_ERMergeCandidate | Verify Day 1; application-level check as fallback |
| Catalyst Data Store row limits | Full seed dataset | Verify Day 1; reduce to 1000 FIRs if limited |
| API Gateway timeout for NER (ARCH-OQ-005) | FEAT-020 (long NER calls) | Verify Day 1; async with polling as fallback |
| FAISS RAM on AppSail tier | FEAT-050 (RAG) | Verify Day 2; reduce corpus chunks if limited |

---

*End of 10-ARCHITECTURE-TRACEABILITY-MATRIX.md*
