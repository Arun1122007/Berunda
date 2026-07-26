# 01 — Problem Statement and Product Vision

**Document ID:** BERUNDA-PH1-VISION-001
**Version:** 1.0 | **Status:** APPROVED — Authoritative Phase 1 product definition
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This document defines what problem Project Berunda solves, for whom, why it matters,
> and what measurable outcomes the hackathon product must create.
> Every proposed feature in the project must trace back to a problem in this document.

---

## 1. Executive Summary

Karnataka's district police stations generate FIRs (First Information Reports) that contain rich, unstructured information about persons, vehicles, locations, legal sections, and circumstances. Today, each FIR exists as an isolated record. A suspect appearing in five FIRs across three districts looks like five unrelated cases because no system cross-references persons, vehicles, or locations across the corpus.

Project Berunda is a **structured information extraction and investigation-support platform** that converts raw FIR text into a queryable, connected intelligence layer. It helps officers register FIRs with AI assistance, enables investigators to discover cross-case connections, provides supervisors with jurisdiction-level situational awareness, and gives analysts access to explainable, bias-audited analytics — all within a responsible-AI framework that keeps every decision in human hands.

**This document is the single source of truth for product scope.** Features not traceable to a problem statement in this document are out of scope.

---

## 2. Background

### 2.1 Context

The Hack2Skill × Karnataka State Police (KSP) Datathon 2026 challenges teams to build an AI-driven crime analytics and visualisation platform on Zoho Catalyst. The Karnataka State Crime Records Bureau (SCRB) collects crime data from district police stations, but the current workflow produces station-level silos with no systematic cross-case intelligence.

The competition provides access to the Karnataka Police FIR schema (ER diagram) and expects teams to demonstrate a working, demoable system using synthetic data within the Zoho Catalyst platform.

### 2.2 What Berunda Is Not

This document explicitly records what Berunda is NOT, to prevent scope drift:

- Berunda is **not** a replacement for CCTNS (Crime and Criminal Tracking Network and Systems)
- Berunda is **not** a system that makes arrest decisions or identifies suspects autonomously
- Berunda is **not** a predictive policing system that allocates patrol resources
- Berunda is **not** a citizen-facing portal
- Berunda is **not** a real-time CCTNS data bridge (Phase 2+)
- Berunda is **not** a production deployment on real KSP infrastructure
- Berunda is **not** a court-admissible evidence management system

---

## 3. Current-State Problem

### 3.1 Unstructured FIR Information

FIR narratives (stored in the `BriefFacts` field) contain unstructured text describing persons, vehicles, locations, dates, and circumstances of incidents. This information is entered manually by officers and is not automatically extracted into structured fields. As a result, the rich information in BriefFacts cannot be searched, filtered, or correlated across cases without manual reading.

**Impact:** An officer who wants to know whether a vehicle registration number KA-01-AB-1234 appears in other cases must manually read case files, one by one, across stations.

### 3.2 Manual Data Entry and Transcription Errors

Officers enter FIR data manually into station records. Names are transcribed inconsistently — "Venkatesh Kumar," "Venkatesha Kumar," "V. Kumar," and "Venkat" may refer to the same individual but appear as four separate person records. Without automated extraction and entity resolution, these are permanently siloed.

**Impact:** Repeat offenders are not surfaced automatically. Recidivism patterns are invisible without manual cross-referencing.

### 3.3 Slow Case Retrieval

Retrieving all cases related to a person, vehicle, or location requires manual search across station records, district archives, or CCTNS queries that return raw records without relationship context.

**Impact:** An investigating officer spends hours — sometimes days — cross-referencing related cases that should be visible in seconds.

### 3.4 Fragmented Case Relationships

The source schema stores Accused, Victim, and Complainant records per case (one-to-many per FIR), but provides no native cross-case identity linking. A person who appears as accused in Case 1 and as a witness in Case 4 generates two completely unrelated records in the current system.

**Impact:** Hidden links between cases — shared vehicles, co-accused networks, location patterns — are invisible without a dedicated relationship intelligence layer.

### 3.5 Difficulty Identifying Recurring Entities

Without cross-case entity resolution, it is impossible to know how many times a specific person, vehicle, or address has appeared across the FIR corpus, or which cases are connected through shared entities.

