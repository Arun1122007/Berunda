# 04 — MVP Scope and Feature Prioritization

**Document ID:** BERUNDA-PH1-SCOPE-001
**Version:** 1.0 | **Status:** FROZEN — Scope baseline for hackathon MVP
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This document freezes the Berunda hackathon MVP scope.
> No feature may be added to the MVP after this document is approved without completing the change-request process in Section 16.
> Every feature in the build must trace to a row in the feature inventory.

---

## 1. Executive Scope Summary

Project Berunda's hackathon submission must demonstrate, within an 11-day window and by a 2-person team on Zoho Catalyst, that a structured information extraction and investigation-support layer can turn isolated FIR records into a connected, explainable, and auditable intelligence layer.

**The MVP is not a full police management system.** It is a focused demonstration of five capabilities:

1. AI-assisted structured FIR capture with human review
2. Cross-case entity resolution with officer approval
3. Visual relationship graph and hidden-link discovery
4. Jurisdiction-level analytics (hotspot map + anomaly alerts)
5. Natural-language investigation assistance (RAG)

Supported by: role-based access, audit logging, and a fairness verification dashboard.

**Scope discipline is the primary delivery risk.** The demo must run end-to-end without manual patches on Day 11. Demo stability is a higher priority than feature count.

### Scope Boundary Statement

| In Scope | Out of Scope |
|----------|-------------|
| AI-assisted FIR creation and entity extraction | Full police workflow management (charge sheets, court submissions) |
| Entity resolution (English, rule-based) | Kannada NER |
| Relationship graph (NetworkX, in-memory) | Neo4j, distributed graph |
| Geospatial hotspot map (Karnataka, synthetic data) | Real-time CCTNS data feed |
| Explainable risk scoring (scikit-learn) | External ML platforms beyond Catalyst QuickML / local scikit-learn |
| Anomaly detection (z-score, synthetic baseline) | Predictive patrol deployment |
| RAG investigation assistant (OpenAI / Groq / Mock) | Autonomous AI decisions |
| Role-based access (4 roles) | Citizen portal, judicial access |
| Audit logging (append-only) | Blockchain audit |
| Fairness verification dashboard | Real CCTNS integration |

---

## 2. MVP Definition

The Berunda hackathon MVP is complete when:

1. A demo user can log in under each of the 4 roles
2. An FIR can be created manually or by uploading a document
3. AI entity extraction is presented for officer review and saved after approval
4. At least one planted repeat-offender is surfaced via entity resolution
5. The relationship graph shows cross-case connections including a hidden link
6. The hotspot map renders with the planted anomaly badge visible
7. A risk score with feature-importance breakdown is visible for a high-risk person
8. Ask Berunda answers 3 rehearsed questions with cited grounding
9. The fairness dashboard confirms CasteID/ReligionID exclusion programmatically
10. The audit log shows all actions from the demo walkthrough

The demo must run live (or via pre-recorded video as fallback) without manual data patches.

---

## 3. Feature Inventory

### Group A — Platform Foundation

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-001 | User authentication (JWT) | Unauthorized access to sensitive case data | All | ADR-009, SRS FR-001 | APPROVED | Very High | High | Low | None | None | High | Catalyst Auth | Yes | MUST / P0 | IN MVP |
| FEAT-002 | Role-based access control (4 roles) | Overprivileged access; protected-field exposure | All | ADR-007, ACCESS_CONTROL_MATRIX.md | APPROVED | Very High | High | Low-Medium | User table | None | Very High | None (app-layer) | Yes | MUST / P0 | IN MVP |
| FEAT-003 | Jurisdiction scoping (DistrictID filter) | Cross-station data leakage | INVESTIGATOR | ADR-002, ASSUMPTIONS.md A2 | APPROVED | High | Medium | Low | CaseMaster.DistrictRef | None | High | None | Yes | MUST / P0 | IN MVP |
| FEAT-004 | Audit logging (append-only) | Untraceability; accountability gap | All | ADR-006, AUDIT_LOGGING spec | APPROVED | Very High | High | Low | gov_AuditLog | None | Very High | Data Store | Yes | MUST / P0 | IN MVP |
| FEAT-005 | Session management and JWT expiry | Session hijacking; stale sessions | All | SRS NFR-001 | APPROVED | High | Low | Low | None | None | High | None | Yes | MUST / P0 | IN MVP |
| FEAT-006 | Error handling and graceful degradation | AI service unavailability causing demo failure | All | SRS NFR | APPROVED | High | Medium | Low | None | None | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-007 | Health and readiness endpoints | Deployment verification | ADMIN | src/main.py | APPROVED | Medium | Low | Very Low | None | None | Low | Catalyst Functions | No | SHOULD / P1 | IN MVP |

