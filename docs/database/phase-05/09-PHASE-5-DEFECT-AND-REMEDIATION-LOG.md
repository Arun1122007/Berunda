# Phase 5 Defect and Remediation Log

> **Document ID:** BERUNDA-PH5-DEFECTS-001 | **Version:** 1.0

| Defect ID | Area | Description | Remediation | Status |
|-----------|------|-------------|-------------|--------|
| P5DB-MAJ-001 | Schema | Catalyst limits FKs to mapping to ROWID, ignoring provided int IDs. | Re-mapped scripts to capture ROWID upon insertion and use that for child dependencies. | FIXED |
| P5DB-MIN-001 | PII | PII/Audit consent flags missing on legacy tables | Wrote scripts to patch Data Store columns via API. | FIXED |