**Impact:** Investigative resources are duplicated. Serial offenders are not identified systematically. Organised crime patterns across districts are invisible.

### 3.6 Evidence and Investigation Traceability

Investigation notes, evidence metadata, and case updates are recorded informally. There is no structured, searchable investigation history attached to each case.

**Impact:** Supervisors cannot quickly assess the current state of an investigation. Audit trails are incomplete.

### 3.7 Supervisor Visibility

Station House Officers (SHOs) and District Superintendents currently rely on manually compiled periodic reports for jurisdiction-level situational awareness. There is no real-time view of crime trends, anomalies, or resource requirements within a jurisdiction.

**Impact:** Resource allocation is reactive. Emerging crime spikes are identified after they have peaked.

### 3.8 Auditability

There is no automated audit trail for who accessed which case, when, and for what purpose. AI-generated recommendations — when they exist — are not traceable to specific officers or decisions.

**Impact:** Accountability is weak. Bias detection and fairness verification are impossible without an audit trail.

### 3.9 Decision-Support Limitations

Investigators do not have access to explainable risk indicators, historical pattern analysis, or natural-language query over case data. Every analytical query requires manual data extraction and processing.

**Impact:** Investigation decisions are made without systematic analytical support. Pattern-based leads are missed.

---

## 4. Root Causes

| Root Cause | Consequence |
|-----------|-------------|
| FIR data stored as unstructured narrative text | Cannot be searched, filtered, or correlated automatically |
| No cross-case entity identity layer | Same person appears as N unrelated records across N cases |
| No structured investigation workflow | Notes, evidence, and updates are informal and unsearchable |
| No jurisdiction-level analytics dashboard | Supervisors rely on periodic manual reports |
| No audit logging at record level | Accountability and bias monitoring are impossible |
| No natural-language interface | Non-technical users cannot query case data directly |
| No bias-auditing tooling | AI-assisted features cannot be verified for fairness |

---

## 5. Affected Users

### Primary Users (must be served by the MVP)

| User | Role | Core Pain |
|------|------|-----------|
| Investigating Officer (IO) | Cross-case investigation and suspect tracking | Cannot find cross-case connections; spends hours on manual cross-referencing |
| Station House Officer (SHO) | Jurisdiction awareness, case assignment, oversight | No real-time view of crime patterns; relies on manual reports |
| SCRB Analyst | State-wide pattern analysis and statutory reporting | Manual data collection from stations; no live state-wide view |
| Compliance / Governance Officer | Fairness and audit oversight | No tools to verify AI recommendations are free from protected-characteristic bias |

### Secondary Users (informed by the product; not primary demo targets)

| User | Role | Future Relevance |
|------|------|-----------------|
| System Administrator | User management, configuration | Must manage roles and access; out of demo spotlight but must exist |
| District Superintendent of Police (SP) | Command-level analytics | SCRB Analyst view covers most of this; SP-specific features are Phase 2 |
| Hackathon Demo Administrator | Demo setup and user provisioning | Required for judging; not a production role |

### Explicitly Excluded Users (not part of the MVP)

| User | Reason for Exclusion |
|------|---------------------|
| Citizens / Complainants | No citizen-facing portal is in scope; FIR complainant is a data subject, not a system user |
| Courts / Judiciary | Read-only access for courts is a Phase 3+ VISION feature |
| Forensic Labs | Evidence metadata linkage is a Phase 2 VISION feature |
| External Agencies (CBI, NIA) | Cross-state correlation is a Phase 5 VISION feature |

---

## 6. User Needs

### Investigating Officer

- Need to find all prior cases involving a specific person, vehicle, or address within seconds
- Need to see relationships between cases — shared entities, co-accused networks
- Need AI assistance in extracting structured entities from FIR narrative text
- Need to verify and correct AI-extracted information before it becomes official
- Need to add investigation notes and evidence references to a case
- Need to ask plain-language questions about case data and receive cited answers

### Station House Officer

- Need real-time view of crime trends and patterns in their jurisdiction
- Need to see anomalous spikes and emerging patterns before they escalate
- Need to assign and monitor investigation progress
- Need to review AI recommendations before they influence investigation decisions