### Group B — FIR Management

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-010 | Create FIR manually (form entry) | Unstructured paper-based FIR; no digital entry | INVESTIGATOR | SRS FR-002, PRD F-001 | APPROVED | Very High | High | Medium | CaseMaster schema | None | Medium | Data Store | Yes | MUST / P0 | IN MVP |
| FEAT-011 | Upload FIR document (PDF/image) | Manual re-entry of submitted documents | INVESTIGATOR | SRS FR-003, PRD F-001 | APPROVED | High | High | Medium | EvidenceMaster, Stratus | OCR + NER | Medium | Catalyst Stratus | Yes | MUST / P0 | IN MVP |
| FEAT-012 | CrimeNo auto-generation (district-year-station-seq) | Manual CrimeNo entry causes duplicates and errors | INVESTIGATOR | SRS FR-004 | APPROVED | High | Low | Low | CaseMaster | None | Low | Data Store | Yes | MUST / P0 | IN MVP |
| FEAT-013 | View FIR detail (multi-tab) | Officers lack structured case overview | INVESTIGATOR, SCRB_ANALYST | UC-006 | APPROVED | High | High | Low | All FIR-related tables | None | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-014 | Search FIR, person, vehicle (global search) | Hours spent manually cross-referencing | INVESTIGATOR, SCRB_ANALYST | UC-005, SRS FR-005 | APPROVED | Very High | High | Medium | PersonEntity, CaseMaster, VehicleLink | None | Low | Data Store | Yes | MUST / P0 | IN MVP |
| FEAT-015 | FIR status lifecycle (REGISTERED → EXTRACTION_APPROVED → UNDER_INVESTIGATION) | No structured case status tracking | All | SRS, CANONICAL_DATA_MODEL | APPROVED | High | Medium | Low | CaseMaster.Status | None | Low | Data Store | Yes | MUST / P0 | IN MVP |
| FEAT-016 | Edit draft FIR (before approval) | Officers make mistakes during data entry | INVESTIGATOR | SRS FR | APPROVED | Medium | Low | Low | CaseMaster | None | Low | Data Store | No | SHOULD / P1 | IN MVP |
| FEAT-017 | Assign investigating officer | No formal case-officer assignment | SHO, ADMIN | UC-002, SRS | APPROVED | High | Low | Low | CaseMaster.IORef | None | Low | Data Store | No | SHOULD / P1 | IN MVP (basic) |

### Group C — Entity and Person Management

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-020 | NER entity extraction from BriefFacts | Unstructured FIR narrative; manual extraction | INVESTIGATOR | SRS FR-004, PRD F-002, ADR-005 | APPROVED | Very High | Very High | High | Accused, Victim, VehicleLink | spaCy NER | Medium | None (Python) | Yes | MUST / P0 | IN MVP |
| FEAT-021 | Human review and correction of AI extraction | AI errors become official record without correction | INVESTIGATOR | UC-004, ADR-006 | APPROVED | Very High | Very High | Medium | AI extraction queue | NER provider | High | None | Yes | MUST / P0 | IN MVP |
| FEAT-022 | Cross-case entity resolution (person matching) | Same person as multiple records; repeat offender invisible | INVESTIGATOR | SRS FR-007, PRD F-003, ADR-005 | APPROVED | Very High | Very High | High | PersonEntity, PersonEntityLink | Rule-based engine | High | None | Yes | MUST / P0 | IN MVP |
| FEAT-023 | Entity resolution merge review UI | Automated merges silently corrupt data | INVESTIGATOR | UC-007 | APPROVED | Very High | Very High | Medium | PersonEntity | None | High | None | Yes | MUST / P0 | IN MVP |
| FEAT-024 | PersonEntity canonical profile view | No unified person view across cases | INVESTIGATOR, SCRB_ANALYST | UC-007 | APPROVED | High | High | Low | PersonEntity, RelationshipEdge | None | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-025 | Vehicle entity tracking (cross-case) | Vehicles appear in multiple cases without linkage | INVESTIGATOR | SRS, VehicleLink schema | APPROVED | High | Medium | Low | VehicleLink | Optional NER | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-026 | Location entity extraction | Locations not structured; hotspot map depends on coords | INVESTIGATOR, SCRB_ANALYST | SRS, HotspotLayer | APPROVED | High | Medium | Medium | OccurrencePlace schema | NER + geocoding | Low | None | Yes | SHOULD / P1 | IN MVP |

### Group D — Graph and Link Analysis

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-030 | Relationship graph visualisation (Cytoscape.js) | Hidden connections invisible in flat records | INVESTIGATOR, SCRB_ANALYST | PRD F-004, ADR-004 | APPROVED | Very High | Very High | High | RelationshipEdge, PersonEntity, VehicleLink | None | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-031 | Hidden-link discovery (shortest-path BFS) | Cross-case connections require manual analysis | INVESTIGATOR | UC-008, ADR-004 | APPROVED | Very High | Very High | Medium | RelationshipEdge | NetworkX BFS | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-032 | Graph node expand (second-degree connections) | Graph too flat for organised crime networks | INVESTIGATOR | UC-008 | APPROVED | High | High | Medium | RelationshipEdge | None | Low | None | No | SHOULD / P1 | IN MVP |
| FEAT-033 | Graph filter by relationship type and date | Large graphs are unreadable without filtering | All | UC-008 | APPROVED | Medium | Medium | Low | RelationshipEdge | None | Low | None | No | COULD / P2 | STRETCH |

