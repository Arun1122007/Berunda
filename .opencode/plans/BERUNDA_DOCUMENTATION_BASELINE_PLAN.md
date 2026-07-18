# Project Berunda — Documentation Baseline Generation Plan

**Plan ID:** PLAN-001
**Status:** Ready for Execution
**Owner:** Phoenix Coder
**Created:** 2026-07-16

---

## 0. Preflight Summary (Completed)

### Source Inventory (12 files)

| # | File | Lines | Classification |
|---|------|-------|----------------|
| 1 | Project_Berunda_01_Enterprise_Blueprint.md | 866 | **Canonical** |
| 2 | project_berunda_blueprint_new.md | 864 | **Near-duplicate** |
| 3 | project_berunda_blueprint.md | 759 | **Historical v1** |
| 4 | CaseGraph_Datathon2026_Blueprint.md | 347 | **Precursor concept** |
| 5 | Project_Berunda_02_Hackathon_Pitch.md | 66 | **Supporting** |
| 6 | Project_Berunda_03_Implementation_Plan.md | 117 | **Supporting** |
| 7 | Project_Berunda_04_Complete_Roadmap.md | 137 | **Supporting** |
| 8 | Project_Berunda_05_Database_ER_Reference.md | 221 | **Supporting** |
| 9 | Project_Berunda_06_Resource_Acquisition_Blueprint.md | 293 | **Supporting** |
| 10 | Project_Berunda_07_Autonomous_Agent_Prompt.md | 251 | **Supporting** |
| 11 | Project_Berunda_08_NotebookLM_Research_Prompt.md | 138 | **Supporting** |
| 12 | Police_FIR_ER_Diagram.pdf | PDF | **Primary source** |

### ERD Key Resolutions

- **Inv_OccuranceTime**: Confirmed separate 1:1 table (relationship matrix), NOT a CaseMaster continuation
- **inv_arrestsurrenderaccused**: Referenced in relationship matrix, NO table definition in PDF (GAP-001)
- **27+ tables confirmed** from PDF: CaseMaster, Inv_OccuranceTime, ComplainantDetails, Victim, Accused, ArrestSurrender, ActSectionAssociation, Act, Section, CrimeHeadActSection, CrimeHead, CrimeSubHead, CasteMaster, ReligionMaster, OccupationMaster, CaseStatusMaster, Court, District, State, Unit, UnitType, Rank, Designation, Employee, CaseCategory, GravityOffence, ChargesheetDetails

---

## 1. Architecture Decisions (ADR Index)

| ADR | Title | Phase 1 Decision |
|-----|-------|-----------------|
| ADR-001 | Phase 1 Architectural Style | Modular Functions + API Gateway (NO event-driven, NO full microservices) |
| ADR-002 | Catalyst Deployment Boundaries | All services within Catalyst |
| ADR-003 | Source-of-Record vs Intelligence Layer | Separate schemas (source tables vs Berunda extensions) |
| ADR-004 | Graph Representation | Relational join tables (no Neo4j until Phase 3+) |
| ADR-005 | Entity Resolution Approach | Rule-based blocking + weighted similarity |
| ADR-006 | RAG and NL Query Safety | Retrieval-before-generation; parameterized templates; cited answers |
| ADR-007 | Sensitive Field Exclusion | Hard exclusion of CasteID/ReligionID from all models |
| ADR-008 | MVP vs Target State | BUILDABLE only; STRETCH deferred |

---

## 2. Document Generation Plan

### ~50 files across 12 directories