### SCRB Analyst

- Need a state-wide drillable view of crime patterns by district, crime type, and time period
- Need to detect cross-district patterns and entity connections
- Need automated report generation for statutory obligations
- Need confidence that AI analytics are explainable and not based on protected characteristics

### Compliance / Governance Officer

- Need to verify that CasteID and ReligionID fields are excluded from all predictive models
- Need access to the full audit log for all sensitive data reads and AI-generated outputs
- Need to generate aggregate compliance reports (e.g., SC/ST Act crime counts by district) without exposing individual records

---

## 7. Product Vision

> **Berunda is a structured information extraction and investigation-support platform that sits on top of Karnataka's existing FIR data as an intelligence layer — turning isolated case records into a connected, queryable, and explainable knowledge base for investigators, supervisors, and analysts, while keeping every decision in human hands.**

Berunda does not decide guilt. Berunda does not replace police judgment. Berunda does not make arrests or produce final legal determinations. Berunda makes human investigators significantly more effective by surfacing information they already have a right to, in a form they can act on.

---

## 8. Product Mission

> **The Berunda hackathon implementation must demonstrate that a 2-person team can — within 11 days, on Zoho Catalyst, with synthetic data — produce a working system that shows how AI-assisted structured information extraction, cross-case entity resolution, and explainable analytics can transform raw FIR data into an actionable, auditable investigation-support layer.**

The demo must be reliable enough to run live in front of judges without manual data patches. Every feature shown must be a working feature, not a mockup.

---

## 9. Product Goals

### GOAL-001 — AI-Assisted Structured FIR Capture

**Goal:** Enable an officer to create or upload an FIR and receive AI-suggested structured entity extraction (persons, vehicles, locations, legal sections) that the officer can review, correct, and approve.

**User benefited:** Investigating Officer, SHO

**Expected outcome:** FIR registration time reduced; extracted entities are more consistent than manual entry; officer remains in control of what is officially recorded.

**Measurement method:** Demo passes when an uploaded FIR produces a verified entity extraction that is saved and searchable.

**Related problem:** Sections 3.1, 3.2

**MVP relevance:** Core — this is the first step of the primary demo flow.

---

### GOAL-002 — Cross-Case Entity Resolution

**Goal:** Automatically match persons (and vehicles) across FIRs despite name spelling variations, and present resolved entities with confidence scores and merge decisions for officer review.

**User benefited:** Investigating Officer

**Expected outcome:** A planted repeat-offender appearing under 4 different name spellings across 4 FIRs is surfaced as a single PersonEntity with all 4 cases linked.

**Measurement method:** Acceptance test — planted repeat-offender correctly linked across 4 cases.

**Related problem:** Section 3.4, 3.5

**MVP relevance:** Core — the signature technical capability.

---

### GOAL-003 — Relationship Graph and Hidden-Link Discovery

**Goal:** Provide an interactive graph showing relationships between a person, their linked cases, co-accused, victims, and vehicles — with path-finding to surface hidden connections.

**User benefited:** Investigating Officer, SHO

**Expected outcome:** Investigator can see that Case 001 and Case 042 are connected through a shared person, vehicle, or co-accused — a connection invisible without the graph.

**Measurement method:** Demo passes when a hidden link (shared vehicle or shared person) is correctly surfaced between two planted cases.

**Related problem:** Sections 3.3, 3.4

**MVP relevance:** Core — visually compelling demo feature.

---

### GOAL-004 — Geospatial Hotspot Analysis

**Goal:** Provide an interactive geospatial map showing crime density by district and station, with time-of-day and crime-type filters.

**User benefited:** SHO, SCRB Analyst

**Expected outcome:** SHO can identify emerging crime hotspots in their jurisdiction at a glance rather than compiling manual Excel reports.

**Measurement method:** Demo passes when the hotspot map renders with drillable district-to-station data and filters work correctly.

**Related problem:** Section 3.7

**MVP relevance:** Core — visually impactful for judges.

---

### GOAL-005 — Explainable Risk Scoring

**Goal:** Compute a repeat-offender risk score for each resolved PersonEntity, with a feature-importance breakdown that explains the score in terms the officer can understand and verify. Caste and religion must be confirmed absent from the model.

