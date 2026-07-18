# Requirements Traceability Matrix

[//]: # (Document ID: BERUNDA-TRACE-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Architects, QA | Source: 01_Enterprise_Blueprint + SRS references | Last Verified: 2026-07-17 | Review: Monthly)

---

## Traceability Chain

Challenge Objective → Stakeholder Need → Use Case → Requirement → Architecture Component → Data Source → Security/Privacy Control → Test Case → Demo Evidence → Roadmap Phase

## Core Traceability

| Use Case | Functional Req | Data Req | AI Req | Security Req | Test | Demo Evidence | Scope |
|----------|---------------|----------|--------|-------------|------|--------------|-------|
| UC-001 (Ingest FIR) | FR-001, FR-003, FR-004 | DR-001, DR-005 | — | SEC-004 | TST-001 | Import shown with validation | MVP |
| UC-002 (Extract entities) | FR-005, FR-006, FR-007 | DR-006 | AIR-001 | — | TST-002 | NER output visible on FIR detail | MVP |
| UC-003 (Resolve person) | FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015 | DR-002 | — | SEC-007 | TST-003 | Cross-case match shown | MVP |
| UC-004 (View graph) | FR-016, FR-017, FR-018 | DR-002 | — | — | TST-004 | Force-directed graph renders | MVP |
| UC-005 (Hidden links) | FR-017, FR-018 | DR-002 | — | — | TST-005 | Path between entities shown | MVP |
| UC-006 (Hotspot map) | FR-021, FR-022, FR-023 | DR-001 | AIR-003 | — | TST-006 | Hexbin layer renders, drill-down works | MVP |
| UC-007 (Temporal analysis) | FR-023 | DR-001, DR-003 | — | — | TST-007 | Charts update with filters | MVP |
| UC-008 (Risk score) | FR-026, FR-027, FR-028, FR-029 | DR-002 | AIR-002, AIR-006 | SEC-001, SEC-002 | TST-008 | Score + feature importance visible | MVP |
| UC-009 (Anomaly detection) | FR-024, FR-025 | DR-001 | AIR-004 | — | TST-009 | Alert marker shown | MVP |
| UC-010 (Ask Berunda) | FR-030, FR-031, FR-032, FR-033, FR-034 | — | AIR-005 | SEC-003 | TST-010 | Cited answer displayed | MVP |
| UC-011 (Auth) | FR-035, FR-036, FR-037, FR-038 | — | — | SEC-001 to SEC-009 | TST-011 | Role-switching demo | MVP |
| UC-012 (Audit) | FR-039, FR-040, FR-041, FR-042 | DR-002 | — | SEC-005 | TST-012 | Audit log searchable | MVP |
| UC-013 (Fairness) | FR-043, FR-044, FR-045 | — | AIR-007 | SEC-007, PRIV-004 | TST-013 | Fairness check green | MVP |
| UC-014 (SC/ST report) | — | DR-004 | — | SEC-007, PRIV-004 | TST-014 | Aggregate report generated | STRETCH |
| UC-015 (State command) | FR-023 | DR-001 | — | SEC-003 | TST-015 | State-level KPI dashboard | MVP |

## Requirements-to-Architecture Mapping

| Architecture Component | Requirements Served |
|----------------------|-------------------|
| Catalyst Data Store | FR-001, FR-002, FR-003, DR-001, DR-002, DR-003 |
| Catalyst Functions | FR-005, FR-010, FR-011, FR-024, AIR-001 |
| Catalyst AppSail | FR-017, FR-026, FR-027, AIR-002 |
| Catalyst QuickML | FR-026, FR-027, FR-030, AIR-002, AIR-005, AIR-006 |
| Catalyst Authentication | FR-035, FR-036, FR-038 |
| Catalyst API Gateway | SEC-003, SEC-008 |
| Catalyst Slate | FR-018, FR-021, FR-022, FR-045 |
| AuditLog (Data Store) | FR-039, FR-040, FR-041, FR-042 |
| RiskScore (Data Store) | FR-026, FR-027 |
| PersonEntity (Data Store) | FR-009, FR-015 |

## Requirements-to-Test Mapping

| Requirement | Test Case(s) |
|-------------|-------------|
| FR-001 (FIR Import) | TST-001, TST-002 |
| FR-005 (English NER) | TST-003 |
| FR-009 (PersonEntity) | TST-004, TST-005 |
| FR-021 (Hotspot Map) | TST-010 |
| FR-026 (Risk Score) | TST-012 |
| FR-030 (RAG Query) | TST-015 |
| FR-035 (Auth) | TST-017 |
| FR-039 (Audit) | TST-019 |
| FR-043 (Fairness) | TST-021 |