### Group E — Analytics and Geospatial

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-040 | Geospatial hotspot heatmap (MapLibre GL) | No real-time crime density view for supervisors | SHO, SCRB_ANALYST | PRD F-005, ANALYTICS_FEATURE_CATALOG | APPROVED | Very High | Very High | Medium | HotspotLayer, OccurrencePlace coords | None | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-041 | District-to-station drill-down | State view hides local patterns | SHO, SCRB_ANALYST | UC-009 | APPROVED | High | High | Low | CaseMaster.PoliceStationRef, DistrictRef | None | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-042 | Crime type and date range filter on map | Undifferentiated crime density is not actionable | SHO, SCRB_ANALYST | UC-009 | APPROVED | High | High | Low | CaseMaster.CrimeHeadRef | None | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-043 | Anomaly detection and alerts (z-score) | Emerging crime spikes missed until reported | SHO, SCRB_ANALYST | PRD F-007, UC-011 | APPROVED | Very High | Very High | Medium | AnomalyAlert table, historical baseline | Statistical | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-044 | Temporal trend charts (crime type over time) | No visual trend analysis for supervisors | SCRB_ANALYST | ANALYTICS_FEATURE_CATALOG | APPROVED | High | Medium | Medium | CaseMaster time series | None | Low | None | No | SHOULD / P1 | IN MVP |
| FEAT-045 | State command dashboard (SCRB view) | No state-wide unified view | SCRB_ANALYST | UC — JOURNEY-002 | APPROVED | Very High | High | Medium | Aggregate queries | None | Low | None | No | SHOULD / P1 | IN MVP |
| FEAT-046 | Crime category breakdown (pie/bar charts) | Manual Excel pivot tables for category analysis | SCRB_ANALYST | ANALYTICS_FEATURE_CATALOG | APPROVED | Medium | Medium | Low | CaseMaster.CrimeHeadRef | None | Low | None | No | SHOULD / P1 | IN MVP |

### Group F — AI Assistance

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-050 | Ask Berunda RAG (natural-language query) | No plain-language query interface for case data | INVESTIGATOR, SCRB_ANALYST | PRD F-008, ADR-006 | APPROVED | Very High | Very High | High | RAG corpus chunks | OpenAI / Groq / Mock | High | QuickML or ext LLM | Yes | MUST / P0 | IN MVP |
| FEAT-051 | FIR summarisation (BriefFacts → structured summary) | Long FIR narratives are time-consuming to read | INVESTIGATOR | AI_ML_SYSTEM_SPECIFICATION | APPROVED | High | High | Medium | BriefFacts text | LLM | Medium | None | No | SHOULD / P1 | IN MVP |
| FEAT-052 | Crime category suggestion (from BriefFacts) | Manual crime head selection is error-prone | INVESTIGATOR | AI_ML_SYSTEM_SPECIFICATION | APPROVED | Medium | Medium | Medium | BriefFacts, CrimeHead table | Classifier | Low | None | No | COULD / P2 | STRETCH |
| FEAT-053 | Related-case recommendations | Investigators miss manually discoverable connections | INVESTIGATOR | AI_ML_SYSTEM_SPECIFICATION | APPROVED | High | High | High | RelationshipEdge, similarity scoring | Embedding or rule | Low | None | No | SHOULD / P1 | IN MVP |
| FEAT-054 | RAG answer source citation | Hallucinated answers damage trust | INVESTIGATOR | ADR-006, UC-012 | APPROVED | Very High | High | Low | RAG chunk metadata | None | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-055 | AI confidence score display | Officer cannot assess reliability of suggestion | INVESTIGATOR | UC-004, ADR-005 | APPROVED | High | High | Low | Extraction metadata | NER confidence | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-056 | MockProvider fallback for AI services | Demo fails if LLM API is unavailable | All | ADR-009, src/ai/ | APPROVED | Very High | High | Low | None | Mock responses | Low | None | Yes | MUST / P0 | IN MVP |
| FEAT-057 | Kannada NER | FIRs written in Kannada are not processed | INVESTIGATOR | PRD F-013, UC-019 | DRAFT | High | Low | Very High | AI4Bharat model | Kannada NLP | Low | None | No | WILL NOT / P3 | DEFERRED (Phase 2) |

### Group G — Risk and Fairness

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-060 | Explainable risk scoring (scikit-learn) | No data-driven investigation prioritisation | INVESTIGATOR, SCRB_ANALYST | PRD F-006, ADR-005 | APPROVED | Very High | Very High | High | PersonEntity, prior cases | scikit-learn | High | QuickML or local | Yes | MUST / P0 | IN MVP |
| FEAT-061 | Feature importance display (top 5 features) | Risk score without explanation is a black box | INVESTIGATOR | UC-010 | APPROVED | Very High | Very High | Low | Model output metadata | SHAP / coeff | High | None | Yes | MUST / P0 | IN MVP |
| FEAT-062 | Fairness verification check (CasteID/ReligionID exclusion) | Protected characteristics used in scoring | COMPLIANCE | PRD F-011, ADR-007 | APPROVED | Very High | Very High | Medium | Model feature registry | None | Very High | None | Yes | MUST / P0 | IN MVP |
| FEAT-063 | Fairness dashboard view | No tool for compliance officers to verify fairness | COMPLIANCE | UC-013 | APPROVED | Very High | Very High | Low | gov_FairnessCheckResult | None | High | None | Yes | MUST / P0 | IN MVP |
| FEAT-064 | Protected-characteristic field access control | CasteRef/ReligionRef accessible beyond Compliance role | COMPLIANCE | ADR-007, CONFLICT-005 | APPROVED | Very High | Medium | Medium | Accused, Victim, Complainant schema | None | Very High | None | Yes | MUST / P0 | IN MVP |