**User benefited:** Investigating Officer, Compliance Officer

**Expected outcome:** Risk score is accompanied by a readable explanation. Officer can see that the score is based on prior case count, recency, and crime diversity — not protected characteristics.

**Measurement method:** Demo passes when the fairness check confirms CasteID/ReligionID are excluded and feature importance is visible.

**Related problem:** Sections 3.8, 3.9

**MVP relevance:** Core — differentiates Berunda from black-box tools; judges care about responsible AI.

---

### GOAL-006 — Anomaly Detection

**Goal:** Detect and flag statistical anomalies in crime frequency (spikes above historical baseline by district and crime type).

**User benefited:** SHO, SCRB Analyst

**Expected outcome:** A planted crime spike (3x normal rate for a week) is detected and surfaced as an anomaly alert on the dashboard.

**Measurement method:** Demo passes when the anomaly alert appears on the dashboard with a z-score indicating deviation from baseline.

**Related problem:** Section 3.7

**MVP relevance:** Core.

---

### GOAL-007 — Natural-Language Investigation Query

**Goal:** Allow investigators and analysts to ask plain-English questions about cases, persons, and vehicles and receive grounded, cited answers.

**User benefited:** Investigating Officer, SCRB Analyst

**Expected outcome:** "What is the connection between FIR-001 and FIR-042?" returns an answer grounded in actual case records with source citations visible.

**Measurement method:** Demo passes when 3 rehearsed questions return grounded, cited answers.

**Related problem:** Section 3.9

**MVP relevance:** Core — "Ask Berunda" is the most accessible demo feature for non-technical judges.

---

### GOAL-008 — Role-Based Access and Audit Logging

**Goal:** Enforce role-based access control (4 roles: INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, ADMIN) with audit logging for every sensitive data read and AI-generated output view.

**User benefited:** All users; Compliance Officer

**Expected outcome:** Each role sees a different view; every sensitive access is logged; the audit log is queryable by the Compliance role.

**Measurement method:** Demo passes when role-switching shows different views and the audit log shows entries for actions performed.

**Related problem:** Section 3.8

**MVP relevance:** Core — required for responsible AI and security compliance.

---

## 10. Non-Goals

The following are explicitly **not** part of the Berunda hackathon MVP. Features listed here must not be implemented without explicit scope change approval.

| Non-Goal | Reason |
|---------|--------|
| Final legal decision-making | Berunda is an advisory tool; all decisions remain with authorised officers |
| Autonomous suspect identification | Human review is mandatory for all entity resolution merge decisions |
| Predictive policing (patrol allocation based on risk scores) | Ethically unacceptable; risk score is for investigative awareness only |
| Production integration with real CCTNS data | Requires legal MOU; Phase 2+ |
| Real sensitive citizen data in the system | Synthetic data only; AGENTS.md Rule 4 |
| Fully automated evidence conclusions | Evidence management is metadata only; no forensic conclusions |
| Replacement of official CCTNS police records | Berunda is an intelligence layer; CCTNS remains the system of record |
| Unverified external surveillance integrations (CCTV, telecom) | No data from unverified surveillance sources |
| Training a large foundation model from scratch | Fine-tuning or RAG over existing LLM; no pre-training |
| Kannada NLP in MVP | Stretch goal — English only in Phase 1; Kannada is Phase 2 |
| Mobile native app | Web-responsive UI only in Phase 1 |
| Real-time CCTNS data streaming | Batch import of synthetic data only |
| Court-facing or prosecutor-facing views | Phase 3+ VISION feature |
| Real biometric data | Prohibited by AGENTS.md safety rules |
| Individual criminality prediction | Risk score is based on case history, not identity markers |

---

## 11. Product Principles

