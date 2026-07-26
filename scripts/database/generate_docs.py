import os

docs_dir = "d:/Hack2Skill/Berunda/docs/database/phase-05"
os.makedirs(docs_dir, exist_ok=True)

docs = {
    "02-PHYSICAL-TABLE-SPECIFICATIONS.md": """# Physical Table Specifications

> **Document ID:** BERUNDA-PH5-TABLE-SPECS-001 | **Version:** 1.0

## Core Tables
- **CaseMaster**: Stores base FIR. Primary Key: ROWID. Public ID: CaseNo.
- **Employee**: Stores Officers. PII Enabled: EmployeeName.
- **Unit**: Stores Police Stations.
- **Inv_OccurrenceTime**: Case occurrence timeline. FK to CaseMaster.
- **PersonEntity**: (Accused/Victim/Complainant) Extracted individuals.
- **VehicleLink**: Extracted vehicles.

## Audit & AI
- **AuditLog**: Immutable. Tracks all views of sensitive PII or AI triggers.
- **AISuggestion**: AI generated insights. FK to CaseMaster.
- **AIReviewDecision**: Human decisions on AISuggestion.

*Note: All tables rely on Catalyst Data Store limitations. Integers may map to BigInt. Foreign keys map to ROWID.*
""",
    "03-ENUMERATIONS-STATE-MACHINES-AND-TRANSITIONS.md": """# Enumerations, State Machines, and Transitions

> **Document ID:** BERUNDA-PH5-ENUMS-001 | **Version:** 1.0

## CaseStatusMaster
- **Values**: Registered, Under Investigation, Chargesheeted, Closed
- **Transitions**: Registered -> Under Investigation -> Chargesheeted/Closed

## AI Review Outcome
- **Values**: Pending, Approved, Rejected, Edited

## Audit Result
- **Values**: Success, Failure, Denied

*No free-text lifecycle states are permitted.*
""",
    "04-INDEX-AND-QUERY-SUPPORT-STRATEGY.md": """# Index and Query Support Strategy

> **Document ID:** BERUNDA-PH5-INDEX-001 | **Version:** 1.0

## Index Strategy for Catalyst
Catalyst provides basic indexing (Search Index).
- **CaseMaster**: CaseNo (Unique, Search Index)
- **Employee**: EmployeeID (Unique, Search Index)
- **Unit**: UnitID (Unique, Search Index)
- **AuditLog**: CorrelationID (Search Index)

*Note: Catalyst automatically indexes ROWID and Foreign Key columns.*
""",
    "05-STRATUS-STORAGE-DESIGN-AND-IMPLEMENTATION.md": """# Stratus Storage Design and Implementation

> **Document ID:** BERUNDA-PH5-STRATUS-001 | **Version:** 1.0

## Storage Categories
1. **Original FIR Documents**: Raw uploaded PDFs/Images. Private, strict access control.
2. **Evidence Files**: Audio/Video/Images associated with a case.
3. **Generated Reports**: Output PDF/CSV analytics.
4. **Temporary Processing**: Fleeting storage for AI chunking.
5. **Demo Data**: Synthetic files for Datathon demo.

## Access Policy
- Stratus containers must be marked as **Private**.
- Temporary files must have an aggressive cleanup job.
- User filenames must not be used directly as object keys to prevent path traversal.
""",
    "06-MIGRATION-PROVISIONING-AND-ROLLBACK-STRATEGY.md": """# Migration, Provisioning, and Rollback Strategy

> **Document ID:** BERUNDA-PH5-MIGRATION-001 | **Version:** 1.0

## Provisioning Mechanism
We utilize Python SDK/API scripts against Catalyst (`catalyst_client.py`) that parse the master Markdown schema (`CATALYST_DATASTORE_SCHEMA_MAPPING.md`) and enforce state idempotently.

## Rollback
- Destructive actions (dropping columns/tables) require explicit confirmation.
- Rollback is achieved by wiping the environment and re-running the seed script (`demo_reset.py`).
""",
    "07-SCHEMA-AND-SEED-VALIDATION-REPORT.md": """# Schema and Seed Validation Report

> **Document ID:** BERUNDA-PH5-SEED-VAL-001 | **Version:** 1.0

## Schema Check
- Diffed Catalyst environment vs `CATALYST_DATASTORE_SCHEMA_MAPPING.md`.
- Mismatches handled programmatically.

## Seed Check
- Executed `import_synthetic_data.py`.
- Verified CaseMaster counts and relationships.
- All seeded records respect synthetic boundaries and environment isolation.
""",
    "08-DATABASE-AND-STORAGE-SECURITY-REPORT.md": """# Database and Storage Security Report

> **Document ID:** BERUNDA-PH5-DB-SEC-001 | **Version:** 1.0

## Security Controls
- **PII / Audit Consent**: Enabled on all Catalyst Data Store columns storing names/ages.
- **Stratus Isolation**: All buckets configured to `Private`.
- **Secret Scanning**: Verified no hardcoded tokens in `import_synthetic_data.py` (uses `.env`).
- **Data Boundaries**: Station-level RBAC is implemented in the AppSail logic, querying against the Unit table.
""",
    "09-PHASE-5-DEFECT-AND-REMEDIATION-LOG.md": """# Phase 5 Defect and Remediation Log

> **Document ID:** BERUNDA-PH5-DEFECTS-001 | **Version:** 1.0

| Defect ID | Area | Description | Remediation | Status |
|-----------|------|-------------|-------------|--------|
| P5DB-MAJ-001 | Schema | Catalyst limits FKs to mapping to ROWID, ignoring provided int IDs. | Re-mapped scripts to capture ROWID upon insertion and use that for child dependencies. | FIXED |
| P5DB-MIN-001 | PII | PII/Audit consent flags missing on legacy tables | Wrote scripts to patch Data Store columns via API. | FIXED |
""",
    "10-PHASE-5-DATABASE-TRACEABILITY-MATRIX.md": """# Phase 5 Database Traceability Matrix

> **Document ID:** BERUNDA-PH5-TRACE-001 | **Version:** 1.0

| Requirement ID | Logical Entity | Physical Table | Implementation Status |
|----------------|----------------|----------------|-----------------------|
| REQ-FIR-01     | FIR            | CaseMaster     | Implemented           |
| REQ-AUTH-01    | Officer        | Employee       | Implemented           |
| REQ-AI-01      | AI Suggestion  | AISuggestion   | Implemented           |
| REQ-SEC-01     | Audit Log      | AuditLog       | Implemented           |
""",
    "11-PHASE-5-COMPLETION-REPORT.md": """# Phase 5 Completion Report

> **Document ID:** BERUNDA-PH5-COMPLETION-001 | **Version:** 1.0
> **Final Verdict: PASS**

## Executive Summary
Phase 5 successfully transitioned the theoretical ERDs into a living Catalyst Data Store architecture. 

## Readiness for Phase 6
- **Database Backend readiness**: TRUE.
- **Data layer interfaces**: Defined.
- **Stratus structure**: Complete.

Backend engineers can now proceed to Phase 6 (API implementation) using the defined Catalyst schemas.
"""
}

for filename, content in docs.items():
    filepath = os.path.join(docs_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)

print(f"Created {len(docs)} markdown files in {docs_dir}")
