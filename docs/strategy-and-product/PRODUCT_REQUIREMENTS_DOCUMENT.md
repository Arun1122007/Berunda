# Product Requirements Document

[//]: # (Document ID: BERUNDA-PRD-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team | Source: 01_Enterprise_Blueprint | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Product Vision

Project Berunda is an AI-native crime intelligence platform that sits on top of Karnataka State Police's existing FIR system as an intelligence layer. It does not replace CCTNS — it adds cross-case entity resolution, explainable risk analytics, geospatial hotspot detection, relationship graph analysis, and grounded natural-language investigation assistance that the current system-of-record cannot provide.

## 2. Jobs to Be Done

| JTBD | Current Solution | Berunda Solution |
|------|-----------------|-----------------|
| "Connect this suspect to other cases" | Manual Excel search across stations | Automated entity resolution with confidence scoring |
| "See crime patterns in my jurisdiction" | Pivot tables and manual charting | Interactive hotspot map and trend dashboard |
| "Find hidden links between cases" | Manual cross-referencing of case files | Graph traversal showing relationship paths |
| "Get a quick answer about case data" | File a request to the data team | Natural-language query with cited answers |
| "Verify the AI is fair" | No tooling available | Live fairness audit dashboard |

## 3. Features and Prioritization

### MVP Features (MUST — BUILDABLE)

| ID | Feature | Epic | Estimate (days) | Dependencies |
|----|---------|------|----------------|--------------|
| F-001 | Synthetic FIR import + schema migration | Data Ingestion | 1 | Data Store provisioned |
| F-002 | English NER entity extraction | Entity Resolution | 1 | F-001, spaCy model |
| F-003 | Cross-case PersonEntity resolution | Entity Resolution | 2 | F-002 |
| F-004 | Relationship graph + hidden-link UI | Link Analysis | 2 | F-003 |
| F-005 | Geospatial hotspot map | Analytics | 1 | F-001 |
| F-006 | Explainable risk scoring | AI/ML | 1 | F-003, QuickML |
| F-007 | Anomaly/spike detection | Analytics | 1 | F-001 |
| F-008 | "Ask Berunda" RAG | AI/ML | 1 | QuickML configured |
| F-009 | Auth + RBAC (3 roles) | Security | 1 | Catalyst Auth |
| F-010 | Audit logging | Security | 1 | AuditLog table |
| F-011 | Live fairness check | Governance | 1 | F-006, F-009 |
| F-012 | Demo evidence pack | Delivery | 1 | All of the above |

### Stretch Features (SHOULD — STRETCH)

| ID | Feature | Epic | Dependencies |
|----|---------|------|--------------|
| F-013 | Kannada NER (AI4Bharat) | Entity Resolution | AI4Bharat model |
| F-014 | MO fingerprinting (embedding similarity) | Link Analysis | sentence-transformers |
| F-015 | Chain-of-custody hash demo | Evidence | Evidence table |
| F-016 | OSM Overpass location enrichment | Analytics | OSM API |
| F-017 | SmartBrowz PDF report generation | Delivery | SmartBrowz |

### Vision Features (WONT-NOW — VISION)

| ID | Feature | Target Phase |
|----|---------|-------------|
| F-018 | Full Kannada NLP pipeline | Phase 2 |
| F-019 | Real CCTNS data bridge | Phase 2 |
| F-020 | OSINT monitoring | Phase 4 |
| F-021 | Cross-state correlation | Phase 5 |
| F-022 | Neo4j graph database migration | Phase 3 |
| F-023 | Event-driven architecture (Signals/Circuits) | Phase 3 |
| F-024 | ABAC access control | Phase 3 |
| F-025 | Voice / speech FIR intake | Phase 2 |
| F-026 | Push notifications | Phase 2 |

## 4. Out-of-Scope Items (Explicit)

| Item | Reason |
|------|--------|
| Individual criminality prediction | Ethically unacceptable; prohibited by design |
| Autonomous watchlist/arrest decisions | Human-in-the-loop always required |
| Real person-level data in demo | Synthetic data only unless authorized |
| Caste/religion-based model features | Hard-excluded by design |
| Full audit-blockchain integration | Phase 3+ target; hash chain sufficient for MVP |
| Mobile native app | Catalyst Slate/Web is responsive; mobile app deferred |

## 5. Assumptions

| # | Assumption | Impact if Wrong |
|---|------------|-----------------|
| 1 | Catalyst platform is available and provisioned before Day 1 | Cannot start without access |
| 2 | QuickML supports required AI capabilities | Architecture redesign needed |
| 3 | Synthetic data is acceptable for judging | Demo may lack authenticity |
| 4 | 11 days is sufficient for the 12 MVP features | Scope must be cut |
| 5 | Team of 2 can work effectively in parallel | Bottlenecks on shared components |

## 6. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Demo completion | End-to-end passes without mid-demo patches | Recorded demo run |
| Entity resolution accuracy | Planted repeat-offender correctly linked across 4 cases | Acceptance test pass |
| Risk score explainability | Feature-importance breakdown visible for every score | UI check |
| Fairness verification | Caste/religion exclusion confirmed programmatically | Fairness check output |
| Catalyst compliance | Every service mapped to a requirement | Compliance table verified |
| RAG answer quality | 3/3 rehearsed questions return grounded, cited answers | Demo run |