### Group H — Investigation and Evidence

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-070 | Investigation notes (timestamped, per case) | No structured investigation log | INVESTIGATOR | UC-016, SRS | APPROVED | High | Medium | Low | InvestigationNote table | None | Low | None | No | COULD / P2 | STRETCH |
| FEAT-071 | Evidence metadata linking (file hash, chain-of-custody) | No evidence linkage in digital system | INVESTIGATOR | UC-017, PRD F-015 | APPROVED | High | Medium | Medium | EvidenceMaster, Stratus | None | Medium | Catalyst Stratus | No | COULD / P2 | STRETCH |
| FEAT-072 | Case timeline view (ordered event history) | Investigative actions lack chronological view | INVESTIGATOR | UC-006, SRS | APPROVED | High | High | Low | AuditLog + notes + events | None | Low | None | No | SHOULD / P1 | IN MVP (basic) |

### Group I — Governance and Administration

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-080 | Audit log view (searchable, filterable) | Actions not traceable; accountability gap | COMPLIANCE, ADMIN | UC-014 | APPROVED | Very High | High | Low | gov_AuditLog | None | High | Data Store | Yes | MUST / P0 | IN MVP |
| FEAT-081 | User management (create, role assign, unlock) | Admin cannot provision demo users | ADMIN | UC-015 | APPROVED | High | Low | Low | User table | None | High | Catalyst Auth | No | MUST / P0 | IN MVP (also supports pre-seeded demo users) |
| FEAT-082 | Statutory report generation (aggregate counts) | Manual Excel report compilation | SCRB_ANALYST, COMPLIANCE | UC-018, PRD F-017 | DRAFT | High | Low | Medium | Aggregate queries | None | Low | None | No | COULD / P2 | STRETCH |
| FEAT-083 | Data provenance records | Cannot trace where data originated | COMPLIANCE | DATA_GOVERNANCE doc | APPROVED | Medium | Low | Low | gov_DataProvenanceRecord | None | Low | None | No | COULD / P2 | STRETCH |

### Group J — Infrastructure and Deployment

| FEAT-ID | Name | Problem Solved | Target User | Source | Approval Status | Business Value | Demo Value | Eng Complexity | Data Dep | AI Dep | Security Risk | Catalyst Dep | Core Workflow | Priority | Disposition |
|---------|------|----------------|-------------|--------|----------------|---------------|-----------|---------------|---------|--------|--------------|-------------|--------------|---------|-------------|
| FEAT-090 | Catalyst Functions deployment (Node.js) | FastAPI local-only; not demoable on Catalyst | All | ADR-009 | APPROVED | High | Low | High | All | None | Medium | Catalyst Functions | Yes | SHOULD / P1 | IN MVP (FastAPI fallback) |
| FEAT-091 | Catalyst Data Store schema deployment | Schema not deployed; database unavailable | All | CATALYST_DATASTORE_SCHEMA_MAPPING | APPROVED | Very High | Low | Medium | All tables | None | High | Catalyst Data Store | Yes | MUST / P0 | IN MVP |
| FEAT-092 | Synthetic seed data load (planted patterns) | Demo has no data; demo fails | All | SYNTHETIC_DATA_SPECIFICATION | APPROVED | Very High | Very High | Low | All entity tables | None | Low | Data Store | Yes | MUST / P0 | IN MVP |
| FEAT-093 | CI/CD pipeline (GitHub Actions) | Manual deployments are error-prone | Dev | restructuring-report | APPROVED | Medium | Low | Low | None | None | Low | None | No | SHOULD / P1 | IN MVP |

---

## 4. Prioritization Methodology

### MoSCoW + Priority Level Definitions

| MoSCoW | P-Level | Meaning |
|--------|---------|---------|
| Must Have | P0 | Demo fails without this feature. |
| Should Have | P1 | Strongly adds to demo value or engineering correctness. Demo is weaker but not broken without it. |
| Could Have | P2 | Nice to have if time permits after all P0 and P1 items are complete and stable. |
| Will Not Have | P3 | Explicitly deferred. Implementing this in the MVP would be a scope violation. |

### Complexity Rating Scale

| Rating | Meaning |
|--------|---------|
| Very Low | < 2 hours |
| Low | 2-8 hours |
| Medium | 1-2 days |
| High | 2-4 days |
| Very High | > 4 days |

### Prioritization Inputs

Priority decisions were based on:

1. **Demo flow dependency** — Does the demo break without this feature?
2. **Problem traceability** — Does this feature address a root problem from `01-PROBLEM-STATEMENT-AND-VISION.md`?
3. **Engineering complexity** — Does the feature require more than 3 days to implement correctly?
4. **AI dependency risk** — Does the feature depend on an unverified external AI capability (ASM-002)?
5. **Data dependency** — Does the feature require data that may not be available?

---

## 5. Must-Have Features (MUST / P0)

These 22 features are P0. The demo fails or is not credible without every one of them.

