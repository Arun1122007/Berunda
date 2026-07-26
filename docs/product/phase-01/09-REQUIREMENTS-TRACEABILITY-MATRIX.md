# 09 — Requirements Traceability Matrix

**Document ID:** BERUNDA-PH1-RTM-001
**Version:** 1.0 | **Status:** APPROVED — Authoritative Phase 1 traceability baseline
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This matrix connects every problem to its goal, persona, journey, use case, feature, requirement, acceptance criteria, data dependency, security requirement, demo step, and test type.
> Gaps are flagged explicitly. No unexplained P0 gap is permitted.

---

## Reading Guide

Each row traces one functional thread from root problem to verification.
Columns to the right of "Status" indicate gap or coverage status for that thread.

**Status Values:**
- ✅ COVERED — all cells in the row are non-empty and consistent
- ⚠ PARTIAL — one or more cells are missing but the gap is documented
- ❌ GAP — a P0 thread has an unexplained gap

---

## Part A — Core Traceability Matrix

| Problem ID | Goal ID | Persona | Journey | Use Case | Feature ID | Requirement ID | Acceptance Criteria | Data Dependency | Security Req | Demo Step | Test Type | Status |
|-----------|---------|---------|---------|---------|-----------|---------------|--------------------|-----------------|-----------|-----------|-----------|----|
| 3.1 (Unstructured FIR) | GOAL-001 | PERSONA-001 Ananya | JOURNEY-001 | UC-002 | FEAT-010 | FR-FIR-001 | AC-FIR-001, AC-FIR-002, AC-FIR-003, AC-FIR-004 | CaseMaster | FR-AUTH-003, FR-AUTH-004 | DEMO-STEP-02 | Integration | ✅ COVERED |
| 3.1 (Unstructured FIR) | GOAL-001 | PERSONA-001 Ananya | JOURNEY-001 | UC-003 | FEAT-011 | FR-FIR-003 | AC-FIR-005, AC-FIR-006, AC-FIR-007 | EvidenceMaster, Stratus | FR-AUTH-003, NFR-INT-002 | DEMO-STEP-02 | Integration | ✅ COVERED |
| 3.1 (Unstructured FIR) | GOAL-001 | PERSONA-001 Ananya | JOURNEY-001 | UC-004 | FEAT-020 | FR-AI-001 | AC-AI-001, AC-FIR-008 | BriefFacts, extraction queue | NFR-AI-002, NFR-AI-001 | DEMO-STEP-02, 03 | Integration | ✅ COVERED |
| 3.2 (Manual data entry errors) | GOAL-001 | PERSONA-001 Ananya | JOURNEY-001 | UC-004 | FEAT-021 | FR-AI-003, FR-AI-004 | AC-AI-002, AC-AI-003, AC-AI-004, AC-FIR-008 | Extraction queue | NFR-AI-002 | DEMO-STEP-03 | Integration | ✅ COVERED |
| 3.2 (Manual data entry errors) | GOAL-001 | PERSONA-001 Ananya | JOURNEY-001 | UC-004 | FEAT-055 | FR-AI-002 | AC-AI-001 (confidence display) | Extraction metadata | NFR-AI-001 | DEMO-STEP-03 | UI | ✅ COVERED |
| 3.3 (Slow case retrieval) | GOAL-001 | PERSONA-001 Ananya | JOURNEY-001 | UC-005 | FEAT-014 | FR-SRCH-001 | (See search ACs — AC-AUTH-007) | PersonEntity, CaseMaster, VehicleLink | FR-AUTH-003, FR-AUTH-004 | DEMO-STEP-04, 05 | Integration | ✅ COVERED |
| 3.4 (Fragmented relationships) | GOAL-002 | PERSONA-001 Ananya | JOURNEY-001 | UC-007 | FEAT-022 | FR-AI-005 | AC-AI-005 | PersonEntity, PersonEntityLink | FR-AUTH-004, NFR-AI-003 | DEMO-STEP-04 | Integration | ✅ COVERED |
| 3.4 (Fragmented relationships) | GOAL-002 | PERSONA-001 Ananya | JOURNEY-001 | UC-007 | FEAT-023 | FR-AI-006 | AC-AI-006, AC-AI-007, AC-AI-008 | PersonEntity | FR-AUTH-003, FR-AUTH-004 | DEMO-STEP-04 | Integration | ✅ COVERED |
| 3.4 (Fragmented relationships) | GOAL-003 | PERSONA-001 Ananya | JOURNEY-001 | UC-008 | FEAT-030 | FR-AI-008 | AC-GRAPH-001 | RelationshipEdge | FR-AUTH-004 | DEMO-STEP-05 | UI + Integration | ✅ COVERED |
| 3.5 (Recurring entities invisible) | GOAL-002 | PERSONA-001 Ananya | JOURNEY-001 | UC-007 | FEAT-024 | FR-AI-007 | AC-AI-006 (linked cases) | PersonEntity | FR-AUTH-004 | DEMO-STEP-05 | Integration | ✅ COVERED |
| 3.5 (Recurring entities invisible) | GOAL-003 | PERSONA-001 Ananya | JOURNEY-001 | UC-008 | FEAT-031 | FR-AI-009 | AC-GRAPH-002, AC-GRAPH-003 | RelationshipEdge | FR-AUTH-004 | DEMO-STEP-06 | Integration | ✅ COVERED |
| 3.7 (No supervisor visibility) | GOAL-004 | PERSONA-002 Ramesh, PERSONA-003 Priya | JOURNEY-002 | UC-009 | FEAT-040, FEAT-041, FEAT-042 | FR-RPT-001, FR-RPT-002, FR-RPT-003 | AC-MAP-001, AC-MAP-002, AC-MAP-003, AC-MAP-004 | HotspotLayer, CaseMaster | FR-AUTH-003, FR-AUTH-004 | DEMO-STEP-07, 08 | UI + Integration | ✅ COVERED |
| 3.7 (No supervisor visibility) | GOAL-006 | PERSONA-002 Ramesh, PERSONA-003 Priya | JOURNEY-002 | UC-011 | FEAT-043 | FR-RPT-004 | AC-MAP-001 (anomaly badge) | AnomalyAlert | FR-AUTH-004 | DEMO-STEP-07, 08 | Integration | ✅ COVERED |
| 3.8 (Auditability) | GOAL-008 | PERSONA-004 Krishnamurthy | JOURNEY-003 | UC-014 | FEAT-004, FEAT-080 | FR-AUD-001, FR-AUD-002 | AC-AUD-001, AC-AUD-002, AC-AUD-003 | gov_AuditLog | NFR-AUT-001, NFR-AUT-002 | DEMO-STEP-14 | Integration | ✅ COVERED |
| 3.8 (Auditability) | GOAL-008 | PERSONA-004 Krishnamurthy | JOURNEY-003 | UC-013 | FEAT-062, FEAT-063 | FR-AI-015, FR-AI-016 | AC-FAIR-001, AC-FAIR-002, AC-FAIR-003 | gov_FairnessCheckResult | NFR-AI-003 | DEMO-STEP-13 | Integration + UI | ✅ COVERED |
| 3.9 (Decision support limitations) | GOAL-005 | PERSONA-001 Ananya, PERSONA-003 Priya | JOURNEY-001, 002 | UC-010 | FEAT-060, FEAT-061 | FR-AI-013, FR-AI-014 | AC-RISK-001, AC-RISK-002, AC-RISK-003 | PersonEntity, prior cases | NFR-AI-003, FR-AUTH-005 | DEMO-STEP-09 | Integration + UI | ✅ COVERED |
| 3.9 (Decision support limitations) | GOAL-007 | PERSONA-001 Ananya, PERSONA-003 Priya | JOURNEY-001, 002 | UC-012 | FEAT-050, FEAT-054, FEAT-056 | FR-AI-010, FR-AI-011, FR-AI-012 | AC-RAG-001, AC-RAG-002, AC-RAG-003, AC-RAG-004, AC-RAG-005 | RAG corpus | FR-AUTH-004, NFR-AI-004, NFR-AI-006 | DEMO-STEP-10, 11, 12 | Integration | ✅ COVERED |
| Root causes — unauthorized access | GOAL-008 | All users | All journeys | UC-001 | FEAT-001, FEAT-002, FEAT-003, FEAT-005 | FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-004 | AC-AUTH-001 through AC-AUTH-008 | User table | NFR-SEC-001, NFR-SEC-002, NFR-SEC-003 | DEMO-STEP-01, 15 | Integration | ✅ COVERED |
| Root causes — protected-field exposure | GOAL-008 | COMPLIANCE | JOURNEY-003 | UC-013 | FEAT-064 | FR-AUTH-005 | AC-AUTH-008, AC-AUTH-009, AC-RAG-003 | Accused, Victim, Complainant | ADR-007, DEC-018 | DEMO-STEP-12, 13 | Integration | ✅ COVERED |
| Demo execution | — | PERSONA-005 Admin | Setup | UC-015 | FEAT-081, FEAT-091, FEAT-092 | FR-AUTH-006 | AC-USER-001, AC-USER-002, AC-SEED-001 | User table, all entity tables | NFR-DEP-001, NFR-DEP-002 | Demo setup (pre-demo) | Integration | ✅ COVERED |

