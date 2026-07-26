# MVP Scope and Release Plan

[//]: # (Document ID: BERUNDA-MVP-001 | Version: 1.1 | Status: APPROVED | Classification: INTERNAL | Owner: Berunda Team)

## MVP Definition
The Berunda MVP is a working, demoable slice that touches every architectural layer.

## MVP Feature Set (Frozen)

| Feature ID | Feature Name | Problem Solved | User Benefited | Source Doc | Business Value | Demo Value | Complexity | Data Dependency | AI Dependency | Security Implications | Catalyst Dependency | Priority | Final Scope |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | Synthetic FIR import | Lack of test data | Admin | PRD | High | High | Low | DB Schema | None | Low | Data Store | P0 | Must Have |
| F-002 | English NER extraction | Unstructured FIR | IO | PRD | High | High | High | Text | NLP | High | AppSail | P0 | Must Have |
| F-003 | Cross-case entity resolution | Data silos | IO | PRD | High | High | High | Entities | ML | High | AppSail | P0 | Must Have |
| F-004 | Relationship graph | No relationship intel | IO / Analyst | PRD | High | High | Med | Graph | None | Med | AppSail | P0 | Must Have |
| F-005 | Geospatial hotspot map | Reactive posture | SHO / SP | PRD | High | High | Med | Geo | None | Med | AppSail | P0 | Must Have |
| F-006 | Explainable risk score | Reactive posture | IO | PRD | Med | High | High | Entities | ML | High | AppSail | P0 | Must Have |
| F-007 | Anomaly detection | Reactive posture | SHO | PRD | High | Med | High | Geo | ML | Med | AppSail | P0 | Must Have |
| F-008 | Ask Berunda RAG | Slow retrieval | IO | PRD | High | High | High | DB | LLM | High | AppSail | P0 | Must Have |
| F-009 | Human review of AI | Need for human-reviewed AI | IO | PRD | High | High | Med | UI | LLM | High | AppSail | P0 | Must Have |
| F-010 | Auth + RBAC | Security | Admin | PRD | High | High | Med | DB | None | High | Auth | P0 | Must Have |
| F-011 | Audit logging | Incomplete auditability | Auditor | PRD | High | Low | Low | DB | None | High | Data Store | P0 | Must Have |
| F-012 | Fairness check | Governance | Auditor | PRD | High | Low | Med | DB | None | Med | AppSail | P0 | Must Have |
| F-013 | Cyber Crime OSINT | Missing external data | Cyber Cell | PRD | Med | Low | High | External | None | High | None | P2 | Could Have |
| F-014 | Chain-of-custody | Evidence tracking | Lab | PRD | Med | Low | Med | DB | None | High | None | P3 | Won\'t Have |

## 11-Day Release Plan
(Retained original plan for reference)