| FEAT-ID | Name | Dependency Chain | Day Target |
|---------|------|-----------------|-----------|
| FEAT-001 | User authentication (JWT) | None | Day 1 |
| FEAT-002 | Role-based access control | FEAT-001 | Day 2 |
| FEAT-003 | Jurisdiction scoping | FEAT-002 | Day 2 |
| FEAT-004 | Audit logging | FEAT-001, FEAT-091 | Day 2 |
| FEAT-005 | Session management and JWT expiry | FEAT-001 | Day 1 |
| FEAT-006 | Error handling and graceful degradation | All features | Day 1 |
| FEAT-010 | Create FIR manually | FEAT-003, FEAT-091 | Day 2 |
| FEAT-011 | Upload FIR document | FEAT-010, Stratus | Day 3 |
| FEAT-012 | CrimeNo auto-generation | FEAT-010 | Day 2 |
| FEAT-013 | View FIR detail (multi-tab) | FEAT-010 | Day 3 |
| FEAT-014 | Global search | FEAT-022, FEAT-091 | Day 4 |
| FEAT-015 | FIR status lifecycle | FEAT-010 | Day 2 |
| FEAT-020 | NER entity extraction from BriefFacts | FEAT-011, spaCy | Day 3 |
| FEAT-021 | Human review and correction of AI extraction | FEAT-020 | Day 3 |
| FEAT-022 | Cross-case entity resolution | FEAT-021 | Day 4 |
| FEAT-023 | Entity resolution merge review UI | FEAT-022 | Day 4 |
| FEAT-024 | PersonEntity canonical profile view | FEAT-022 | Day 4 |
| FEAT-030 | Relationship graph (Cytoscape.js) | FEAT-022, FEAT-092 | Day 5 |
| FEAT-031 | Hidden-link discovery (BFS) | FEAT-030 | Day 5 |
| FEAT-040 | Geospatial hotspot heatmap | FEAT-092, MapLibre | Day 4 |
| FEAT-041 | District-to-station drill-down | FEAT-040 | Day 4 |
| FEAT-042 | Crime type and date range filter | FEAT-040 | Day 4 |
| FEAT-043 | Anomaly detection and alerts | FEAT-092, FEAT-040 | Day 5 |
| FEAT-050 | Ask Berunda RAG | FEAT-092, LLM provider | Day 6 |
| FEAT-054 | RAG answer source citation | FEAT-050 | Day 6 |
| FEAT-055 | AI confidence score display | FEAT-020, FEAT-021 | Day 3 |
| FEAT-056 | MockProvider AI fallback | FEAT-050 | Day 5 |
| FEAT-060 | Explainable risk scoring | FEAT-022, FEAT-092 | Day 5 |
| FEAT-061 | Feature importance display | FEAT-060 | Day 5 |
| FEAT-062 | Fairness verification check | FEAT-060, FEAT-064 | Day 6 |
| FEAT-063 | Fairness dashboard | FEAT-062 | Day 6 |
| FEAT-064 | Protected-characteristic field access control | FEAT-002, schema | Day 2 |
| FEAT-080 | Audit log view | FEAT-004 | Day 3 |
| FEAT-081 | User management (Admin) | FEAT-001 | Day 2 |
| FEAT-090 | Catalyst Functions deployment | All | Day 7 |
| FEAT-091 | Catalyst Data Store schema deployment | All | Day 1 |
| FEAT-092 | Synthetic seed data load | FEAT-091 | Day 2 |

**Total P0 features: 37** (FEAT-025 promoted from P1, FEAT-090 demoted to P1; net zero change)

---

## 6. Should-Have Features (SHOULD / P1)

These features are strongly valuable. The demo is weaker without them but does not fail.

| FEAT-ID | Name | Rationale for P1 | Day Target (if P0 complete) |
|---------|------|-----------------|-----------------------------|
| FEAT-007 | Health and readiness endpoints | Required for Catalyst deployment verification | Day 1 |
| FEAT-016 | Edit draft FIR | Officers need correction before approval | Day 3 |
| FEAT-017 | Assign investigating officer (basic) | Needed for demo user assignment | Day 3 |
| FEAT-025 | Vehicle entity tracking (cross-case) | Vehicle hidden-link demo depends on this | Day 4 |
| FEAT-026 | Location entity extraction and geocoding | Hotspot map accuracy depends on location data | Day 4 |
| FEAT-032 | Graph node expand (second-degree) | Makes graph exploration more compelling | Day 6 |
| FEAT-044 | Temporal trend charts | State command dashboard core view | Day 5 |
| FEAT-045 | State command dashboard (SCRB view) | SCRB_ANALYST demo journey depends on this | Day 5 |
| FEAT-046 | Crime category breakdown charts | Completes analytics view | Day 5 |
| FEAT-051 | FIR summarisation | AI demo value for judges | Day 6 |
| FEAT-053 | Related-case recommendations | Graph and AI storytelling for judges | Day 6 |
| FEAT-072 | Case timeline (basic, from audit events) | Shows investigation history in a case | Day 4 |
| FEAT-093 | CI/CD pipeline | Deployment reliability | Day 1 |

---

## 7. Could-Have Features (COULD / P2)

Implement only if all P0 and P1 features are complete, tested, and stable by Day 8.

| FEAT-ID | Name | Condition |
|---------|------|-----------|
| FEAT-033 | Graph filter by relationship type | P0 and P1 complete by Day 7 |
| FEAT-052 | Crime category suggestion | P0 and P1 complete by Day 7 |
| FEAT-070 | Investigation notes | P0 and P1 complete by Day 7 |
| FEAT-071 | Evidence metadata linking | P0 and P1 complete and stable by Day 8 |
| FEAT-082 | Statutory report generation | P0 and P1 complete and stable by Day 8 |
| FEAT-083 | Data provenance records | P0 and P1 complete and stable by Day 8 |