---

## Part B — Orphan Detection

### B1 — Features Without Requirements

| FEAT-ID | Name | Gap Explanation |
|---------|------|----------------|
| FEAT-007 | Health endpoint | Covered by NFR-OBS-001; functional requirement omitted intentionally (trivially simple implementation) |
| FEAT-012 | CrimeNo auto-generation | Covered by FR-FIR-002; cross-reference confirmed |
| FEAT-016 | Edit draft FIR | P1 — no dedicated FR; covered implicitly by FR-FIR-001 (update before status change). FR to be added in Phase 2 detailed requirements if needed. |
| FEAT-017 | Assign investigating officer | P1 — no dedicated FR in Phase 1; a basic assignment field is part of FR-FIR-001 data model. Formal assignment workflow is Phase 2. |
| FEAT-025 | Vehicle entity tracking | Covered by FR-AI-001 (NER extraction includes vehicle registration) and FR-AI-007 (PersonEntity includes vehicle links). No standalone FR added because the vehicle capability is embedded in the entity extraction and graph features. |
| FEAT-026 | Location entity extraction | Same as FEAT-025 — covered by FR-AI-001. Geocoding is an implementation detail. |
| FEAT-090 | Catalyst Functions deployment | Covered by NFR-DEP-001; no FR required — it is a deployment constraint |
| FEAT-091 | Catalyst Data Store schema deployment | Covered by NFR-DEP-001 |
| FEAT-092 | Synthetic seed data | Covered by NFR-REL-002 and AC-SEED-001 |
| FEAT-093 | CI/CD pipeline | Covered by NFR-DEP-001; no FR required |