| Principle | Meaning in Practice |
|-----------|-------------------|
| **Human review first** | No AI output becomes official case information without an authorised officer reviewing and approving it |
| **Authorization-first access** | Every data access is gated by a valid JWT and verified role; deny by default |
| **Explainability** | Every AI-generated score, suggestion, or answer includes the reasoning behind it; black-box outputs are not permitted |
| **Auditability** | Every sensitive data access and AI output view generates an immutable audit log entry |
| **Privacy** | CasteID and ReligionID fields are restricted to the Compliance role; demographic data is never used in predictive models |
| **Data minimisation** | Only data fields necessary for each role's function are exposed; no broad data dumps |
| **Source-grounded AI** | RAG answers are grounded in retrieved case documents; no answer is provided without a source citation |
| **Correctness over automation** | A slower but correct human-reviewed result is preferable to a fast but unverified automated result |
| **Graceful failure** | If an AI service is unavailable, the system degrades to showing the underlying structured data; it does not show errors to the end user |
| **Demo reliability** | Features shown to judges must be working features on live data; no hardcoded demo values |

---

## 12. Expected Outcomes

### Hackathon Outcomes (Demonstrable on Day 11)

| Outcome | How Demonstrated |
|---------|-----------------|
| Structured FIR entity extraction works | Upload a synthetic FIR; show extracted persons, vehicles, and locations |
| Cross-case entity resolution works | Search for a planted repeat-offender; show 4 cases linked to one PersonEntity |
| Relationship graph is interactive | Click on a PersonEntity; show force-directed graph with linked cases and co-accused |
| Hotspot map is functional | Show heatmap over Karnataka; drill down to district and station |
| Risk score is explainable | Show score with feature-importance breakdown; confirm caste/religion exclusion |
| Anomaly detection fires | Show the anomaly alert for the planted crime spike week |
| Ask Berunda answers grounded questions | Ask 3 rehearsed questions; verify cited answers |
| Role-based access works | Switch between Investigator, Analyst, and Compliance roles; verify different views |
| Audit log is queryable | Show audit log entries for actions performed during demo |
| Fairness check passes | Show fairness dashboard confirming CasteID/ReligionID exclusion |

### Future Production Outcomes (Roadmap — Not Hackathon Claims)

| Phase | Outcome |
|-------|---------|
| Phase 2 — Pilot | At least one investigator-confirmed hidden link discovered that would not have been found manually |
| Phase 3 — District | Cross-district query resolution time reduced from days to minutes |
| Phase 4 — State | SCRB statutory reports generated directly from platform without manual Excel compilation |
| Phase 5 — National | At least one independently operated state instance deployed |

---

## 13. Outcome Hierarchy

```
Problem: Isolated FIR records hide connections between persons, cases, and locations
  → User need: Investigators need to find cross-case connections quickly and reliably
    → Product capability: Cross-case entity resolution with confidence scoring
      → User outcome: Repeat offender surfaced in seconds instead of hours
        → Success measurement: Planted repeat-offender correctly linked across 4 cases in acceptance test

Problem: FIR narrative text is unstructured and cannot be searched
  → User need: Officers need structured entity data without manual transcription
    → Product capability: AI-assisted NER extraction with human review and correction
      → User outcome: FIR entity data is structured and searchable immediately after registration
        → Success measurement: Demo shows extracted entities visible in FIR detail view

Problem: Supervisors have no real-time jurisdiction awareness
  → User need: SHOs need live crime trend and hotspot data
    → Product capability: Geospatial hotspot map with anomaly detection
      → User outcome: SHO identifies emerging patterns in one dashboard view
        → Success measurement: Hotspot map renders with filters; anomaly alert fires for planted spike

Problem: AI recommendations cannot be verified for fairness
  → User need: Compliance officers need evidence that models are fair
    → Product capability: Fairness verification dashboard + feature-importance display
      → User outcome: Compliance officer can confirm on demand that no model uses caste/religion features
        → Success measurement: Fairness check output confirms exclusion programmatically
```

---

## 14. Product Positioning

### Versus Existing Systems

| System | What it does well | Berunda's difference |
|--------|------------------|---------------------|
| CCTNS | Standardised FIR digitisation | Record-keeping only; Berunda adds intelligence layer |
| NCRB / ICJS | National crime statistics | Retrospective aggregate reporting; Berunda is investigator-facing and real-time |
| Palantir Gotham | Best-in-class entity resolution | Proprietary, expensive, closed-source, not Catalyst-native, not India-specific |
| IBM i2 | Mature link chart analysis | Desktop-centric, license-per-seat, no built-in fairness governance |