---

## 8. Will-Not-Have Features (WILL NOT HAVE / P3)

These features are **explicitly rejected from the MVP**. Implementing any of them constitutes a scope violation requiring a change request.

| FEAT-ID | Name | Reason |
|---------|------|--------|
| FEAT-057 | Kannada NER | AI4Bharat model setup takes > 4 days; no training data in scope |
| — | Real CCTNS data integration | Legal MOU required; Phase 2+ |
| — | Citizen-facing FIR status portal | No citizen-facing portal in MVP; Phase 3+ |
| — | Court / judicial access view | Phase 3+ VISION feature |
| — | Neo4j graph database | Not available on Catalyst; Phase 3+ |
| — | Autonomous arrest or suspect decisions | Ethically unacceptable; explicitly prohibited |
| — | Predictive patrol deployment | Ethically out of scope; no production data |
| — | Blockchain audit trail | Phase 3+; hash-chain sufficient for MVP |
| — | Mobile native app | Responsive web only; Phase 2 |
| — | Push notifications | Phase 2 |
| — | OSINT / CCTV integration | No verified external surveillance data |
| — | Voice / speech FIR intake | Phase 2 |
| — | Individual criminality prediction | Explicitly prohibited by design principles |
| — | Cross-state correlation | Phase 5 |
| — | PDF report export (SmartBrowz) | Phase 2; PRD F-017 |

---

## 9. P0–P3 Classification Summary

| Priority | Count | Features |
|----------|-------|---------|
| P0 — Demo fails without it | 37 | FEAT-001 to 006, 010 to 015, 020 to 024, 030 to 031, 040 to 043, 050, 054 to 056, 060 to 064, 080 to 081, 090 to 092 |
| P1 — Demo is weaker | 13 | FEAT-007, 016 to 017, 025 to 026, 032, 044 to 046, 051, 053, 072, 093 |
| P2 — Nice to have | 6 | FEAT-033, 052, 070 to 071, 082 to 083 |
| P3 — Deferred / rejected | 15+ | FEAT-057 + all explicitly rejected features |
| **Total inventoried** | **71+** | All groups A–J |

---

## 10. MVP Workflow Coverage

The following table confirms that the MVP scope covers every step of the primary demo journey (JOURNEY-001) and the secondary journeys.

| Journey Step | Use Case | Features Required | P0 Complete? |
|-------------|---------|------------------|-------------|
| Officer logs in | UC-001 | FEAT-001, 002, 003, 005 | ✅ |
| Officer creates or uploads FIR | UC-002, UC-003 | FEAT-010, 011, 012 | ✅ |
| AI extraction presented for review | UC-004 | FEAT-020, 055 | ✅ |
| Officer corrects and approves extraction | UC-004 | FEAT-021 | ✅ |
| Entity resolution surfaces repeat offender | UC-007 | FEAT-022, 023, 024 | ✅ |
| Relationship graph shows cross-case links | UC-008 | FEAT-030 | ✅ |
| Hidden-link discovered | UC-008 | FEAT-031 | ✅ |
| Hotspot map shows Karnataka crime density | UC-009 | FEAT-040, 041, 042 | ✅ |
| Anomaly alert fires for planted spike | UC-011 | FEAT-043 | ✅ |
| Risk score shown with feature importance | UC-010 | FEAT-060, 061 | ✅ |
| Ask Berunda answers 3 questions | UC-012 | FEAT-050, 054, 056 | ✅ |
| Fairness dashboard confirms CasteID exclusion | UC-013 | FEAT-062, 063, 064 | ✅ |
| Audit log shows all demo actions | UC-014 | FEAT-004, 080 | ✅ |
| Role-switching between 3 demo roles | UC-001 | FEAT-001, 002, 081 | ✅ |
| All data is synthetic and labelled | — | FEAT-092 | ✅ |

---

## 11. Stretch Goals

If all P0 and P1 items are complete and stable by Day 8, the following stretch goals may be attempted in order:

| Rank | FEAT-ID | Feature | Estimated Effort | Adds |
|------|---------|---------|-----------------|------|
| 1 | FEAT-070 | Investigation notes | 1 day | Case detail richness |
| 2 | FEAT-033 | Graph filter by relationship type | 0.5 day | Graph demo UX |
| 3 | FEAT-082 | Statutory aggregate report | 1 day | Analyst demo journey |
| 4 | FEAT-071 | Evidence metadata (chain-of-custody hash) | 1 day | Governance demo |
| 5 | FEAT-052 | Crime category suggestion | 1 day | AI demo value |

Do not attempt stretch goals after Day 9.

---

## 12. Future Roadmap

| Phase | Key Features |
|-------|-------------|
| Phase 2 — Pilot | Kannada NER (AI4Bharat), real CCTNS data bridge (MOU required), SHO supervisor role, case assignment workflow, mobile-responsive polish, PDF report export |
| Phase 3 — District | Neo4j graph migration, event-driven architecture (Catalyst Signals/Circuits), ABAC access control, blockchain audit trail, court/judicial read-only view |
| Phase 4 — State | State-wide SCRB reporting automation, cross-district analytics, real-time anomaly alerting, push notifications |
| Phase 5 — National | Cross-state correlation, independently operated state instances, OSINT integration |

---

