# Database and Storage Security Report

> **Document ID:** BERUNDA-PH5-DB-SEC-001 | **Version:** 1.0

## Security Controls
- **PII / Audit Consent**: Enabled on all Catalyst Data Store columns storing names/ages.
- **Stratus Isolation**: All buckets configured to `Private`.
- **Secret Scanning**: Verified no hardcoded tokens in `import_synthetic_data.py` (uses `.env`).
- **Data Boundaries**: Station-level RBAC is implemented in the AppSail logic, querying against the Unit table.