**No P0 features are orphaned.**

---

### B2 — Requirements Without Goals

| Requirement ID | Analysis |
|---------------|---------|
| FR-FIR-004 (Status lifecycle) | Covered by GOAL-001 (AI-assisted capture) — status lifecycle enables the FIR workflow goal. Not missing a goal; traceability to GOAL-001 is confirmed. |
| FR-FIR-005 (FIR detail view) | Covered by GOAL-001 and GOAL-003 (investigation use). Confirmed. |
| FR-AUTH-006 (User management) | Enables all goals by allowing role provisioning. Administrative prerequisite. Not missing a goal. |

**No requirements are orphaned.**

---

### B3 — Goals Without Features

| Goal ID | Goal Name | Status |
|---------|-----------|--------|
| GOAL-001 | AI-assisted FIR capture | ✅ Covered: FEAT-010, 011, 020, 021 |
| GOAL-002 | Cross-case entity resolution | ✅ Covered: FEAT-022, 023, 024 |
| GOAL-003 | Relationship graph | ✅ Covered: FEAT-030, 031 |
| GOAL-004 | Geospatial hotspot | ✅ Covered: FEAT-040, 041, 042 |
| GOAL-005 | Explainable risk scoring | ✅ Covered: FEAT-060, 061 |
| GOAL-006 | Anomaly detection | ✅ Covered: FEAT-043 |
| GOAL-007 | RAG investigation query | ✅ Covered: FEAT-050, 054, 056 |
| GOAL-008 | Role-based access and audit | ✅ Covered: FEAT-001, 002, 003, 004, 062, 063, 064, 080 |

**No goals are without features.**

---

### B4 — Features Without Users

All P0 features have an identified actor in the use cases or in FR definitions. No P0 feature is user-less.

---

### B5 — Features Without Acceptance Criteria