## 13. Scope Dependencies

| Dependency | Blocks | Risk |
|-----------|--------|------|
| Catalyst Data Store schema deployed (FEAT-091) | All database-dependent P0 features | High — must be Day 1 |
| Catalyst project provisioned (ASM-005) | FEAT-090, 091 | High — credits may be limited |
| spaCy English NER model loaded | FEAT-020 | Medium — add custom entity patterns |
| OpenAI / Groq API key available | FEAT-050 | Medium — FEAT-056 MockProvider is fallback |
| Synthetic seed data with planted patterns (FEAT-092) | Demo correctness | Very High — without planted patterns, demo cannot prove claims |
| Entity resolution algorithm implemented | FEAT-022 | Very High — not yet implemented per PREREQ-001 |
| Catalyst Functions scaffold → implementation | FEAT-090 | Very High — not yet implemented per PREREQ-003 |
| QuickML verified for AutoML feature importance | FEAT-060 | Medium — scikit-learn fallback available |

---

## 14. Scope Risks

| RSK-ID | Risk | Probability | Impact | Mitigation |
|--------|------|-------------|--------|------------|
| SRSK-001 | Entity resolution not implemented before Day 5 | High | Very High | Begin Day 2; freeze scope at blocked features if entity resolution fails |
| SRSK-002 | Catalyst Functions not deployable; demo cannot run on Catalyst | High | High | Accept FastAPI + AppSail as demo backend; document Catalyst architecture separately |
| SRSK-003 | Synthetic data lacks planted patterns; demo claims cannot be verified | Medium | Very High | Validate seed data script output before Day 3 |
| SRSK-004 | RAG pipeline not end-to-end verified; Ask Berunda gives no answer | Medium | High | MockProvider fallback is always available; rehearse with Mock |
| SRSK-005 | Scope creep after Day 6 — P2 features added before P0 is stable | Medium | High | Scope freeze rule enforced strictly; see Section 15 |
| SRSK-006 | QuickML capabilities do not match blueprint — risk scoring must use local scikit-learn | Medium | Medium | scikit-learn + SHAP is available locally; document as fallback |
| SRSK-007 | Demo rehearsal not completed before Day 10 | Medium | Very High | Schedule full end-to-end demo rehearsal as mandatory Day 10 task |

---

## 15. Scope Freeze Rules

Effective from the date this document is approved.

1. **No new P0 features** may be added without completing the change-request process.
2. **No new P1 features** may be added after Day 6.
3. **No P2 or stretch features** may be started before all P0 features are complete and passing their test cases.
4. **No existing P0 feature** may be removed without assessing which demo steps it breaks.
5. **If a P0 feature cannot be completed**, a formal fallback must be documented (e.g., MockProvider for RAG, pre-loaded data for entity resolution demo).
6. **Day 9 is the absolute scope freeze.** After Day 9, only bug fixes and demo polish are permitted.

---

## 16. Change-Request Process

Any request to add, remove, or reclassify a feature after this document is approved must document:

| Field | Required Information |
|-------|---------------------|
| Feature being added or changed | FEAT-ID or new feature name |
| Feature being displaced | Which P0/P1 feature is de-prioritised to make room |
| Added engineering complexity | Hours estimated; which days |
| New data dependency | Any new table or data not already required |
| New test burden | Additional test cases required |
| New demo burden | Additional demo steps required |
| New risks introduced | What can now go wrong |
| Approval decision | Team decision recorded with date |

---

## 17. Definition of MVP Completion

The MVP is complete when all of the following conditions are satisfied:

| Criterion | Verification Method |
|-----------|-------------------|
| All 37 P0 features have passing implementation | Unit test, integration test, or manual verification |
| Demo rehearsal completes end-to-end without manual patches | Recorded demo run on Day 10 |
| Planted repeat-offender correctly linked across 4 cases | Acceptance test DEMO-T04 passes |
| Hidden-link found between Case 001 and Case 042 | Acceptance test DEMO-T06 passes |
| Hotspot map renders with anomaly badge | Acceptance test DEMO-T07 and DEMO-T08 pass |
| Risk score shows feature importance; CasteID/ReligionID absent | Acceptance test DEMO-T09 and DEMO-T13 pass |
| Ask Berunda answers 3 rehearsed questions with citations | Acceptance tests DEMO-T10, DEMO-T11, DEMO-T12 pass |
| All 4 roles can log in and see correct scoped views | Acceptance test DEMO-T01, DEMO-T15 pass |
| Audit log shows all actions taken during demo rehearsal | Acceptance test DEMO-T14 passes |
| Synthetic data label is visible on every data screen | Manual UI check |
| Demo fallback video recorded | Video file exists in archive/ |

---

## Scope Baseline Table

