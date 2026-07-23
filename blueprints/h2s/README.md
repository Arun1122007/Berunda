# Source Blueprint Documents

> **Last Updated:** 2026-07-18
> **Classification:** Internal

---

## Purpose

This directory contains the original 12 source blueprint documents authored during the Hack2Skill Datathon 2026 planning phase. These are the authoritative originals from which the restructured documentation in `docs/` was derived. Do not modify these files directly; any changes should be made to the corresponding `docs/` documents and then reflected back to these blueprints if needed.

---

## File Index

| # | File | Purpose | Corresponding Docs |
|---|------|---------|-------------------|
| 01 | `Project_Berunda_01_Enterprise_Blueprint.md` | Enterprise-level system blueprint, architecture vision, and strategic context | `docs/04_ARCHITECTURE/`, `docs/02_STRATEGY_AND_PRODUCT/` |
| 02 | `Project_Berunda_02_Hackathon_Pitch.md` | Hackathon pitch deck narrative, problem statement, and proposed solution | `docs/02_STRATEGY_AND_PRODUCT/`, `docs/11_DELIVERY/HACKATHON_DEMO_AND_PITCH_PLAN.md` |
| 03 | `Project_Berunda_03_Implementation_Plan.md` | Phased implementation plan with milestones and timeline | `docs/11_DELIVERY/IMPLEMENTATION_PLAN.md`, `docs/10_DEVSECOPS_AND_OPERATIONS/` |
| 04 | `Project_Berunda_04_Complete_Roadmap.md` | End-to-end product roadmap from MVP to target state | `docs/11_DELIVERY/ENTERPRISE_ROADMAP.md`, `docs/02_STRATEGY_AND_PRODUCT/MVP_SCOPE_AND_RELEASE_PLAN.md` |
| 05 | `Project_Berunda_05_Database_ER_Reference.md` | Database entity-relationship reference and schema design | `docs/05_DATA/CANONICAL_DATA_MODEL.md`, `docs/05_DATA/ENTITY_RESOLUTION_SPECIFICATION.md` |
| 06 | `Project_Berunda_06_Resource_Acquisition_Blueprint.md` | Resource acquisition plan, domain allowlist, and download procedures | `docs/13_RESOURCES/01_ENTERPRISE_RESOURCE_ACQUISITION_BLUEPRINT.md` |
| 07 | `Project_Berunda_07_Autonomous_Agent_Prompt.md` | Autonomous agent operating instructions and safety rules | `docs/13_RESOURCES/02_AUTONOMOUS_RESOURCE_ACQUISITION_AGENT_PROMPT.md` |
| 08 | `Project_Berunda_08_NotebookLM_Research_Prompt.md` | NotebookLM research and gap analysis prompt | `docs/13_RESOURCES/03_NOTEBOOKLM_RESEARCH_AND_GAP_ANALYSIS_PROMPT.md` |
| 09 | `project_berunda_blueprint.md` | Comprehensive system blueprint (early draft) | `docs/04_ARCHITECTURE/`, `docs/05_DATA/` |
| 10 | `project_berunda_blueprint_new.md` | Revised comprehensive system blueprint | `docs/04_ARCHITECTURE/`, `docs/05_DATA/` |
| 11 | `CaseGraph_Datathon2026_Blueprint.md` | CaseGraph-specific blueprint for the datathon submission | `docs/02_STRATEGY_AND_PRODUCT/`, `docs/03_REQUIREMENTS/` |
| 12 | `Police_FIR_ER_Diagram.pdf` | Police FIR entity-relationship diagram (original PDF) | `docs/reference/pdf_extracted.md`, `docs/05_DATA/SOURCE_ERD_RECONCILIATION.md` |

---

## Relationship to `docs/`

The `docs/` directory contains the restructured, expanded, and cross-referenced documentation derived from these blueprints. Each blueprint may map to multiple `docs/` subdirectories. The mapping above is a high-level guide; detailed traceability is maintained in:

- `docs/99_REPORTS/TRACEABILITY_CHAIN.md`
- `docs/99_REPORTS/DOCUMENTATION_COVERAGE_MATRIX.md`

---

## Maintenance

- These files are **read-only source documents**. Never edit them directly for the purpose of updating project documentation.
- If a blueprint contains an error, fix it in the corresponding `docs/` file first, then create a note in the discrepancy log (`docs/01_DISCOVERY/CONTRADICTION_ASSUMPTION_AND_GAP_REGISTER.md`).
- When a new version of a source document is produced, archive the old version to `archive/` and place the new version here with an updated timestamp.