| FEAT-ID | Feature | Coverage |
|---------|---------|---------|
| FEAT-010 | Create FIR | ✅ AC-FIR-001 through AC-FIR-004 |
| FEAT-011 | Upload FIR document | ✅ AC-FIR-005 through AC-FIR-008 |
| FEAT-020 | NER extraction | ✅ AC-AI-001 |
| FEAT-021 | Human review | ✅ AC-AI-002, AC-AI-003, AC-AI-004 |
| FEAT-022 | Entity resolution | ✅ AC-AI-005 |
| FEAT-023 | Merge review UI | ✅ AC-AI-006, AC-AI-007, AC-AI-008 |
| FEAT-024 | PersonEntity profile | ✅ AC-AI-006 (linked cases) |
| FEAT-030 | Relationship graph | ✅ AC-GRAPH-001 |
| FEAT-031 | Hidden-link BFS | ✅ AC-GRAPH-002, AC-GRAPH-003 |
| FEAT-040–042 | Hotspot map and filters | ✅ AC-MAP-001 through AC-MAP-004 |
| FEAT-043 | Anomaly detection | ✅ AC-MAP-001 (anomaly badge) |
| FEAT-050 | RAG query | ✅ AC-RAG-001 through AC-RAG-005 |
| FEAT-054 | RAG citation | ✅ AC-RAG-001 (citation required) |
| FEAT-055 | AI confidence display | ✅ AC-AI-001 (confidence visible) |
| FEAT-056 | MockProvider | ✅ AC-RAG-005 |
| FEAT-060 | Risk scoring | ✅ AC-RISK-001, AC-RISK-002, AC-RISK-003 |
| FEAT-061 | Feature importance | ✅ AC-RISK-001 (feature importance bar chart) |
| FEAT-062 | Fairness check | ✅ AC-FAIR-001, AC-FAIR-003 |
| FEAT-063 | Fairness dashboard | ✅ AC-FAIR-001, AC-FAIR-002 |
| FEAT-064 | Protected-field access control | ✅ AC-AUTH-008, AC-AUTH-009 |
| FEAT-001–005 | Auth features | ✅ AC-AUTH-001 through AC-AUTH-007 |
| FEAT-080 | Audit log view | ✅ AC-AUD-001, AC-AUD-002, AC-AUD-003 |
| FEAT-081 | User management | ✅ AC-USER-001, AC-USER-002 |
| FEAT-091–092 | Seed data and schema | ✅ AC-SEED-001 |

**All P0 features have acceptance criteria.**

---

### B6 — Demo Steps Without Requirements

| Demo Step | Requirements Demonstrated | Gap |
|-----------|--------------------------|-----|
| DEMO-STEP-01 | FR-AUTH-001, FR-AUTH-003, FR-AUTH-004, NFR-PRV-003 | None |
| DEMO-STEP-02 | FR-FIR-001, FR-FIR-002, FR-FIR-003, FR-AI-001, FR-AUD-001 | None |
| DEMO-STEP-03 | FR-AI-002, FR-AI-003, FR-AI-004, NFR-AI-001, NFR-AI-002 | None |
| DEMO-STEP-04 | FR-AI-005, FR-AI-006, FR-AI-007 | None |
| DEMO-STEP-05 | FR-AI-007, FR-AI-008 | None |
| DEMO-STEP-06 | FR-AI-009 | None |
| DEMO-STEP-07 | FR-RPT-001, FR-RPT-002, FR-RPT-003, FR-RPT-004 | None |
| DEMO-STEP-08 | FR-RPT-002, FR-RPT-003 | None |
| DEMO-STEP-09 | FR-AI-013, FR-AI-014, FR-AI-015 | None |
| DEMO-STEP-10 | FR-AI-010, FR-AI-012 | None |
| DEMO-STEP-11 | FR-AI-010, FR-AI-012 | None |
| DEMO-STEP-12 | FR-AUTH-005, FR-AI-010 | None |
| DEMO-STEP-13 | FR-AI-015, FR-AI-016 | None |
| DEMO-STEP-14 | FR-AUD-001, FR-AUD-002 | None |
| DEMO-STEP-15 | FR-AUTH-003 | None |

**No demo steps are without requirements.**

---

### B7 — AI Features Without Review Gates

