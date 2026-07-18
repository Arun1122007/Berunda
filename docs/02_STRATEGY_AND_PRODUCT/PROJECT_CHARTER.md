# Project Berunda — Project Charter

[//]: # (Document ID: BERUNDA-CHTR-001 | Version: 1.0 | Status: DRAFT | Classification: PUBLIC | Owner: Berunda Team | Audience: Team | Source: 01_Enterprise_Blueprint | Last Verified: 2026-07-17 | Review: Monthly)

---

## Project Identity

| Field | Value |
|-------|-------|
| Project Name | Project Berunda |
| Tagline | AI-Native Crime Intelligence Operating System for Karnataka State Police |
| Team | Phoenix Coder (2 members) |
| Event | Karnataka State Police Datathon 2026 (Hack2Skill × KSP) |
| Duration | 11 days (hackathon) with documented enterprise roadmap |
| Mandatory Platform | Catalyst by Zoho |

## Mission

Give the Karnataka State Police and the State Crime Records Bureau one living, queryable picture of crime across the state — replacing fragmented Excel sheets with a system that connects every FIR, person, location, and case in real time, in both Kannada and English.

## Vision

Berunda is the open, Catalyst-native intelligence layer that sits on top of CCTNS and station records, adding cross-case relationship graphs, explainable predictive analytics with built-in bias auditing, and bilingual natural-language investigation support — none of which exist together in any single system available to Indian state police today.

## Objectives

| OBJ-ID | Objective | Priority |
|--------|-----------|----------|
| OBJ-001 | Deliver a working, demoable MVP within 11 days that demonstrates every architectural layer | MUST |
| OBJ-002 | Demonstrate cross-case entity resolution that connects persons across multiple FIRs | MUST |
| OBJ-003 | Provide explainable, bias-audited risk scoring as an alternative to black-box predictive policing | MUST |
| OBJ-004 | Enable natural-language investigation assistance via grounded RAG | MUST |
| OBJ-005 | Show live sensitive-feature governance and fairness verification | MUST |
| OBJ-006 | Fully comply with the mandatory Catalyst deployment requirement | MUST |
| OBJ-007 | Establish an open-core foundation that can scale from district to national deployment | SHOULD |

## Scope

### In Scope (MVP — BUILDABLE)

1. Synthetic FIR import and entity extraction (English)
2. Cross-case `PersonEntity` resolution with confidence scoring
3. Case/person relationship graph and hidden-link discovery
4. Geospatial hotspot map with district-to-station drill-down
5. Explainable risk scoring with feature-importance breakdown
6. Anomaly and spike detection against historical baselines
7. "Ask Berunda" grounded RAG over a curated case corpus
8. Role-based authentication and authorization (3 roles)
9. Audit logging for sensitive reads and AI-assisted outputs
10. Live sensitive-feature exclusion and fairness verification

### Out of Scope (Stretch or Vision)

- Kannada NLP (🧩 STRETCH)
- OSINT monitoring (🔭 VISION)
- Cross-state correlation (🔭 VISION)
- Graph database migration (🔭 VISION)
- Event-driven architecture (🔭 VISION)
- Real CCTNS integration (Phase 2+)
- Voice / speech interfaces (Phase 2+)
- Mobile app / push notifications (🧩 STRETCH)

## Key Stakeholders

| Stakeholder | Role |
|-------------|------|
| Investigating Officers (IOs) | Primary users — cross-referencing persons/vehicles/locations |
| Station House Officers (SHOs) | Local jurisdiction dashboard |
| SCRB | State-wide analytics and statutory reporting |
| District SPs | Resource deployment and hotspot monitoring |
| Judging Panel (Datathon) | Evaluators of technical depth, innovation, and compliance |

## Success Criteria

1. End-to-end demo completes without data patches mid-demo
2. Entity resolution correctly links a planted repeat-offender across 4 synthetic cases
3. Risk score is accompanied by a readable feature-importance breakdown
4. Fairness check confirms caste/religion fields are excluded from models and restricted by role
5. "Ask Berunda" returns grounded, cited answers to 3 rehearsed questions
6. Catalyst compliance table maps every service used to a requirement