**Berunda's fit:** It is the only option that is simultaneously open-core and state-owned, designed for Karnataka's linguistic and legal context, and built with fairness auditing as a first-class feature rather than a bolt-on.

---

## 15. Elevator Pitches

### One-Sentence Description

> Berunda transforms Karnataka's fragmented FIR records into a connected, queryable intelligence layer — built entirely on Zoho Catalyst, with explainable AI and built-in fairness verification.

### Thirty-Second Explanation

> Karnataka Police generates thousands of FIRs, but each one is an isolated record. A suspect appearing in five cases across three districts looks like five unrelated files. Berunda extracts structured entities from FIR narratives using AI, resolves person identities across cases, and surfaces hidden connections — while keeping every decision in an officer's hands and every AI recommendation fully explainable and auditable.

### Two-Minute Explanation

> Karnataka's crime data lives in station-level silos. FIR narratives are unstructured. The same person appears under different name spellings across different cases. There is no tool that connects these records automatically, no way to ask a plain-English question about case data, and no way to verify that AI recommendations are not based on protected characteristics like caste or religion.
>
> Berunda addresses each of these problems. An officer uploads or creates an FIR. AI extracts persons, vehicles, and locations from the narrative text. The officer reviews and corrects the suggestions before they are saved. Once saved, the FIR becomes searchable. The entity resolution engine matches persons across cases — even with name variations — and presents matches with confidence scores for human approval.
>
> Investigators see a relationship graph showing every case connected to a person, vehicle, or location. SCRB analysts see a live geospatial hotspot map with district drill-down and anomaly alerts. The Ask Berunda feature answers plain-English questions over the case corpus with source citations. And the Compliance officer sees a fairness dashboard that confirms, every day, that caste and religion fields are excluded from every predictive model.
>
> All of this runs on Zoho Catalyst, using synthetic Karnataka Police data, with an audit log for every action and a human review gate before any AI suggestion becomes official.

### Judge-Facing Hackathon Pitch

> "Project Berunda is a working, demoable intelligence layer on top of Karnataka's FIR database, built on Zoho Catalyst in 11 days by a 2-person team. We solve the specific problem that the same suspect — Venkatesh — appears as four different names across four different FIRs, and today no one connects them. Berunda does. In five minutes, I'll show you AI-assisted entity extraction, cross-case relationship graphs, a live geospatial hotspot map, an explainable risk score with feature importance breakdown, natural-language case queries, and a fairness dashboard that verifies caste and religion are excluded from every model. Every feature is a working feature. Every AI output has a human review gate. And everything is logged."

---

## 16. Constraints

| Constraint | Source | Impact |
|-----------|--------|--------|
| Must deploy on Zoho Catalyst | Hackathon rules | Architecture must use Catalyst Functions, Data Store, Auth, QuickML, AppSail |
| 11-day build window | Hackathon timeline | Forces strict scope discipline; 12 MVP features maximum |
| 2-person team | Team composition | Parallelism limited; critical-path features must be identified |
| Synthetic data only | AGENTS.md Rule 4; responsible-AI | No real PII; demo uses Faker en_IN generated data |
| No real CCTNS integration | Legal — requires MOU | MVP uses synthetic import; CCTNS is Phase 2 |
| English-only NLP in MVP | Time constraint | Kannada NER is STRETCH / Phase 2 |
| Human review required for all AI outputs | Responsible AI; DEC-006, DEC-007 | No autonomous decisions; every AI suggestion requires officer approval |

---

## 17. Assumptions Requiring Validation

The following assumptions in this document are unconfirmed and must be validated before the affected work begins. See `10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md` for the full register.

| ASM-ID | Assumption | Validation Required By |
|--------|-----------|----------------------|
| ASM-002 | Catalyst QuickML supports LLM serving, RAG, and AutoML feature importance | Day 1 |
| ASM-004 | Synthetic data is acceptable for judging | Day 1 |
| ASM-008 | Submission format is repository + demo video + slide deck | Day 1 |
| ASM-009 | OpenAI / Groq API keys are available for the demo environment | Day 5 |

---

*End of 01-PROBLEM-STATEMENT-AND-VISION.md*