`
README.md

docs/00_START_HERE.md
docs/00_DOCUMENT_CONTROL.md
docs/00_GLOSSARY.md

docs/01_DISCOVERY/
  SOURCE_INVENTORY_AND_AUTHORITY.md
  CONTRADICTION_ASSUMPTION_AND_GAP_REGISTER.md
  EXTERNAL_CLAIM_VERIFICATION_REGISTER.md
  INFORMATION_CLASSIFICATION_AND_PUBLICATION_PLAN.md

docs/02_STRATEGY_AND_PRODUCT/
  PROJECT_CHARTER.md
  EXECUTIVE_SUMMARY.md
  PROBLEM_STAKEHOLDERS_AND_PERSONAS.md
  PRODUCT_REQUIREMENTS_DOCUMENT.md
  USE_CASE_CATALOG.md
  MVP_SCOPE_AND_RELEASE_PLAN.md
  SUCCESS_METRICS_AND_BENEFITS_REALIZATION.md

docs/03_REQUIREMENTS/
  SOFTWARE_REQUIREMENTS_SPECIFICATION.md
  NON_FUNCTIONAL_REQUIREMENTS.md
  REQUIREMENTS_TRACEABILITY_MATRIX.md
  ACCEPTANCE_CRITERIA_AND_DEFINITION_OF_DONE.md

docs/04_ARCHITECTURE/
  SYSTEM_CONTEXT_AND_CONTAINER_ARCHITECTURE.md
  HIGH_LEVEL_DESIGN.md
  LOW_LEVEL_DESIGN.md
  CATALYST_SERVICE_MAPPING.md
  INTEGRATION_AND_EVENT_ARCHITECTURE.md
  ARCHITECTURE_DECISION_RECORD_INDEX.md
  ADR/ADR-001 through ADR-008

docs/05_DATA/
  DATA_ARCHITECTURE.md
  SOURCE_ERD_RECONCILIATION.md
  CANONICAL_DATA_MODEL.md
  DATA_DICTIONARY.md
  ENTITY_RESOLUTION_SPECIFICATION.md
  SYNTHETIC_DATA_SPECIFICATION.md
  DATA_QUALITY_PROFILING_AND_VALIDATION_PLAN.md
  DATA_GOVERNANCE_RETENTION_AND_PROVENANCE.md

docs/06_AI_AND_ANALYTICS/
  AI_ML_SYSTEM_SPECIFICATION.md
  ANALYTICS_FEATURE_CATALOG.md
  MODEL_EVALUATION_AND_MLOPS_PLAN.md
  RAG_KNOWLEDGE_BASE_AND_GROUNDING_SPEC.md
  MODEL_AND_DATA_CARD_TEMPLATES.md
  RESPONSIBLE_AI_AND_HUMAN_OVERSIGHT.md

docs/07_API_AND_CONTRACTS/
  API_DESIGN_SPECIFICATION.md
  ERROR_AUTHORIZATION_AND_AUDIT_CONTRACTS.md
  EVENT_AND_JOB_CONTRACTS.md

docs/08_SECURITY_PRIVACY_GOVERNANCE/
  SECURITY_ARCHITECTURE.md
  THREAT_MODEL.md
  ACCESS_CONTROL_MATRIX.md
  PRIVACY_IMPACT_ASSESSMENT.md
  AI_IMPACT_ASSESSMENT.md
  AUDIT_LOGGING_AND_EVIDENCE_INTEGRITY.md
  INCIDENT_RESPONSE_AND_BREACH_PLAYBOOK.md

docs/09_QUALITY/
  TEST_STRATEGY.md
  TEST_CASE_CATALOG.md
  PERFORMANCE_RELIABILITY_AND_ACCESSIBILITY_PLAN.md
  DEMO_DATA_AND_EVIDENCE_VALIDATION_PLAN.md

docs/10_DEVSECOPS_AND_OPERATIONS/
  ENVIRONMENT_AND_DEPLOYMENT_STRATEGY.md
  CICD_AND_RELEASE_MANAGEMENT.md
  OBSERVABILITY_AND_MODEL_MONITORING.md
  BACKUP_DISASTER_RECOVERY_AND_BUSINESS_CONTINUITY.md
  OPERATIONS_RUNBOOK.md

docs/11_DELIVERY/
  IMPLEMENTATION_PLAN.md
  PRIORITIZED_PRODUCT_BACKLOG.md
  RISK_REGISTER.md
  HACKATHON_DEMO_AND_PITCH_PLAN.md
  SUBMISSION_READINESS_CHECKLIST.md
  ENTERPRISE_ROADMAP.md

docs/12_OPEN_SOURCE_AND_ASSURANCE/
  OPEN_SOURCE_LICENSE_AND_ATTRIBUTION_STRATEGY.md
  CONTRIBUTING_GUIDE_DRAFT.md
  SECURITY_POLICY_DRAFT.md
  CODE_OF_CONDUCT_DRAFT.md

docs/99_REPORTS/
  DOCUMENTATION_COVERAGE_MATRIX.md
  DOCUMENTATION_QA_REPORT.md
  DOCUMENTATION_COMPLETION_REPORT.md
`

---

## 3. MVP Feature Cut (Frozen)

### ✅ MVP (MUST — BUILDABLE, 11 days)
1. Synthetic FIR import/intake (Faker generator)
2. English NER entity extraction from BriefFacts (spaCy → Function)
3. Cross-case PersonEntity resolution (blocking + weighted similarity)
4. Case/person relationship graph + hidden-link demo (NetworkX in AppSail)
5. Geospatial hotspot map + drill-down (KDE/hexbin aggregation)
6. Explainable risk score with feature importance (QuickML AutoML)
7. Anomaly/spike detection (z-score deviation)
8. "Ask Berunda" RAG over synthetic corpus (QuickML LLM + RAG)
9. Auth + RBAC (Catalyst Authentication, 3 roles)
10. Audit logging for sensitive reads + AI outputs (append-only AuditLog)
11. Live fairness check (caste/religion exclusion verification)
12. Public-safe demo evidence pack

### 🧩 STRETCH (if ahead)
Kannada NER, MO fingerprinting, chain-of-custody hash, push notifications, OSM enrichment

### 🔭 VISION (documented, not built)
Kannada NLP full, OSINT, cross-state, Neo4j, event-driven, ABAC, blockchain, voice, multi-agent, 30-year backfill

---

## 4. Critical Gaps

| ID | Description | Impact |
|----|-------------|--------|
| GAP-001 | inv_arrestsurrenderaccused junction table: no column defs in PDF | Cannot complete schema |
| GAP-002 | Submission format not confirmed (video/link/repo/deck?) | Day 11 undefined |
| GAP-003 | Judging rubric not available | Cannot weight effort |
| GAP-004 | Catalyst credits not redeemed | Deployment blocked |
| GAP-005 | QuickML capabilities unverified against current docs | Architecture risk |

---

## 5. Execution Order

**Phase A**: Foundation (README, 00_DOCUMENT_CONTROL, 00_GLOSSARY, 00_START_HERE)
**Phase B**: Discovery (source inventory, gaps, classification)
**Phase C**: Strategy & Product (charter, PRD, personas, use cases)
**Phase D**: Requirements (SRS, NFRs, traceability)
**Phase E**: Architecture + ADRs (context, HLD, LLD, 8 ADRs)
**Phase F**: Data (ERD reconciliation, data model, dictionary, synthetic data spec)
**Phase G**: AI & Analytics (AI/ML spec, feature catalog, RAG spec)
**Phase H**: API & Contracts
**Phase I**: Security, Privacy, Governance
**Phase J**: Quality (test strategy, case catalog)
**Phase K**: DevSecOps & Operations
**Phase L**: Delivery (backlog, risk register, demo plan, roadmap)
**Phase M**: Open Source & Assurance
**Phase N**: QA Reports

---

## 6. Questions for You

Before I start execution, do you have any specific preferences or questions about the plan above?