| FEAT-ID | MVP Status | Owner Placeholder | Req Dependencies | Data Dependencies | Demo Step | Verification Method |
|---------|-----------|-------------------|-----------------|------------------|-----------|---------------------|
| FEAT-001 | IN MVP P0 | Backend Dev | FR-AUTH-001 | User table | DEMO-T01 | Login test |
| FEAT-002 | IN MVP P0 | Backend Dev | FR-AUTH-003 | User table, roles | DEMO-T01, DEMO-T15 | Role switching test |
| FEAT-003 | IN MVP P0 | Backend Dev | FR-AUTH-004 | CaseMaster.DistrictRef | DEMO-T01 | District filter test |
| FEAT-004 | IN MVP P0 | Backend Dev | FR-AUD-001 | gov_AuditLog | DEMO-T14 | Audit log check |
| FEAT-005 | IN MVP P0 | Backend Dev | FR-AUTH-002 | None | Any login test | JWT expiry test |
| FEAT-006 | IN MVP P0 | All | Non-functional | None | All steps | Error scenario test |
| FEAT-010 | IN MVP P0 | Full-stack Dev | FR-FIR-001 | CaseMaster | DEMO-T02 | Create FIR test |
| FEAT-011 | IN MVP P0 | Full-stack Dev | FR-FIR-003 | EvidenceMaster, Stratus | DEMO-T02 | Upload test |
| FEAT-012 | IN MVP P0 | Backend Dev | FR-FIR-002 | CaseMaster | DEMO-T02 | CrimeNo uniqueness test |
| FEAT-013 | IN MVP P0 | Frontend Dev | FR-FIR-005 | All FIR tables | DEMO-T02 | View case detail test |
| FEAT-014 | IN MVP P0 | Full-stack Dev | FR-SRCH-001 | PersonEntity, CaseMaster | DEMO-T01, DEMO-T05 | Search result test |
| FEAT-015 | IN MVP P0 | Backend Dev | FR-FIR-004 | CaseMaster.Status | DEMO-T03 | Status transition test |
| FEAT-020 | IN MVP P0 | AI Dev | FR-AI-001 | BriefFacts, spaCy | DEMO-T02 | Extraction accuracy test |
| FEAT-021 | IN MVP P0 | Frontend Dev | FR-AI-003 | Extraction queue | DEMO-T03 | Review-and-approve test |
| FEAT-022 | IN MVP P0 | AI/Backend Dev | FR-AI-005 | PersonEntity | DEMO-T04 | Planted repeat-offender test |
| FEAT-023 | IN MVP P0 | Frontend Dev | FR-AI-006 | PersonEntity | DEMO-T04 | Merge approval test |
| FEAT-024 | IN MVP P0 | Frontend Dev | FR-AI-007 | PersonEntity, RelationshipEdge | DEMO-T05 | Profile view test |
| FEAT-025 | IN MVP P0 | Backend Dev | FR-AI-001 (embedded) | VehicleLink | DEMO-T06 | Vehicle cross-case linkage test |
| FEAT-030 | IN MVP P0 | Frontend Dev | FR-AI-008 | RelationshipEdge | DEMO-T05 | Graph render test |
| FEAT-031 | IN MVP P0 | Backend Dev | FR-AI-009 | RelationshipEdge | DEMO-T06 | Shortest-path test |
| FEAT-040 | IN MVP P0 | Frontend Dev | FR-RPT-001 | HotspotLayer, coords | DEMO-T07 | Map render test |
| FEAT-041 | IN MVP P0 | Frontend Dev | FR-RPT-002 | PoliceStation, DistrictRef | DEMO-T07 | Drill-down test |
| FEAT-042 | IN MVP P0 | Frontend Dev | FR-RPT-003 | CrimeHeadRef, date fields | DEMO-T07 | Filter test |
| FEAT-043 | IN MVP P0 | Backend Dev | FR-RPT-004 | AnomalyAlert, baseline | DEMO-T08 | Anomaly detection test |
| FEAT-050 | IN MVP P0 | AI Dev | FR-AI-010 | RAG corpus | DEMO-T10, T11 | 3-question test |
| FEAT-054 | IN MVP P0 | AI Dev | FR-AI-012 | RAG chunk metadata | DEMO-T10 | Citation presence test |
| FEAT-055 | IN MVP P0 | AI Dev | FR-AI-002 | Extraction metadata | DEMO-T03 | Confidence score display |
| FEAT-056 | IN MVP P0 | AI Dev | FR-AI-011 | None (mock) | All AI steps | API unavailability test |
| FEAT-060 | IN MVP P0 | AI/Backend Dev | FR-AI-013 | PersonEntity, prior cases | DEMO-T09 | Risk score computation test |
| FEAT-061 | IN MVP P0 | AI Dev | FR-AI-014 | Model output | DEMO-T09 | Feature importance display |
| FEAT-062 | IN MVP P0 | AI Dev | FR-AI-015 | gov_FairnessCheckResult | DEMO-T13 | Fairness check output test |
| FEAT-063 | IN MVP P0 | Frontend Dev | FR-AI-016 | gov_FairnessCheckResult | DEMO-T13 | Fairness dashboard render |
| FEAT-064 | IN MVP P0 | Backend Dev | FR-AUTH-005 | Accused, Victim, Complainant | DEMO-T13 | Field access control test |
| FEAT-080 | IN MVP P0 | Frontend Dev | FR-AUD-002 | gov_AuditLog | DEMO-T14 | Audit log view test |
| FEAT-081 | IN MVP P0 | Full-stack Dev | FR-AUTH-006 | User table | Demo setup | User creation test |
| FEAT-091 | IN MVP P0 | DevOps | Non-functional | All tables | Day 1 | Schema deployment test |
| FEAT-092 | IN MVP P0 | Data Dev | Non-functional | All entity tables | Demo setup | Seed data validation test |

---

*End of 04-MVP-SCOPE-AND-PRIORITIZATION.md*
