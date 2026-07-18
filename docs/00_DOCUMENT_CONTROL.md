# Document Control

[//]: # (Document ID: BERUNDA-DOC-CTRL-001 | Version: 1.0 | Status: APPROVED | Classification: PUBLIC | Owner: Berunda Team | Audience: Team | Source: Project Berunda master prompt | Last Verified: 2026-07-17 | Review: Monthly)

---

## Document Master Register

| Field | Value |
|-------|-------|
| Project | Project Berunda — AI-Native Crime Intelligence Platform |
| Team | Phoenix Coder (2 members) |
| Datathon | Karnataka State Police Datathon 2026 (Hack2Skill) |
| Mandatory Platform | Catalyst by Zoho |
| Documentation Baseline Version | 1.0 |
| Last Verified | 2026-07-16 |
| Review Cadence | Weekly during hackathon; monthly thereafter |
| Owner | Phoenix Coder Team |

## Document Identification Convention

All documents in this baseline use the following stable ID prefixes:

| Prefix | Entity |
|--------|--------|
| OBJ-### | Business Objective |
| STK-### | Stakeholder / Persona |
| UC-### | Use Case |
| FR-### | Functional Requirement |
| NFR-### | Non-Functional Requirement |
| DR-### | Data Requirement |
| AIR-### | AI Requirement |
| SEC-### | Security Control |
| PRIV-### | Privacy Control |
| GOV-### | Governance Control |
| API-### | API Contract |
| ADR-### | Architecture Decision Record |
| RSK-### | Risk |
| ASM-### | Assumption |
| GAP-### | Issue / Gap |
| TST-### | Test Case |
| EVD-### | Demo Evidence |
| RSRC-### | Resource/Acquisition Item |

## Requirement Field Template

Every requirement record contains:

- **ID** — Stable identifier per the convention above
- **Title** — Short, descriptive name
- **Description** — What the requirement means
- **Rationale** — Why it exists
- **Stakeholder** — Primary stakeholder reference (STK-###)
- **Priority** — MUST / SHOULD / COULD / WONT-NOW
- **Delivery Scope** — MVP / STRETCH / VISION
- **Source Reference** — Traceable to source document and section
- **Dependencies** — Other requirements it depends on
- **Security/Privacy Implications** — Relevant controls
- **Acceptance Criteria** — Given/When/Then form
- **Verification Method** — How to verify
- **Demo Evidence** — How it's shown
- **Status** — DRAFT / REVIEW / APPROVED / IMPLEMENTED / TESTED

## Information Classification Levels

| Level | Description | Examples |
|-------|-------------|---------|
| PUBLIC | Safe for public repository and judging panel | README, Glossary, Market analysis, Open source docs |
| INTERNAL | Team-internal design detail; safe to share with organizers | PRD, SRS, Architecture, Data model, API specs |
| CONFIDENTIAL | Schema details from the organizer's ERD; require careful handling | Source ERD reconciliation, specific field mappings |
| RESTRICTED | Security controls, access specifics, incident playbooks | Threat model, PII handling details, breach playbook |

## Source File Authority Matrix

| Document | Authority | Notes |
|----------|-----------|-------|
| Police_FIR_ER_Diagram.pdf | **PRIMARY** | Organizer-provided schema |
| Project_Berunda_01_Enterprise_Blueprint.md | **CANONICAL NARRATIVE** | v2, reconciled with ERD |
| project_berunda_blueprint_new.md | Near-duplicate reference | Slight formatting differences |
| project_berunda_blueprint.md | Historical v1 (reference) | Pre-ERD generic schema |
| CaseGraph_Datathon2026_Blueprint.md | Precursor concept | Earlier project naming |
| Project_Berunda_02_Hackathon_Pitch.md | Supporting | Judge-facing pitch |
| Project_Berunda_03_Implementation_Plan.md | Supporting | 11-day build tasks |
| Project_Berunda_04_Complete_Roadmap.md | Supporting | Phase timeline, risks |
| Project_Berunda_05_Database_ER_Reference.md | Supporting | Schema extract |
| Project_Berunda_06_Resource_Acquisition_Blueprint.md | Supporting | Data acquisition plan |
| Project_Berunda_07_Autonomous_Agent_Prompt.md | Supporting | Auto-acquisition agent prompt |
| Project_Berunda_08_NotebookLM_Research_Prompt.md | Supporting | NotebookLM research prompt |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-16 | Phoenix Coder | Initial enterprise documentation baseline |
