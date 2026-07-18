# Traceability Chain

[//]: # (Document ID: BERUNDA-REP-004 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team, Governance | Source: All project docs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Traceability Overview

This document traces every feature of Project Berunda end-to-end through the complete delivery lifecycle. The traceability chain follows a linear path from strategic intent through to empirical evidence:

**Challenge Objective â†’ Stakeholder Need â†’ Use Case â†’ Functional Requirement â†’ Architecture Component â†’ Data Entity â†’ Security/Privacy Control â†’ Test Case â†’ Demo Evidence â†’ Roadmap Phase**

### 1.1 Traceability Purpose

- **Accountability**: Every feature in the MVP can be traced back to an approved objective and stakeholder need
- **Coverage Analysis**: Identify requirements, data entities, or stakeholders with insufficient test coverage
- **Impact Assessment**: When a requirement or component changes, the full blast radius is visible
- **Demo Readiness**: Each feature maps to concrete demo evidence observable during the 11-day hackathon
- **Governance Compliance**: Security, privacy, and fairness controls are explicitly mapped to the features they protect

### 1.2 Reference Documents

| Document | ID | Source |
|----------|----|--------|
| Project Charter | BERUNDA-CHTR-001 | `docs/strategy-and-product/PROJECT_CHARTER.md` |
| Problem, Stakeholders & Personas | BERUNDA-PERS-001 | `docs/strategy-and-product/PROBLEM_STAKEHOLDERS_AND_PERSONAS.md` |
| Use Case Catalog | BERUNDA-UC-001 | `docs/strategy-and-product/USE_CASE_CATALOG.md` |
| Software Requirements Specification | BERUNDA-SRS-001 | `docs/requirements/SOFTWARE_REQUIREMENTS_SPECIFICATION.md` |
| Requirements Traceability Matrix | BERUNDA-TRACE-001 | `docs/requirements/REQUIREMENTS_TRACEABILITY_MATRIX.md` |
| Test Case Catalog | BERUNDA-QA-002 | `docs/quality/TEST_CASE_CATALOG.md` |
| Enterprise Roadmap | BERUNDA-DEL-006 | `docs/delivery/ENTERPRISE_ROADMAP.md` |

### 1.3 ID Prefix Reference

| Prefix | Meaning | Source Document |
|--------|---------|----------------|
| OBJ- | Business Objective | Project Charter |
| STK- | Stakeholder | Problem, Stakeholders & Personas |
| UC- | Use Case | Use Case Catalog |
| FR- | Functional Requirement | SRS Â§1 |
| DR- | Data Requirement | SRS Â§2 |
| AIR- | AI Requirement | SRS Â§3 |
| SEC- | Security Requirement | SRS Â§4 |
| PRIV- | Privacy Requirement | SRS Â§5 |
| TC- | Test Case | Test Case Catalog |
| TST- | Alternative Test ID | Test Case Catalog (legacy mapping) |

---

## 2. Complete Traceability Matrix

Each row maps one feature end-to-end from the originating business objective to the roadmap phase and demo evidence.

| Feature | Objective | Stakeholder | Use Case | FR | Architecture | Data | Security | Test | Demo Evidence | Roadmap |
|---------|-----------|-------------|----------|-----|-------------|------|----------|------|--------------|---------|
| FIR Structured Import | OBJ-001 | STK-001 | UC-001 | FR-001, FR-003, FR-004 | Ingestion Function (Catalyst Function) | src_CaseMaster, src_AccusedDetails, src_VictimDetails, src_ComplainantDetails | SEC-004, SEC-005 | TC-INT-001, TC-INT-002 | Upload dialog shown; imported case list renders with validation pass/fail indicators | Phase 1 MVP |
| FIR Manual Entry | OBJ-001 | STK-001 | UC-001 | FR-002, FR-003 | Ingestion Function + Slate UI | src_CaseMaster | SEC-004, SEC-005 | â€” | Manual entry form with field-level validation | Phase 1 MVP |
| Duplicate FIR Detection | OBJ-001 | STK-001 | UC-001 | FR-004 | Ingestion Function | src_CaseMaster.CrimeNo | SEC-004 | TC-INT-002 | Duplicate CrimeNo flagged with warning badge | Phase 1 MVP |
| English NER Extraction | OBJ-001 | STK-001 | UC-002 | FR-005, FR-007, FR-008 | NER Function (spaCy pipeline) | int_PersonEntityLink, int_VehicleLink, src_CaseMaster.BriefFacts | SEC-004 | TC-NER-001 to TC-NER-005, TC-INT-001 | FIR detail view shows extracted entities with confidence scores | Phase 1 MVP |
| Kannada NER Extraction | OBJ-001 | STK-001 | UC-002 | FR-006 | NER Function (IndicNLP) | int_PersonEntityLink | SEC-004 | â€” | â€” | Phase 2 STRETCH |
| PersonEntity Resolution | OBJ-002 | STK-001, STK-003 | UC-003 | FR-009 to FR-015 | Entity Resolution Function | int_PersonEntity, int_PersonEntityLink, src_AccusedDetails, src_VictimDetails, src_ComplainantDetails | SEC-004, PRIV-004 | TC-ER-001 to TC-ER-008, TC-INT-003, TC-AT-001 | Planted 4â†’1 merge; PersonEntity detail shows linked cases with confidence badges | Phase 1 MVP |
| Relationship Graph View | OBJ-002 | STK-003 | UC-004 | FR-016, FR-017, FR-018 | AppSail NetworkX + Graph UI | int_RelationshipEdge, int_PersonEntity | SEC-004 | TC-INT-004, TC-AT-002 | Force-directed graph renders; nodes clickable; edges show relationship type | Phase 1 MVP |
| Hidden Link Discovery | OBJ-002 | STK-003 | UC-005 | FR-017, FR-018 | AppSail NetworkX (shortest-path, centrality) | int_RelationshipEdge, int_PersonEntity, int_VehicleLink | SEC-004 | TC-INT-004, TC-AT-002 | Co-accused cluster visualized; shortest path between two entities shown | Phase 1 MVP |
| Vehicle Linking | OBJ-002 | STK-001 | UC-004 | FR-019 | NER Function + Graph | int_VehicleLink, int_RelationshipEdge | SEC-004 | TC-AT-003 | Vehicle detail shows all associated cases across districts | Phase 1 MVP |
| MO Pattern Matching | OBJ-002 | STK-003 | UC-005 | FR-020 | Embedding Function (Sentence-Transformer) | int_MOEmbedding (proposed) | â€” | â€” | â€” | Phase 2 STRETCH |
| Geospatial Hotspot Map | OBJ-003 | STK-003, STK-004 | UC-006 | FR-021, FR-022, FR-023 | Hotspot Function + Slate Map | int_HotspotLayer, src_CaseMaster (Lat/Long) | SEC-004 | TC-INT-005 | Hexbin/heatmap layer renders; drill-down from state â†’ district â†’ station works | Phase 1 MVP |
| Temporal Crime Analysis | OBJ-003 | STK-003, STK-004 | UC-007 | FR-023 | Analytics Function + Slate Charts | src_CaseMaster (date, type, jurisdiction) | SEC-004 | â€” | Line/bar charts update with date range, crime type, jurisdiction filters | Phase 1 MVP |
| Anomaly/Spike Detection | OBJ-003 | STK-003 | UC-009 | FR-024, FR-025 | Anomaly Function (z-score) | int_AnomalyAlert, src_CaseMaster | SEC-004 | TC-AD-001 to TC-AD-003, TC-AT-004 | AnomalyAlert badge on dashboard; spike detail shows deviation magnitude | Phase 1 MVP |
| Risk Score Computation | OBJ-004 | STK-003 | UC-008 | FR-026, FR-027, FR-028, FR-029 | QuickML AutoML + Risk Function | int_RiskScore, int_PersonEntity, gov_AuditLog | SEC-007, PRIV-004 | TC-RS-001 to TC-RS-005, TC-INT-007, TC-AT-005, TC-SEC-005 | Score bar + feature importance breakdown visible; CasteID absent from features | Phase 1 MVP |
| RAG Natural-Language Query | OBJ-005 | STK-001, STK-003 | UC-010 | FR-030, FR-031, FR-032, FR-033, FR-034 | QuickML LLM + RAG Function | int_RAGCorpusChunk, gov_AuditLog | SEC-004, FR-032, EC-003 | TC-INT-006, TC-AT-003, TC-SEC-001, TC-SEC-002 | Cited answer to "How many FIRs in Bengaluru Urban?" with source document links | Phase 1 MVP |
| User Authentication | OBJ-006 | STK-001, STK-012, STK-013 | UC-011 | FR-035, FR-038 | Catalyst Auth + API Gateway | src_Employee (user directory) | SEC-001 to SEC-009 | TC-AUTH-001 to TC-AUTH-004 | Login flow; MFA challenge; valid token grants access; expired token returns 401 | Phase 1 MVP |
| Role-Based Access Control | OBJ-006 | STK-001, STK-012, STK-013 | UC-011 | FR-036, FR-037 | Catalyst Auth + API Gateway | src_Employee.RoleID | SEC-003, SEC-007, SEC-008 | TC-RBAC-001 to TC-RBAC-004, TC-AT-006 | Role-switching demo: Investigator sees district data only; Compliance sees CasteID | Phase 1 MVP |
| Person-Level Read Audit | OBJ-006 | STK-012 | UC-012 | FR-039, FR-041, FR-042 | Audit Function | gov_AuditLog | SEC-004, PRIV-005 | TC-INT-008 | Audit log viewer shows who read which person record, when, and why | Phase 1 MVP |
| AI Output Audit | OBJ-006 | STK-012 | UC-012 | FR-040, FR-041, FR-042 | Audit Function | gov_AuditLog | SEC-004, PRIV-005 | TC-INT-008 | RAG query and risk score reads logged with user, query, and response digest | Phase 1 MVP |
| Fairness/Bias Verification | OBJ-007 | STK-012 | UC-013 | FR-043, FR-044, FR-045 | Fairness Function | gov_FairnessCheckResult, int_RiskScoreFeatureImportance, gov_AuditLog | SEC-007, PRIV-004 | TC-AT-005 | Fairness dashboard shows green "PASS" for all checks; restricted fields verifiably absent | Phase 1 MVP |
| SC/ST Aggregate Reporting | OBJ-007 | STK-012 | UC-014 | â€” | Reporting Function | src_ComplainantDetails.CasteID | SEC-007, PRIV-004 | â€” | â€” | Phase 2 STRETCH |
| State-Level Command Dashboard | OBJ-003 | STK-003, STK-008 | UC-015 | FR-023 | Slate Dashboard | src_CaseMaster | SEC-003 | â€” | State-level KPI cards with district comparison, trends, and drill-down | Phase 1 MVP |
| Synthetic Data Generation | OBJ-001 | STK-001 | UC-001 | FR-046, FR-047, FR-048, FR-049 | DataGen Function | All source tables | PRIV-001, PRIV-002 | â€” | 2000+ synthetic FIRs generated with seeded reproducibility; planted patterns visible | Phase 1 MVP |

---

## 3. Requirement-to-Code Mapping

Every functional, data, AI, and security requirement is mapped to the Catalyst component that implements it.

### 3.1 Functional Requirement Mapping

| FR ID | Title | Component | Catalyst Service | Data Read | Data Write | Depends On |
|-------|-------|-----------|-----------------|-----------|------------|------------|
| FR-001 | FIR Structured Import | FIR Ingestion Function | Catalyst Function | CSV/Excel source file | src_CaseMaster, src_AccusedDetails, src_VictimDetails, src_ComplainantDetails | DR-001, DR-005 |
| FR-002 | FIR Manual Entry | FIR Entry Form | Catalyst Slate + Function | â€” | src_CaseMaster | DR-001 |
| FR-003 | Data Validation | FIR Ingestion Function | Catalyst Function | src_CaseMaster (schema) | â€” | â€” |
| FR-004 | Duplicate Detection | FIR Ingestion Function | Catalyst Function | src_CaseMaster.CrimeNo | â€” | â€” |
| FR-005 | English NER | NER Extraction Function | Catalyst Function (spaCy) | src_CaseMaster.BriefFacts | int_PersonEntityLink, int_VehicleLink | DR-006, AIR-001 |
| FR-006 | Kannada NER | NER Extraction Function (extended) | Catalyst Function (IndicNLP) | src_CaseMaster.BriefFacts | int_PersonEntityLink | AIR-008 |
| FR-007 | Confidence Scoring | NER Extraction Function | Catalyst Function | â€” | int_PersonEntityLink.Confidence | â€” |
| FR-008 | Entity Linking | NER Extraction Function | Catalyst Function | int_PersonEntity | int_PersonEntityLink.CaseMasterID | â€” |
| FR-009 | PersonEntity Identity | Entity Resolution Function | Catalyst Function | src_AccusedDetails, src_VictimDetails, src_ComplainantDetails | int_PersonEntity | DR-002 |
| FR-010 | Blocking Strategy | Entity Resolution Function | Catalyst Function | int_PersonEntity | â€” | â€” |
| FR-011 | Similarity Scoring | Entity Resolution Function | Catalyst Function | int_PersonEntity | int_PersonEntityLink.MatchConfidence | â€” |
| FR-012 | Match Thresholds | Entity Resolution Function | Catalyst Function | Config table | â€” | â€” |
| FR-013 | Manual Review | ER Review UI | Catalyst Slate | int_PersonEntityLink (grey zone) | int_PersonEntityLink.ReviewStatus | â€” |
| FR-014 | Merge Approval | ER Review UI | Catalyst Slate | int_PersonEntityLink | int_PersonEntity.MergedInto | â€” |
| FR-015 | Provenance Tracking | Entity Resolution Function | Catalyst Function | â€” | int_PersonEntityLink.SourceTable, SourceRecordID | â€” |
| FR-016 | RelationshipEdge Table | Link Analysis Function | Catalyst Function | int_PersonEntityLink, int_VehicleLink | int_RelationshipEdge | DR-002 |
| FR-017 | Graph Traversal | Link Analysis Function | Catalyst AppSail (NetworkX) | int_RelationshipEdge | â€” | â€” |
| FR-018 | Graph Visualization | Relationship Graph UI | Catalyst Slate + AppSail | int_RelationshipEdge | â€” | â€” |
| FR-019 | Vehicle Linking | NER + Link Analysis Function | Catalyst Function | int_VehicleLink | int_RelationshipEdge | â€” |
| FR-020 | MO Pattern Matching | MO Embedding Function | Catalyst Function (Sentence-Transformer) | src_CaseMaster.BriefFacts | int_MOEmbedding | AIR-009 |
| FR-021 | Hotspot Map | Hotspot Function | Catalyst Function | src_CaseMaster.Lat, src_CaseMaster.Long | int_HotspotLayer | AIR-003 |
| FR-022 | District Drill-Down | Hotspot UI | Catalyst Slate | int_HotspotLayer | â€” | â€” |
| FR-023 | Temporal Filter | Hotspot + Analytics UI | Catalyst Slate | src_CaseMaster (date, type, jurisdiction) | â€” | â€” |
| FR-024 | Anomaly Detection | Anomaly Function | Catalyst Function | src_CaseMaster | int_AnomalyAlert | AIR-004 |
| FR-025 | Anomaly Alert | Anomaly Function | Catalyst Function | int_AnomalyAlert | int_AnomalyAlert.AlertStatus | â€” |
| FR-026 | Risk Score Computation | QuickML Risk Function | Catalyst QuickML + Function | int_PersonEntity + feature tables | int_RiskScore | AIR-002, AIR-006 |
| FR-027 | Feature Importance | QuickML Risk Function | Catalyst QuickML | â€” | int_RiskScore.FeatureImportanceJSON | AIR-006 |
| FR-028 | Feature Exclusion | QuickML Risk Function | Catalyst QuickML | int_RiskScore | â€” | SEC-007, PRIV-004 |
| FR-029 | Score Explainability | Risk Score UI | Catalyst Slate | int_RiskScore | â€” | â€” |
| FR-030 | RAG Query | RAG Query Function | Catalyst QuickML LLM | int_RAGCorpusChunk | â€” | AIR-005 |
| FR-031 | Source Citations | RAG Query Function | Catalyst QuickML LLM | int_RAGCorpusChunk | â€” | â€” |
| FR-032 | Role-Based Filtering | RAG Query Function | Catalyst QuickML LLM | int_RAGCorpusChunk | â€” | SEC-003 |
| FR-033 | Insufficient Evidence Response | RAG Query Function | Catalyst QuickML LLM | â€” | â€” | â€” |
| FR-034 | Query Audit | RAG + Audit Function | Catalyst Function | gov_AuditLog | gov_AuditLog | â€” |
| FR-035 | User Authentication | Catalyst Auth | Catalyst Authentication | src_Employee | â€” | â€” |
| FR-036 | Role-Based Access | RBAC Enforcer | Catalyst API Gateway + Auth | src_Employee.RoleID | â€” | SEC-003 |
| FR-037 | Jurisdiction Scoping | RBAC Enforcer | Catalyst API Gateway + Auth | src_Employee.DistrictID | â€” | â€” |
| FR-038 | MFA Support | Catalyst Auth | Catalyst Authentication | â€” | â€” | â€” |
| FR-039 | Person-Level Read Audit | Audit Function | Catalyst Function | gov_AuditLog | gov_AuditLog | â€” |
| FR-040 | AI Output Audit | Audit Function | Catalyst Function | gov_AuditLog | gov_AuditLog | â€” |
| FR-041 | Append-Only Log | Audit Function | Catalyst Function | gov_AuditLog | gov_AuditLog | â€” |
| FR-042 | Audit Queryability | Audit UI | Catalyst Slate | gov_AuditLog | â€” | â€” |
| FR-043 | Fairness Check | Fairness Function | Catalyst Function | int_RiskScoreFeatureImportance | gov_FairnessCheckResult | AIR-007 |
| FR-044 | Role Restriction Check | Fairness Function | Catalyst Function | gov_AuditLog, src_ComplainantDetails | gov_FairnessCheckResult | â€” |
| FR-045 | Fairness Dashboard | Fairness UI | Catalyst Slate | gov_FairnessCheckResult | â€” | â€” |
| FR-046 | Synthetic Data Generation | DataGen Function | Catalyst Function | â€” | All src_ tables | â€” |
| FR-047 | Planted Patterns | DataGen Function | Catalyst Function | â€” | int_PersonEntityLink (planted merges) | â€” |
| FR-048 | Seeded Reproducibility | DataGen Function | Catalyst Function | â€” | â€” | â€” |
| FR-049 | Synthetic Labeling | DataGen Function | Catalyst Function | â€” | src_CaseMaster.Label | â€” |

### 3.2 AI Requirement Mapping

| AIR ID | Title | Component | Service |
|--------|-------|-----------|---------|
| AIR-001 | NER Pipeline | NER Extraction Function | Catalyst Function (spaCy) |
| AIR-002 | Risk Scoring Model | QuickML Risk Function | Catalyst QuickML AutoML |
| AIR-003 | Hotspot Detection | Hotspot Function | Catalyst Function (KDE/hexbin) |
| AIR-004 | Anomaly Detection | Anomaly Function | Catalyst Function (z-score) |
| AIR-005 | RAG Foundation | RAG Query Function | Catalyst QuickML LLM |
| AIR-006 | Feature Importance | QuickML Risk Function | Catalyst QuickML |
| AIR-007 | Fairness Auditing | Fairness Function | Catalyst Function |
| AIR-008 | Kannada NER | NER Extraction Function (extended) | Catalyst Function (IndicNLP) |
| AIR-009 | MO Embeddings | MO Embedding Function | Catalyst Function (Sentence-Transformer) |
| AIR-010 | Drift Monitoring | â€” | â€” |
| AIR-011 | Bias Proxy Check | â€” | â€” |
| AIR-012 | No Criminality Prediction | All AI Functions | â€” |
| AIR-013 | Advisory Only | All AI Output UI | Catalyst Slate |
| AIR-014 | Human-in-the-Loop | All AI Functions + Review UI | â€” |
| AIR-015 | Confidence Display | All AI Output UI | Catalyst Slate |

### 3.3 Data Requirement Mapping

| DR ID | Title | Tables | Created By | Used By |
|-------|-------|--------|------------|---------|
| DR-001 | Source Schema Migration | All 27+ src_ tables | FIR Ingestion | All Functions |
| DR-002 | Berunda Extension Tables | int_PersonEntity, int_PersonEntityLink, int_RelationshipEdge, int_RiskScore, gov_AuditLog | Various Functions | Various Functions |
| DR-003 | Indexes | src_CaseMaster (CrimeMajorHeadID, CrimeRegisteredDate, PoliceStationID) | DB Migration | Hotspot, Anomaly, Temporal |
| DR-004 | CasteID Not Indexed | src_ComplainantDetails.CasteID | DB Migration | Compliance (only) |
| DR-005 | CrimeNo Parsing | src_CaseMaster.CrimeNo | FIR Ingestion | â€” |
| DR-006 | Full-Text Index | Inv_OccuranceTime.BriefFacts | DB Migration | NER Function |
| DR-007 | Schema Separation | src_ vs int_ vs gov_ | DB Migration | All |

### 3.4 Security Requirement Mapping

| SEC ID | Title | Enforced By | Protects |
|--------|-------|-------------|----------|
| SEC-001 | Encryption at Rest | Catalyst Data Store Platform | All data |
| SEC-002 | Encryption in Transit | Catalyst API Gateway | All communication |
| SEC-003 | API Gateway | Catalyst API Gateway | All API endpoints |
| SEC-004 | Input Validation | All Catalyst Functions | All user input fields |
| SEC-005 | Parameterized Queries | All Catalyst Functions | All DB queries |
| SEC-006 | Secrets Management | Catalyst Secrets | API keys, credentials |
| SEC-007 | CasteID Role Restriction | RBAC Enforcer + API Gateway | src_ComplainantDetails.CasteID, ReligionID |
| SEC-008 | Rate Limiting | Catalyst API Gateway | All API endpoints |
| SEC-009 | Session Management | Catalyst Auth | All authenticated sessions |

### 3.5 Privacy Requirement Mapping

| PRIV ID | Title | Enforced By | Scope |
|---------|-------|-------------|-------|
| PRIV-001 | No Real PII in Demo | DataGen Function | All synthetic data |
| PRIV-002 | Synthetic Labeling | DataGen Function | All src_ records |
| PRIV-003 | Data Minimization | All Functions | All data collection |
| PRIV-004 | Caste/Religion Governance | RBAC + Fairness Function + QuickML | Model features + reporting |
| PRIV-005 | Audit Proportionality | Audit Function | gov_AuditLog contents |

---

## 4. Data Entity Traceability

Every data entity (table) in the Berunda Data Store schema traced from creation through read/write/delete operations and security controls.

### 4.1 Source Tables (src_ â€” Imported from FIR ERD)

| Data Entity | Created By | Read By | Updated By | Deleted By | Security Controls | Classification |
|------------|-----------|---------|------------|------------|-------------------|---------------|
| src_CaseMaster | FIR Ingestion Function | All Functions | Never (immutable) | Admin only | SEC-001, SEC-002, SEC-004 | SENSITIVE |
| src_AccusedDetails | FIR Ingestion Function | ER, Risk, Graph, RAG, Audit | Never | Admin only | SEC-001, SEC-004 | SENSITIVE |
| src_VictimDetails | FIR Ingestion Function | ER, Risk, Graph, RAG, Audit | Never | Admin only | SEC-001, SEC-004 | SENSITIVE |
| src_ComplainantDetails | FIR Ingestion Function | ER, RAG, Audit, Compliance | Never | Admin only | SEC-001, SEC-004, SEC-007 (CasteID), PRIV-004 | RESTRICTED |
| src_WitnessDetails | FIR Ingestion Function | ER, Graph, Audit | Never | Admin only | SEC-001, SEC-004 | SENSITIVE |
| src_PropertyDetails | FIR Ingestion Function | Graph, RAG, Audit | Never | Admin only | SEC-001, SEC-004 | INTERNAL |
| src_VehicleDetails | FIR Ingestion Function | NER, Graph, RAG, Audit | Never | Admin only | SEC-001, SEC-004 | SENSITIVE |
| src_Inv_OccuranceTime | FIR Ingestion Function | NER, RAG, Audit | Never | Admin only | SEC-001, SEC-004 | INTERNAL |
| src_Inv_SpotInspection | FIR Ingestion Function | RAG, Audit | Never | Admin only | SEC-001, SEC-004 | INTERNAL |
| src_Employee | FIR Ingestion Function | Auth, RBAC, Audit | Admin | Admin | SEC-001, SEC-002, SEC-009 | RESTRICTED |
| src_Unit (PoliceStation) | FIR Ingestion Function | All | Admin | Admin | SEC-001 | PUBLIC |
| src_District | FIR Ingestion Function | All | Admin | Admin | SEC-001 | PUBLIC |
| src_CrimeMajorHead | FIR Ingestion Function | All | Admin | Admin | SEC-001 | PUBLIC |
| src_CrimeMinorHead | FIR Ingestion Function | All | Admin | Admin | SEC-001 | PUBLIC |

### 4.2 Intelligence Tables (int_ â€” Berunda Extensions)

| Data Entity | Created By | Read By | Updated By | Deleted By | Security Controls | Classification |
|------------|-----------|---------|------------|------------|-------------------|---------------|
| int_PersonEntity | Entity Resolution Function | Risk, Graph, RAG, Audit, Compliance | Entity Resolution (merge) | Admin only | SEC-001, SEC-002, SEC-004 | SENSITIVE |
| int_PersonEntityLink | Entity Resolution Function | Graph, RAG, Audit, Compliance | Manual Review (confirm/reject) | Admin only | SEC-001, SEC-004 | SENSITIVE |
| int_VehicleLink | NER Function + Entity Resolution | Graph, RAG, Audit | Never | Admin only | SEC-001, SEC-004 | SENSITIVE |
| int_RelationshipEdge | Link Analysis Function | Graph UI, RAG, Audit | Link Analysis (recompute) | Admin only | SEC-001 | INTERNAL |
| int_HotspotLayer | Hotspot Function | Hotspot UI | Hotspot Function (refresh) | Admin only | SEC-001 | INTERNAL |
| int_AnomalyAlert | Anomaly Function | Anomaly UI, Dashboard | Anomaly Function (acknowledge) | Admin only | SEC-001 | INTERNAL |
| int_RiskScore | QuickML Risk Function | Risk UI, Compliance | Risk Function (recompute) | Admin only | SEC-001, SEC-007, PRIV-004 | RESTRICTED |
| int_RiskScoreFeatureImportance | QuickML Risk Function | Risk UI, Fairness | Risk Function (recompute) | Admin only | SEC-001, SEC-007, PRIV-004 | RESTRICTED |
| int_RAGCorpusChunk | RAG Corpus Builder | RAG Function | RAG Corpus Builder (refresh) | Admin only | SEC-001, SEC-004 | INTERNAL |
| int_MOEmbedding (proposed) | MO Embedding Function | MO Matching Function | MO Embedding Function (refresh) | Admin only | SEC-001 | INTERNAL |

### 4.3 Governance Tables (gov_ â€” Audit & Compliance)

| Data Entity | Created By | Read By | Updated By | Deleted By | Security Controls | Classification | Retention |
|------------|-----------|---------|------------|------------|-------------------|---------------|-----------|
| gov_AuditLog | Multiple Functions (Audit, RAG, Risk) | Audit UI, Compliance | Never (append-only) | Never (immutable) | SEC-001, SEC-002, SEC-004, PRIV-005 | RESTRICTED | 7 years (statutory) |
| gov_FairnessCheckResult | Fairness Function | Fairness UI, Compliance | Never | Admin only | SEC-001, SEC-007, PRIV-004 | RESTRICTED | Indefinite |

---

## 5. Stakeholder-to-Requirement Coverage

Maps every stakeholder to the functional requirements that serve their needs and identifies gaps for future phases.

### 5.1 Primary Stakeholder Coverage

| STK-ID | Stakeholder | FR IDs Covered (MVP) | FR IDs Covered (STRETCH/VISION) | Gaps |
|--------|-------------|----------------------|--------------------------------|------|
| STK-001 | Investigating Officers (IOs) | FR-001 to FR-008 (Ingest + NER), FR-009 to FR-019 (ER + Graph + Vehicle), FR-026 to FR-029 (Risk + Explain), FR-030 to FR-034 (RAG), FR-035 to FR-038 (Auth) | FR-020 (MO Matching), FR-006 (Kannada NER) | None for MVP; MO Pattern and Kannada NLP deferred to Phase 2 |
| STK-002 | Station House Officers (SHOs) | FR-021 to FR-023 (Hotspot + Temporal), FR-024 to FR-025 (Anomaly), FR-030 to FR-034 (RAG), FR-035 to FR-038 (Auth), UC-015 (Command Dashboard) | â€” | Local dashboard for jurisdiction awareness is covered by hotspot + temporal filters |
| STK-003 | SCRB Analysts | FR-009 to FR-019 (ER + Graph), FR-021 to FR-023 (Hotspot + Temporal), FR-024 to FR-025 (Anomaly), FR-026 to FR-029 (Risk), FR-030 to FR-034 (RAG), UC-015 (Dashboard) | FR-020 (MO Matching) | MO Pattern Matching is the key gap; deferred to STRETCH |
| STK-004 | Superintendent of Police (District) | FR-021 to FR-023 (Hotspot + Temporal), FR-024 to FR-025 (Anomaly), UC-015 (Dashboard) | â€” | None for MVP; resource deployment recommendations are implicit in hotspot + anomaly |
| STK-005 | Cyber Crime Cells | â€” | â€” | Full gap â€” OSINT correlation is VISION only |
| STK-006 | Forensic Labs | â€” | â€” | Full gap â€” evidence metadata is VISION only |
| STK-007 | Judiciary / Courts | â€” | â€” | Full gap â€” read-only case timelines are VISION only |
| STK-008 | DGP Office / Home Ministry | UC-015 (State Dashboard) | â€” | State-level dashboard covers this need at MVP level |
| STK-009 | Women Safety Wing | FR-021 to FR-023 (Hotspot drill-down by crime type) | â€” | Crime-type filtering on hotspot covers women-safety patterns |
| STK-010 | Traffic Police | FR-019 (Vehicle Linking) | â€” | Vehicle-linked incident cross-referencing is covered by VehicleLink |
| STK-011 | Citizens (indirect) | FR-043 to FR-045 (Fairness), PRIV-001 to PRIV-005 | â€” | Governance safeguards benefit citizens indirectly |
| STK-012 | Governance / Compliance Officer | FR-015 (Provenance), FR-028 (Feature Exclusion), FR-034 (Query Audit), FR-039 to FR-042 (Audit), FR-043 to FR-045 (Fairness), SEC-007, PRIV-004 | AIR-011 (Bias Proxy Check) | None for MVP; bias proxy check deferred to STRETCH |
| STK-013 | System Admin | FR-035 to FR-038 (Auth + RBAC), FR-046 to FR-049 (Synthetic Data), SEC-001 to SEC-009 | â€” | None for MVP |

### 5.2 Coverage Heat Map

| Stakeholder Group | Requirements Met | Requirements Deferred | Coverage % |
|-------------------|-----------------|----------------------|------------|
| Primary Users (IO + SHO) | 30 FRs | 2 FRs (FR-006, FR-020) | 94% |
| Analysts (SCRB + SP) | 24 FRs | 1 FR (FR-020) | 96% |
| Governance (Compliance + Admin) | 18 FRs | 0 FRs | 100% |
| Specialized (Cyber, Forensics, Judiciary) | 0 FRs | â€” | 0% (VISION) |

---

## 6. Test Coverage by Requirement

Maps every functional requirement to its corresponding test cases across all test tiers.

### 6.1 Functional Requirement Test Coverage

| FR ID | Title | Unit Tests | Integration Tests | Acceptance Tests | Security Tests |
|-------|-------|-----------|-------------------|-----------------|---------------|
| FR-001 | FIR Structured Import | â€” | TC-INT-001, TC-INT-002 | â€” | â€” |
| FR-002 | FIR Manual Entry | â€” | â€” | â€” | â€” |
| FR-003 | Data Validation | â€” | TC-INT-001 | â€” | â€” |
| FR-004 | Duplicate Detection | â€” | TC-INT-002 | â€” | â€” |
| FR-005 | English NER | TC-NER-001 to TC-NER-005 | TC-INT-001 | â€” | â€” |
| FR-006 | Kannada NER | â€” | â€” | â€” | â€” |
| FR-007 | Confidence Scoring | TC-NER-001 to TC-NER-005 | â€” | â€” | â€” |
| FR-008 | Entity Linking | TC-NER-001 to TC-NER-005 | TC-INT-001 | â€” | â€” |
| FR-009 | PersonEntity Identity | TC-ER-001 to TC-ER-008 | TC-INT-003 | TC-AT-001 | â€” |
| FR-010 | Blocking Strategy | TC-ER-001 to TC-ER-008 | â€” | â€” | â€” |
| FR-011 | Similarity Scoring | TC-ER-001 to TC-ER-008 | â€” | â€” | â€” |
| FR-012 | Match Thresholds | TC-ER-008 | â€” | â€” | â€” |
| FR-013 | Manual Review | â€” | TC-INT-003 | TC-AT-001 | â€” |
| FR-014 | Merge Approval | â€” | â€” | TC-AT-001 | â€” |
| FR-015 | Provenance Tracking | TC-ER-001 to TC-ER-008 | TC-INT-003 | â€” | â€” |
| FR-016 | RelationshipEdge Table | â€” | TC-INT-004 | TC-AT-002 | â€” |
| FR-017 | Graph Traversal | â€” | TC-INT-004 | TC-AT-002 | â€” |
| FR-018 | Graph Visualization | â€” | TC-INT-004 | TC-AT-002 | â€” |
| FR-019 | Vehicle Linking | â€” | TC-INT-004 | TC-AT-003 | â€” |
| FR-020 | MO Pattern Matching | â€” | â€” | â€” | â€” |
| FR-021 | Hotspot Map | â€” | TC-INT-005 | â€” | â€” |
| FR-022 | District Drill-Down | â€” | TC-INT-005 | â€” | â€” |
| FR-023 | Temporal Filter | â€” | TC-INT-005 | â€” | â€” |
| FR-024 | Anomaly Detection | TC-AD-001 to TC-AD-003 | â€” | TC-AT-004 | â€” |
| FR-025 | Anomaly Alert | TC-AD-001 to TC-AD-003 | â€” | TC-AT-004 | â€” |
| FR-026 | Risk Score Computation | TC-RS-001 to TC-RS-005 | TC-INT-007 | TC-AT-005 | TC-SEC-005 |
| FR-027 | Feature Importance | TC-RS-003 | TC-INT-007 | TC-AT-005 | â€” |
| FR-028 | Feature Exclusion | TC-RS-004 | â€” | â€” | TC-SEC-005 |
| FR-029 | Score Explainability | â€” | TC-INT-007 | â€” | â€” |
| FR-030 | RAG Query | â€” | TC-INT-006 | TC-AT-003 | TC-SEC-001, TC-SEC-002 |
| FR-031 | Source Citations | â€” | TC-INT-006 | â€” | â€” |
| FR-032 | Role-Based Filtering | â€” | TC-INT-006 | â€” | â€” |
| FR-033 | Insufficient Evidence Response | â€” | TC-INT-006 | â€” | â€” |
| FR-034 | Query Audit | â€” | TC-INT-006 | â€” | â€” |
| FR-035 | User Authentication | TC-AUTH-001 to TC-AUTH-004 | TC-INT-008 | TC-AT-006 | TC-SEC-004 |
| FR-036 | Role-Based Access | TC-RBAC-001 to TC-RBAC-004 | TC-INT-008 | TC-AT-006 | â€” |
| FR-037 | Jurisdiction Scoping | TC-RBAC-001, TC-RBAC-002 | â€” | TC-AT-006 | â€” |
| FR-038 | MFA Support | â€” | â€” | â€” | â€” |
| FR-039 | Person-Level Read Audit | â€” | TC-INT-008 | â€” | â€” |
| FR-040 | AI Output Audit | â€” | TC-INT-008 | â€” | â€” |
| FR-041 | Append-Only Log | â€” | TC-INT-008 | â€” | â€” |
| FR-042 | Audit Queryability | â€” | TC-INT-008 | â€” | â€” |
| FR-043 | Fairness Check | â€” | TC-INT-009 | TC-AT-005 | â€” |
| FR-044 | Role Restriction Check | â€” | â€” | TC-AT-005 | â€” |
| FR-045 | Fairness Dashboard | â€” | TC-INT-009 | TC-AT-005 | â€” |
| FR-046 | Synthetic Data Generation | â€” | â€” | â€” | â€” |
| FR-047 | Planted Patterns | â€” | â€” | TC-AT-001 to TC-AT-006 | â€” |
| FR-048 | Seeded Reproducibility | â€” | â€” | â€” | â€” |
| FR-049 | Synthetic Labeling | â€” | â€” | â€” | â€” |

### 6.2 Test Coverage Summary by Tier

| Test Tier | Total Tests | FRs Covered | FRs Not Covered | Coverage % |
|-----------|-------------|-------------|-----------------|------------|
| Unit Tests | 25 | FR-005, FR-007 to FR-015, FR-024, FR-025, FR-026 to FR-028, FR-035 to FR-037 | FR-001 to FR-004, FR-006, FR-016 to FR-023, FR-029 to FR-034, FR-038 to FR-045, FR-046 to FR-049 | 37% |
| Integration Tests | 9 | FR-001, FR-003 to FR-005, FR-008, FR-009, FR-013, FR-015 to FR-019, FR-021 to FR-023, FR-026, FR-027, FR-029 to FR-034, FR-035 to FR-037, FR-039 to FR-043, FR-045 | FR-002, FR-006, FR-010, FR-011, FR-012, FR-014, FR-020, FR-024, FR-025, FR-028, FR-038, FR-044, FR-046 to FR-049 | 67% |
| Acceptance Tests | 6 | FR-009, FR-013 to FR-019, FR-024 to FR-027, FR-030, FR-035 to FR-037, FR-043 to FR-045, FR-047 | Most non-integration FRs | 35% |
| Security Tests | 5 | FR-026, FR-028, FR-030, FR-035 | â€” | 10% |

### 6.3 Security & Privacy Test Mapping

| Security/Privacy ID | Title | Test Cases | Verification Point |
|---------------------|-------|------------|-------------------|
| SEC-001 | Encryption at Rest | â€” | Platform capability (Catalyst-managed) |
| SEC-002 | Encryption in Transit | â€” | TLS enforced at API Gateway |
| SEC-003 | API Gateway | TC-AUTH-001 to TC-AUTH-004 | Token validation at gateway |
| SEC-004 | Input Validation | TC-SEC-001, TC-SEC-002, TC-SEC-003 | SQL injection, XSS rejection |
| SEC-005 | Parameterized Queries | TC-SEC-001, TC-SEC-002 | Query execution without injection |
| SEC-006 | Secrets Management | â€” | Code review for hardcoded secrets |
| SEC-007 | CasteID Role Restriction | TC-RBAC-003, TC-RBAC-004, TC-SEC-005 | 403 on restricted field access |
| SEC-008 | Rate Limiting | â€” | Platform capability |
| SEC-009 | Session Management | TC-AUTH-002, TC-AUTH-003, TC-SEC-004 | Timeout and token expiry |
| PRIV-001 | No Real PII in Demo | â€” | Synthetic generation verification |
| PRIV-002 | Synthetic Labeling | â€” | Label field inspection |
| PRIV-003 | Data Minimization | â€” | Code review of data collection |
| PRIV-004 | Caste/Religion Governance | TC-RS-004, TC-AT-005, TC-SEC-005 | Feature exclusion + RBAC |
| PRIV-005 | Audit Proportionality | â€” | Audit log field review |

---

## 7. Demo Evidence Traceability

Maps every demo scenario to the features, requirements, and test cases that prove it works.

### 7.1 MVP Demo Scenarios

| Demo # | Scenario | Feature | FR | Key Observation | Test Case Evidence | Success Criteria |
|--------|----------|---------|-----|----------------|-------------------|-----------------|
| DEMO-01 | FIR Import | FIR Structured Import | FR-001, FR-003, FR-004 | "Upload" button loads 2000+ synthetic FIRs; validation badges appear; duplicates flagged | TC-INT-001, TC-INT-002 | No data patches mid-demo |
| DEMO-02 | Entity Extraction | English NER | FR-005, FR-007, FR-008 | FIR detail shows PERSON, VEHICLE, LOCATION entities highlighted with confidence % | TC-NER-001 to TC-NER-005 | Entities visible and scored |
| DEMO-03 | Person Resolution | Entity Resolution | FR-009 to FR-015 | Search "Venkatesh" â†’ all 4 name variants resolve to 1 PersonEntity with 4 linked cases | TC-ER-001 to TC-ER-008, TC-INT-003, TC-AT-001 | Planted 4â†’1 match confirmed |
| DEMO-04 | Hidden Link Graph | Relationship Graph + Hidden Links | FR-016 to FR-018 | Click person â†’ force-directed graph shows co-accused cluster; shortest-path reveals hidden link | TC-INT-004, TC-AT-002 | Hidden link visible in graph |
| DEMO-05 | Hotspot Drill-Down | Geospatial Hotspot | FR-021 to FR-023 | Hexbin map loads; click district â†’ station-level drill-down works; date filter updates tiles | TC-INT-005 | Map renders with drill-down |
| DEMO-06 | Risk Score + Explainability | Risk Scoring | FR-026 to FR-029 | Person detail shows score bar + feature importance pie; CasteID absent from features | TC-RS-001 to TC-RS-005, TC-INT-007 | Score + feature importance visible |
| DEMO-07 | Anomaly Spike Alert | Anomaly Detection | FR-024, FR-025 | Dashboard alert badge shows "5x spike" in designated district/week; details show z-score | TC-AD-001 to TC-AD-003, TC-AT-004 | Spike alert visible |
| DEMO-08 | RAG Cited Answer | RAG Query | FR-030 to FR-034 | Type "How many FIRs in Bengaluru Urban?" â†’ answer with 3 source document citations | TC-INT-006, TC-SEC-001, TC-SEC-002 | Cited answer displayed |
| DEMO-09 | Role Switching | Auth + RBAC | FR-035 to FR-038 | Login as Investigator â†’ sees only district data; switch to Compliance â†’ sees CasteID; cross-district attempt returns 403 | TC-AUTH-001 to TC-AUTH-004, TC-RBAC-001 to TC-RBAC-004, TC-AT-006 | Role switch works cleanly |
| DEMO-10 | Audit Trail | Audit Logging | FR-039 to FR-042 | Audit viewer shows who read which person; RAG queries logged; append-only verified | TC-INT-008 | Audit log searchable |
| DEMO-11 | Fairness Check | Fairness Verification | FR-043 to FR-045 | Fairness dashboard shows green "PASS" for feature exclusion + role restriction checks | TC-INT-009, TC-AT-005 | Dashboard green |

### 7.2 Demo Script Flow

```
Phase 1: DATA FOUNDATION (DEMO-01)
  â”œâ”€ Upload synthetic Excel â†’ 2000+ FIRs ingested
  â”œâ”€ Validation badges, duplicate flagging
  â””â”€ Tables populated: src_CaseMaster, src_AccusedDetails, etc.

Phase 2: INTELLIGENCE LAYER (DEMO-02 â†’ DEMO-04)
  â”œâ”€ Open FIR detail â†’ NER entities highlighted (DEMO-02)
  â”œâ”€ Search "Venkatesh" â†’ 4â†’1 resolution with confidence (DEMO-03)
  â””â”€ Click PersonEntity â†’ relationship graph with hidden link (DEMO-04)

Phase 3: ANALYTICS (DEMO-05 â†’ DEMO-07)
  â”œâ”€ Switch to hotspot map â†’ state hexbin â†’ drill to district (DEMO-05)
  â”œâ”€ Click person â†’ risk score with feature breakdown (DEMO-06)
  â””â”€ Dashboard anomaly badge â†’ spike detail with magnitude (DEMO-07)

Phase 4: NATURAL LANGUAGE (DEMO-08)
  â””â”€ "Ask Berunda" â†’ cited answer with source documents

Phase 5: GOVERNANCE (DEMO-09 â†’ DEMO-11)
  â”œâ”€ Login as Investigator â†’ district-scoped view (DEMO-09)
  â”œâ”€ Switch to Compliance â†’ audit log search (DEMO-10)
  â””â”€ Fairness dashboard green; CasteID 403 for non-Compliance (DEMO-11)
```

---

## 8. Roadmap Phase Traceability

Maps features, requirements, and components to their delivery phases.

### 8.1 Phase 1 â€” Hackathon MVP (11 Days)

| Feature Group | FRs | Components | Demo Evidence |
|--------------|-----|-----------|--------------|
| Data Ingestion + NER | FR-001 to FR-008 | Ingestion Function, NER Function | DEMO-01, DEMO-02 |
| Entity Resolution | FR-009 to FR-015 | Entity Resolution Function, ER UI | DEMO-03 |
| Relationship Graph | FR-016 to FR-019 | AppSail NetworkX, Graph UI | DEMO-04 |
| Geospatial + Temporal | FR-021 to FR-023 | Hotspot Function, Slate Map | DEMO-05 |
| Anomaly Detection | FR-024, FR-025 | Anomaly Function | DEMO-07 |
| Risk Scoring | FR-026 to FR-029 | QuickML AutoML, Risk UI | DEMO-06 |
| RAG Query | FR-030 to FR-034 | QuickML LLM, RAG Function | DEMO-08 |
| Auth + RBAC | FR-035 to FR-038 | Catalyst Auth, API Gateway | DEMO-09 |
| Audit Logging | FR-039 to FR-042 | Audit Function, Audit UI | DEMO-10 |
| Fairness | FR-043 to FR-045 | Fairness Function, Fairness UI | DEMO-11 |
| Synthetic Data | FR-046 to FR-049 | DataGen Function | DEMO-01 (precondition) |

### 8.2 Phase 2 â€” Post-Hackathon (3 Months)

| Feature Group | FRs | Components | Rationale |
|--------------|-----|-----------|-----------|
| Kannada NLP | FR-006, AIR-008 | NER Function (IndicNLP) | Bilingual mandate |
| MO Fingerprinting | FR-020, AIR-009 | MO Embedding Function | Key investigative gap |
| Chain-of-Custody Hashing | FR-040 (extended) | Audit Function (SHA-256) | Tamper evidence |
| OpenStreetMap Enrichment | FR-021 (extended) | Hotspot Function | Better location context |
| Push Notifications | FR-025 (extended) | Notification Function | Proactive alerting |
| CSV/PDF Report Export | FR-042 (extended) | Report Function | Operational need |
| Multi-Language RAG | FR-030 (extended) | RAG Function | Full bilingual support |
| SC/ST Aggregate Report | UC-014 | Reporting Function | Statutory requirement |

### 8.3 Phase 3 â€” Enterprise Scale (6 Months)

| Feature Group | Description | Target |
|--------------|-------------|--------|
| Event-Driven Architecture | Replace polling with event triggers | Scalability |
| Neo4j Graph Migration | Move RelationshipEdge to native graph DB | Performance at scale |
| CQRS Pattern | Separate read/write models | Query performance |
| OSINT Integration | Web scraping + social media correlation | Cyber crime |
| Real CCTNS Integration | API-level connection to production CCTNS | Live data feed |
| Advanced Analytics | Time-series forecasting, recidivism modeling | Predictive intelligence |

### 8.4 Phase 4 â€” Intelligence Platform (12 Months)

| Feature Group | Description | Target |
|--------------|-------------|--------|
| Multi-Modal AI | Image analysis (crime scene photos), audio transcription | Rich evidence processing |
| Voice Intake | Telephone FIR registration via speech-to-text | Citizen accessibility |
| Blockchain Audit Trail | Distributed ledger for chain-of-custody | Tamper-proof evidence |
| Cross-State Correlation | National-level crime pattern matching | Federal intelligence |
| Mobile App | Field access for IOs | Operational mobility |

---

## 9. Gap Analysis

Identifies requirements, entities, and stakeholders with insufficient coverage.

### 9.1 Coverage Gaps

| Gap ID | Area | Gap Description | SeverITY | Mitigation |
|--------|------|-----------------|----------|------------|
| GAP-001 | Test Coverage | FR-002 (Manual Entry) has zero test cases | LOW | Manual entry is secondary; accept for MVP |
| GAP-002 | Test Coverage | FR-006 (Kannada NER) has zero test cases | MEDIUM | Deferred to Phase 2; no test needed now |
| GAP-003 | Test Coverage | FR-020 (MO Matching) has zero test cases | MEDIUM | Deferred to STRETCH; no test needed now |
| GAP-004 | Test Coverage | FR-046 to FR-049 (Synthetic Data) have no dedicated tests | LOW | Covered implicitly by all demo scenarios using synthetic data |
| GAP-005 | Test Coverage | No unit tests for Geospatial (FR-021 to FR-023) | LOW | Integration tests cover core functionality |
| GAP-006 | Test Coverage | No unit tests for Audit (FR-039 to FR-042) | LOW | Integration tests cover audit trail |
| GAP-007 | Test Coverage | No unit tests for RAG (FR-030 to FR-034) | LOW | Integration + security tests cover RAG |
| GAP-008 | Test Coverage | No unit tests for FIR Import (FR-001 to FR-004) | LOW | Integration tests cover import flow |
| GAP-009 | Stakeholder | STK-005 (Cyber Crime) â€” no requirements | VISION | Intentional; OSINT is VISION-scope |
| GAP-010 | Stakeholder | STK-006 (Forensic Labs) â€” no requirements | VISION | Intentional; evidence tracking is VISION-scope |
| GAP-011 | Stakeholder | STK-007 (Judiciary) â€” no requirements | VISION | Intentional; court access is VISION-scope |
| GAP-012 | Security | SEC-001, SEC-006, SEC-008 have no automated tests | MEDIUM | Platform capabilities; verify via documentation review |
| GAP-013 | Data | DR-007 (Schema Separation) has no verification test | LOW | Architectural constraint; verify via schema inspection |
| GAP-014 | AI | AIR-010 (Drift Monitoring), AIR-011 (Bias Proxy Check) not implemented | SHOULD | Accept for MVP; add in Phase 2 |
| GAP-015 | Demo | MFA (FR-038) may not be demonstrable in hackathon environment | LOW | Accept; document as "not shown due to time" |

### 9.2 Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Test gaps in manual entry (FR-002) could hide UX bugs | LOW | LOW | Manual QA during demo rehearsal |
| No unit tests for core pipeline (FR-001 to FR-004) | MEDIUM | LOW | Integration tests cover end-to-end |
| Stakeholder gaps for Cyber, Forensics, Judiciary | LOW | N/A | Intentional scope decision documented |
| MFA not demoable | LOW | MEDIUM | Alternative: show MFA config screen |

---

## 10. Change Impact Analysis

When a requirement or component changes, use this section to determine the full blast radius.

### 10.1 Impact Vectors

| Change | Affected FRs | Affected Tests | Affected Demos | Affected Roadmap |
|--------|-------------|----------------|----------------|-------------------|
| Modify NER model/spaCy pipeline | FR-005, FR-007, FR-008 | TC-NER-001 to TC-NER-005, TC-INT-001 | DEMO-02 | Phase 1 |
| Change entity resolution threshold logic | FR-011, FR-012 | TC-ER-001 to TC-ER-008, TC-INT-003, TC-AT-001 | DEMO-03 | Phase 1 |
| Replace QuickML AutoML with different ML service | FR-026 to FR-029 | TC-RS-001 to TC-RS-005, TC-INT-007, TC-AT-005, TC-SEC-005 | DEMO-06 | Phase 1 |
| Change API Gateway provider | FR-035 to FR-038 | TC-AUTH-001 to TC-AUTH-004, TC-RBAC-001 to TC-RBAC-004, TC-INT-008, TC-AT-006 | DEMO-09 | Phase 1 |
| Add new data entity to schema | DR-001 to DR-007 | Affected function tests | â€” | Phase specific |
| Remove CasteID/ReligionID columns | SEC-007, PRIV-004, FR-028, FR-043, FR-044 | TC-RS-004, TC-AT-005, TC-SEC-005 | DEMO-06, DEMO-11 | Phase 1 |

---

## 11. Revision History

| Version | Date | Author | Change Description |
|---------|------|--------|-------------------|
| 1.0 | 2026-07-17 | Berunda Team | Initial traceability chain â€” complete MVP trace |

---

*End of Traceability Chain Document (BERUNDA-REP-004)*
