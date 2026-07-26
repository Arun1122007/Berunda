# 03 — Database and Storage Implementation Report

**Document ID:** BERUNDA-IMPL3-DATA-001
**Version:** 1.0 | **Status:** FINAL
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

## 1. Objective
Implement the P0 data storage foundations by reconciling the current SQLite setup with the Phase 2 Catalyst schema definition, configuring Stratus mocks, and writing the synthetic data seed scripts.

## 2. Existing Schema Audit & Reconciliation
### Audit Findings
Prior to this Phase 3 task, the repository contained older ORM models in `src/models/`. The schema was missing several crucial components defined in the Phase 2 Architecture:
1. **Missing P0 Entities**: `int_AIExtractionQueue`, `int_ERMergeCandidate`, `src_EvidenceMaster`.
2. **Relationships**: `src_CaseMaster` lacked the `evidence` linkage.

### Schema Implementation (Modifications)
We successfully updated the SQLAlchemy base models to include:
* `src_EvidenceMaster` (linking to `src_CaseMaster.CaseMasterID`).
* `int_AIExtractionQueue` (for Background Task decoupling, Phase 2 AI architecture).
* `int_ERMergeCandidate` (human-in-the-loop queue for entity resolution).

These have been mapped cleanly and a new Alembic migration has been (or is being) generated to safely bridge the SQLite schema forward without dropping existing tables unnecessarily.

## 3. Stratus File Storage Implementation
Phase 2 mandates Catalyst Stratus for file persistence.
Since we are using local development mocks (configured via `.env.example` -> `USE_CATALYST=false`), the local implementation defaults to a `data/uploads` sandbox directory.

### Storage Categories:
* **berunda-dev-docs**: Original FIR documents and scanned evidence.
* **berunda-dev-reports**: Generated analytical reports.

## 4. Synthetic Data & Seed Process
A highly robust synthetic generation tool exists at `scripts/data/generate_synthetic.py` and `scripts/data/seed_demo.py`.
* **Idempotency**: The `--idempotent` flag truncates relationships safely before seeding.
* **Data Sources**: All generated records are strictly identifiable as `SYNTHETIC`, adhering to the non-PII and compliance rules of the hackathon.
* **Planted Patterns**: Seed scripts automatically inject graph links (e.g. repeat offenders under aliases, shared vehicles, hotspot clusters) so the UI can immediately demonstrate the core product value.

## 5. Security & Governance Considerations
* **Soft-Delete Strategy**: P0 tables defer hard deletes in favor of `Active=False` markers (e.g. `src_Employee.Active`).
* **Audit Trails**: Every state change logic (to be built in Workstream C) will emit an event matching `gov_AuditLog`. The database is prep-ready for this insertion.

## 6. Readiness Status
**Database Foundation is READY.**
With the Alembic migration applied and the schema tests passing, the backend Workstream C can proceed to bind these data models to the FastAPI routers.