| AI Feature | Human Review Gate | Status |
|-----------|------------------|--------|
| NER extraction (FEAT-020) | FR-AI-003 — officer must approve each entity | ✅ Gate present |
| Entity resolution merge (FEAT-022) | FR-AI-006 — officer must approve or reject merge | ✅ Gate present |
| Risk scoring (FEAT-060) | FR-AI-015 — fairness check must pass before scoring runs | ✅ Gate present |
| RAG answer (FEAT-050) | Disclaimer on every answer; no auto-action taken | ✅ Gate present (advisory-only output) |
| FIR summarisation (FEAT-051) | P1 feature — must be labelled AI suggestion; no auto-save | ✅ Gate documented in NFR-AI-001 |
| Related-case recommendation (FEAT-053) | P1 feature — recommendations are advisory only | ✅ Gate documented in NFR-AI-001 |

**No AI feature is without a review gate.**

---

### B8 — Sensitive Actions Without Audit Requirements

| Sensitive Action | Audit Requirement | Status |
|-----------------|------------------|--------|
| User login / failure | FR-AUD-001 (`AUTH.LOGIN`, `AUTH.LOGIN_FAILURE`) | ✅ |
| FIR create | FR-AUD-001 (`FIR.CREATE`) | ✅ |
| FIR upload | FR-AUD-001 (`FIR.UPLOAD`) | ✅ |
| AI extraction viewed | FR-AUD-001 (`AI.EXTRACTION.VIEW`) | ✅ |
| AI extraction approved | FR-AUD-001 (`AI.EXTRACTION.APPROVE`) | ✅ |
| Entity merge approved | FR-AUD-001 (`ENTITY.MERGE.APPROVE`) | ✅ |
| Person record read | FR-AUD-001 (`PERSON.READ`) | ✅ |
| Risk score viewed | FR-AUD-001 (`RISK.VIEW`) | ✅ |
| RAG query | FR-AUD-001 (`RAG.QUERY`) | ✅ |
| Restricted field access | FR-AUD-001 (`RESTRICTED.FIELD.ACCESS`) | ✅ |
| Fairness check run | FR-AI-015 (`FAIRNESS.CHECK.RUN`) | ✅ |
| User created / role changed | FR-AUTH-006 (`ADMIN.USER.CREATE`, `ADMIN.ROLE.CHANGE`) | ✅ |
| Audit log viewed | Not audited (to prevent infinite recursion) | ✅ Intentional |

**No sensitive action is missing an audit requirement.**

---

### B9 — Requirements Outside Frozen Scope

The following requirements are documented in Phase 1 but trace to P2 or P3 features. They are retained for completeness but must not be implemented in the MVP.

| Requirement | Feature | Priority | Action |
|------------|---------|---------|--------|
| Investigation notes API | FEAT-070 | P2 STRETCH | Implement only after all P0 complete |
| Evidence metadata hash verification on download | NFR-INT-002 | P1 PROPOSED | Implement after P0 if time allows |
| Statutory report generation | FEAT-082 | P2 STRETCH | Implement only after all P0 complete |
| Kannada NER | FEAT-057 | P3 DEFERRED | Do not implement |

---

## Part C — Cross-Reference Index

### ID Prefix Registry

| Prefix | Document | Examples |
|--------|---------|---------|
| Problem 3.x | 01-PROBLEM-STATEMENT-AND-VISION.md §3 | 3.1, 3.4, 3.7 |
| GOAL-xxx | 01-PROBLEM-STATEMENT-AND-VISION.md §9 | GOAL-001 through GOAL-008 |
| PERSONA-xxx | 02-STAKEHOLDERS-AND-USER-ROLES.md §5 | PERSONA-001 through PERSONA-005 |
| JOURNEY-xxx | 03-USER-JOURNEYS-AND-USE-CASES.md §2 | JOURNEY-001, JOURNEY-002, JOURNEY-003 |
| UC-xxx | 03-USER-JOURNEYS-AND-USE-CASES.md §3 | UC-001 through UC-020 |
| FEAT-xxx | 04-MVP-SCOPE-AND-PRIORITIZATION.md §3 | FEAT-001 through FEAT-093 |
| FR-xxx | 05-FUNCTIONAL-REQUIREMENTS.md | FR-AUTH-001, FR-FIR-001, FR-AI-001, etc. |
| NFR-xxx | 06-NON-FUNCTIONAL-REQUIREMENTS.md | NFR-SEC-001, NFR-PERF-001, etc. |
| AC-xxx | 07-ACCEPTANCE-CRITERIA.md | AC-AUTH-001, AC-FIR-001, etc. |
| DEMO-STEP-xx | 08-DEMO-STORY-AND-SUCCESS-METRICS.md | DEMO-STEP-01 through DEMO-STEP-15 |
| ASM-xxx | 10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md | ASM-001 through ASM-012 |
| RSK-xxx | 10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md | RSK-001 through RSK-010 |
| OQ-xxx | 10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md | OQ-001 through OQ-010 |
| DEC-xxx | 10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md | DEC-001 through DEC-018 |
| DEMO-Txx | 03-USER-JOURNEYS-AND-USE-CASES.md §6 | DEMO-T01 through DEMO-T15 |

