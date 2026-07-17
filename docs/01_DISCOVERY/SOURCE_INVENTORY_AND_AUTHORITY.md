# Source Inventory and Authority Matrix

[//]: # (Document ID: BERUNDA-SRC-INV-001 | Status: DRAFT | Classification: INTERNAL)

---

## Purpose

Complete inventory of every source file in the project workspace, classified by authority, freshness, and role.

## Source Authority Precedence

1. **Organizer-provided data** — Police_FIR_ER_Diagram.pdf (confidential schema)
2. **Current official Zoho Catalyst documentation** — for platform capabilities and limits
3. **Official Indian legal/government sources** — for legal/compliance claims
4. **Canonical narrative** — Project_Berunda_01_Enterprise_Blueprint.md
5. **Supporting companion docs** — _02 through _08
6. **Near-duplicate** — project_berunda_blueprint_new.md (reference only)
7. **Historical draft** — project_berunda_blueprint.md (older v1)
8. **Precursor concept** — CaseGraph_Datathon2026_Blueprint.md

## Complete File Inventory

| # | Filename | Type | Size (lines) | Classification | Authority | Freshness |
|---|----------|------|-------------|---------------|-----------|-----------|
| 1 | `Project_Berunda_01_Enterprise_Blueprint.md` | Markdown | 866 | Canonical narrative | HIGH — v2, ERD-reconciled | Current (2026-07) |
| 2 | `project_berunda_blueprint_new.md` | Markdown | 864 | Near-duplicate | LOW — near-identical to canonical | Current |
| 3 | `project_berunda_blueprint.md` | Markdown | 759 | Historical v1 | LOW — pre-ERD generic schema | Outdated |
| 4 | `CaseGraph_Datathon2026_Blueprint.md` | Markdown | 347 | Precursor concept | MEDIUM — useful competitive framing | Current |
| 5 | `Project_Berunda_02_Hackathon_Pitch.md` | Markdown | 66 | Judge-facing pitch | MEDIUM — strategic framing | Current |
| 6 | `Project_Berunda_03_Implementation_Plan.md` | Markdown | 117 | Build plan | MEDIUM — day-level tasks | Current |
| 7 | `Project_Berunda_04_Complete_Roadmap.md` | Markdown | 137 | Roadmap | MEDIUM — phase-level plan | Current |
| 8 | `Project_Berunda_05_Database_ER_Reference.md` | Markdown | 221 | Schema extract | MEDIUM — duplicate of Blueprint §6 | Current |
| 9 | `Project_Berunda_06_Resource_Acquisition_Blueprint.md` | Markdown | 293 | Data acquisition | MEDIUM — resource strategy | Current |
| 10 | `Project_Berunda_07_Autonomous_Agent_Prompt.md` | Markdown | 251 | Agent prompt | LOW — operational guide | Current |
| 11 | `Project_Berunda_08_NotebookLM_Research_Prompt.md` | Markdown | 138 | Research prompt | LOW — research workflow | Current |
| 12 | `Police_FIR_ER_Diagram.pdf` | PDF | 564 lines (extracted) | **PRIMARY source** | HIGHEST — organizer-provided | Current |

## Duplicate Detection

| Group | Files | Decision |
|-------|-------|----------|
| Primary + near-duplicate | `01_Enterprise_Blueprint.md` + `project_berunda_blueprint_new.md` | Use `01` as canonical; mark `_new` as reference-only |
| Historical | `project_berunda_blueprint.md` | Older v1; do not use for current claims |
| Precursor | `CaseGraph_Datathon2026_Blueprint.md` | Captures competitive analysis and naming research |
| Supporting | `_02` through `_08` | Each has distinct content; all retained |

## Document-Set Claim

The documents claim to be a "companion set of 5" (01-05). The actual package contains:
- 8 numbered companion documents (01-08)
- 1 ERD PDF
- 2 additional blueprint files (new + old)
- 1 CaseGraph precursor

**Resolution:** The "5-document set" claim is outdated. The full set of 12 files is documented above.

## Unresolved Source Questions

| Question | Impact | Action |
|----------|--------|--------|
| Q1: Has the ERD PDF been updated since the source documents were written? | Schema may have changed | Re-check portal before building |
| Q2: Are there additional organizer-provided files not in this package? | Missing requirements | Check Hack2Skill dashboard |
| Q3: What is the exact submission format? | Day 11 deliverable undefined | Check Submissions tab |
| Q4: Is there a published judging rubric? | Cannot weight effort | Check dashboard Resources tab |