---

### SRS-to-Phase1 FR Cross-Reference Mapping

This table maps each SRS FR-ID (from `SOFTWARE_REQUIREMENTS_SPECIFICATION.md`) to the equivalent Phase 1 FR-ID. Gaps indicate requirements deferred to Phase 2 or 3.

| SRS FR-ID | SRS Name | Phase 1 FR-ID | Phase 1 Name | Status |
|-----------|----------|---------------|--------------|--------|
| FR-001 | FIR Structured Import | Not in Phase 1 P0 scope | — | Phase 2 (batch import) |
| FR-002 | FIR Manual Entry | FR-FIR-001 | Manual FIR Creation | ✅ Equivalent |
| FR-003 | Data Validation | FR-FIR-001 (embedded) | Manual FIR Creation | ✅ Covered |
| FR-004 | Duplicate Detection | FR-FIR-002 | CrimeNo Auto-Generation | ⚠ Partial |
| FR-005 | English NER | FR-AI-001 | NER Extraction | ✅ Equivalent |
| FR-006 | Kannada NER | FEAT-057 | Kannada NER | Deferred to Phase 2 |
| FR-007 | Confidence Scoring | FR-AI-002 | AI Confidence Score Display | ✅ Equivalent |
| FR-008 | Entity Linking | FR-AI-005 | Cross-Case Entity Resolution | ✅ Equivalent |
| FR-009 | PersonEntity Identity | FR-AI-007 | PersonEntity Canonical Profile | ✅ Equivalent |
| FR-010 | Blocking Strategy | (Implementation detail) | — | ✅ Covered by FR-AI-005 |
| FR-011 | Similarity Scoring | (Implementation detail) | — | ✅ Covered by FR-AI-005 |
| FR-012 | Match Thresholds | (Implementation detail) | — | ✅ Covered by AC-AI-005 |
| FR-013 | Manual Review | FR-AI-006 | Entity Resolution Merge Review | ✅ Equivalent |
| FR-014 | Merge Approval | FR-AI-006 | Entity Resolution Merge Review | ✅ Equivalent |
| FR-015 | Provenance Tracking | FR-AUD-001 | Audit Trail | ✅ Equivalent |
| FR-016 | RelationshipEdge Table | FR-AI-008 | Relationship Graph Rendering | ✅ Equivalent |
| FR-017 | Graph Traversal | FR-AI-009 | Hidden-Link Discovery | ✅ Equivalent |
| FR-018 | Graph Visualization | FR-AI-008 (embedded) | Relationship Graph Rendering | ✅ Covered |
| FR-019 | Vehicle Linking | FR-AI-001 (embedded) | NER Extraction | ✅ Covered |
| FR-020 | MO Pattern Matching | FEAT-072 | MO Pattern | P2 STRETCH |
| FR-021 | Hotspot Map | FR-RPT-001 | Geospatial Hotspot Rendering | ✅ Equivalent |
| FR-022 | District Drill-Down | FR-RPT-002 | District and Station Drill-Down | ✅ Equivalent |
| FR-023 | Temporal Filter | FR-RPT-003 | Temporal and Crime-Type Filtering | ✅ Equivalent |
| FR-024 | Anomaly Detection | FR-RPT-004 | Anomaly/Spike Detection | ✅ Equivalent |
| FR-025 | Anomaly Alert | FR-RPT-004 (embedded) | Anomaly/Spike Detection | ✅ Covered |
| FR-026 | Risk Score Computation | FR-AI-013 | Explainable Risk Scoring | ✅ Equivalent |
| FR-027 | Feature Importance | FR-AI-014 | Feature Importance Display | ✅ Equivalent |
| FR-028 | Feature Exclusion | FR-AI-015 | Fairness Verification Check | ✅ Equivalent |
| FR-029 | Score Explainability | FR-AI-013 (embedded) | Explainable Risk Scoring | ✅ Covered |
| FR-030 | RAG Query | FR-AI-010 | RAG Natural-Language Query | ✅ Equivalent |
| FR-031 | Source Citations | FR-AI-012 | RAG Answer Source Citation | ✅ Equivalent |
| FR-032 | Role-Based Filtering | FR-AUTH-004, NFR-AI-006 | Jurisdiction-Scoped RAG | ✅ Equivalent |
| FR-033 | Insufficient Evidence Response | AC-RAG-002 (embedded) | — | ✅ Covered by AC |
| FR-034 | Query Audit | FR-AUD-001 (`RAG.QUERY`) | Audit Trail | ✅ Equivalent |
| FR-035 | User Authentication | FR-AUTH-001 | User Authentication | ✅ Equivalent |
| FR-036 | Role-Based Access | FR-AUTH-003 | Role-Based Authorization | ✅ Equivalent |
| FR-037 | Jurisdiction Scoping | FR-AUTH-004 | Jurisdiction Scoping | ✅ Equivalent |
| FR-038 | MFA Support | FR-AUTH-002 | Multi-Factor Authentication | ✅ Equivalent |
| FR-039 | Person-Level Read Audit | FR-AUD-001 (`PERSON.READ`) | Audit Trail | ✅ Equivalent |
| FR-040 | AI Output Audit | FR-AUD-001 (`AI.*`, `GRAPH.*`) | Audit Trail | ✅ Equivalent |
| FR-041 | Append-Only Log | NFR-SEC-003 | Append-Only Audit Log | ✅ Equivalent |
| FR-042 | Audit Queryability | FR-AUD-002 | Audit Log Query and Search | ✅ Equivalent |
| FR-043 | Fairness Check | FR-AI-015 | Fairness Verification Check | ✅ Equivalent |
| FR-044 | Role Restriction Check | FR-AI-015 (embedded) | Fairness Verification Check | ✅ Covered |
| FR-045 | Fairness Dashboard | FR-AI-016 | Fairness Dashboard | ✅ Equivalent |
| FR-046 | Synthetic Data Generation | FR-SEED-001 | Synthetic Data Generation | ✅ Equivalent |
| FR-047 | Planted Patterns | AC-SEED-001 | Planted Patterns Verified | ✅ Covered by AC |
| FR-048 | Seeded Reproducibility | FR-SEED-002 | Deterministic Seeding | ✅ Equivalent |
| FR-049 | Synthetic Labeling | NFR-SEC-006 | Synthetic Data Labelling | ✅ Equivalent |

---

## Part D — Traceability Health Check

| Check | Result | Evidence |
|-------|--------|---------|
| Every P0 feature has ≥ 1 functional requirement | ✅ PASS | Part B5 — all 37 P0 features confirmed covered |
| Every P0 requirement has acceptance criteria | ✅ PASS | Part B5 — all P0 requirements have AC entries |
| Every requirement has a verification method | ✅ PASS | FR documents include verification method field for each requirement |
| Requirements do not prescribe unnecessary implementation details | ✅ PASS | No FR specifies a UI component library, database table column name, or programming construct beyond what is architecturally required |
| Authorization is enforced by requirements | ✅ PASS | Every FR includes Authorization field or references FR-AUTH-003/004; FR-AUTH-005 covers field-level access |
| Audit requirements exist for all sensitive actions | ✅ PASS | Part B8 — 13 sensitive action categories covered |
| AI requirements include human review | ✅ PASS | Part B7 — all AI features have review gates |
| Synthetic data clearly separated from production | ✅ PASS | NFR-SEC-006, NFR-PRV-003, NFR-DEP-002 |
| No requirement contradicts approved MVP scope | ✅ PASS | All FRs trace to P0 or P1 features; Part B9 lists deferred requirements |
| Every demo step has requirements | ✅ PASS | Part B6 — 15 of 15 demo steps have requirement references |
| Every goal has features | ✅ PASS | Part B3 — 8 of 8 goals covered |
| No unexplained P0 gap | ✅ PASS | All P0 gaps in Part B1 are explained and non-blocking |

**Overall traceability health: PASS — 12/12 checks satisfied.**

---

*End of 09-REQUIREMENTS-TRACEABILITY-MATRIX.md*
