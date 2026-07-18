# Execute Resource Acquisition Blueprint — Implementation Plan

Implement the full directory structure, acquisition scripts, manifest files, reports, and configuration specified in [Project_Berunda_06_Resource_Acquisition_Blueprint.md](file:///d:/Hack2Skill/Berunda/document/h2s/Project_Berunda_06_Resource_Acquisition_Blueprint.md) and [Project_Berunda_07_Autonomous_Agent_Prompt.md](file:///d:/Hack2Skill/Berunda/document/h2s/Project_Berunda_07_Autonomous_Agent_Prompt.md).

## Environment Summary (Verified)

| Tool | Version | Status |
|------|---------|--------|
| Python | 3.13.5 | ✅ |
| Git | 2.52.0 | ✅ |
| Node.js | 24.15.0 | ✅ |
| Java | 19.0.1 | ✅ |
| PowerShell | 5.1 (Windows PS, not pwsh) | ✅ |
| pip | 26.1.2 | ✅ |
| pandas | 2.3.1 | ✅ installed |
| requests | 2.32.4 | ✅ installed |
| networkx | 3.6.1 | ✅ installed |
| Faker | — | ❌ not installed |
| shapely / geopandas | — | ❌ not installed |
| Disk (D:) | 107.72 GB free | ✅ ample |

---

## User Review Required

> [!IMPORTANT]
> **Git checkpoint**: Before any file creation, I'll create a git commit/tag (`pre-acquisition-scaffold`) so everything is reversible. The repo currently has uncommitted modifications to ~80 docs files.

> [!IMPORTANT]
> **Python package installation**: The scripts require `Faker`, `shapely`, and `hashlib` (stdlib). I'll need to `pip install Faker` and possibly `shapely` during execution. These are declared P1 resources (R032). Do you approve these pip installs?

> [!WARNING]
> **No real data will be downloaded** during this phase. This plan creates the *scaffolding* — directory structure, runnable scripts, empty manifests, and the preflight report. Actual resource acquisition (Phase 3 of File 07) will be a dry-run first, presented for your approval before executing.

---

## Open Questions

> [!IMPORTANT]
> **PowerShell version**: Your system has Windows PowerShell 5.1 (not PowerShell Core/pwsh). The File 07 scripts specify `.ps1` files. Should I write them for Windows PowerShell 5.1 compatibility, or would you prefer Python-only scripts?

> [!NOTE]
> **Uncommitted changes**: There are ~80 modified docs files not yet committed. Should I commit them as part of the pre-acquisition checkpoint, or leave them staged?

---

## Proposed Changes

### Phase 0 — Directory Structure (Blueprint Section G)

Create the full directory tree as specified. All directories will include a `.gitkeep` to ensure they're tracked.

#### [NEW] Full directory tree

```text
d:\Hack2Skill\Berunda\
  ├── data/
  │   ├── organizer/           # R001 and Hack2Skill-provided files
  │   ├── raw/                 # R006-R022 as originally downloaded
  │   ├── external/            # API responses (R011, R012, R017)
  │   ├── interim/
  │   ├── processed/
  │   ├── synthetic/           # Faker output, SYNTHETIC_ prefixed
  │   ├── samples/
  │   └── restricted-placeholders/  # Mock adapters for FUTURE-RESTRICTED
  ├── boundaries/              # OSM/Bhuvan geospatial layers
  ├── repositories/            # Cloned repos (owner__repo format)
  ├── models/
  ├── manifests/
  ├── scripts/
  │   ├── acquisition/
  │   ├── validation/
  │   └── transformation/
  ├── resources/
  │   ├── source-pages/
  │   ├── standards/
  │   ├── papers/
  │   └── licenses/
  ├── reports/
  ├── logs/
  └── quarantine/              # Download landing zone
```

---

### Phase 1 — Configuration & Safety Files

#### [NEW] [.gitignore](file:///d:/Hack2Skill/Berunda/.gitignore)

Comprehensive `.gitignore` covering:
- `data/organizer/` and `data/synthetic/` (large files)
- `quarantine/`
- `repositories/` (cloned repos)
- `models/`
- `.env`, secrets, credentials
- Python caches, `__pycache__`, `.pyc`
- Node `node_modules/`
- OS files (`.DS_Store`, `Thumbs.db`)
- Log files over typical sizes
- Large data files (`*.parquet`, `*.db`, `*.sqlite`)

#### [NEW] [AGENTS.md](file:///d:/Hack2Skill/Berunda/AGENTS.md)

Agent operating instructions per File 07 — workspace root, safety rules summary, domain allowlist, command allowlist, interaction policy.

---

### Phase 2 — Manifest Files (Blueprint Section H)

#### [NEW] `manifests/resource_manifest.csv`
Pre-populated with all 35 resources (R001-R035) from Section C. Columns: `resource_id`, `priority`, `category`, `resource_name`, `source_url`, `publisher`, `license`, `legal_class`, `pii_risk`, `acquisition_method`, `catalyst_mapping`, `limitation`, `acceptance_criterion`, `status`, `date_acquired`, `checksum`, `local_path`.

#### [NEW] `manifests/resource_manifest.json`
JSON version of the same, machine-parseable.

#### [NEW] `manifests/download_manifest.csv`
Empty template: `resource_id`, `url`, `http_status`, `bytes_received`, `timestamp`, `local_path`, `checksum_sha256`.

#### [NEW] `manifests/repository_inventory.csv`
Empty template: `resource_id`, `repo_url`, `clone_path`, `pinned_commit`, `license_spdx`, `classification`, `dependency_file`, `secrets_scan_result`.

#### [NEW] `manifests/license_inventory.csv`
Pre-populated with known licenses for R001-R035.

#### [NEW] `manifests/provenance.jsonl`
Empty JSONL file with a comment/header describing the schema.

#### [NEW] `manifests/failure_log.csv`
Empty template: `resource_id`, `attempted_date`, `failure_reason`, `next_action`.

#### [NEW] `manifests/missing_resource_register.csv`
Empty template: `resource_id`, `reason_missing`, `impact`, `mitigation`.

#### [NEW] `manifests/approval_register.csv`
Empty template: `resource_id`, `approval_type`, `approved_by`, `approval_date`.

---

### Phase 3 — Acquisition Scripts (File 07 Required Scripts)

All scripts will support: `--dry-run` (default True), `--resource-id`, `--priority`, `--max-file-size` (200MB), `--max-total-size` (1GB), `--resume`, `--force`, structured logging, retry with exponential backoff, path validation, idempotency, and meaningful exit codes.

#### [NEW] `scripts/acquisition/preflight.ps1`
Phase 0 preflight: checks environment, disk space, existing files, produces `reports/PREFLIGHT_REPORT.md`.

#### [NEW] `scripts/acquisition/download_resources.ps1`
PowerShell acquisition script using `Invoke-WebRequest` with resumable downloads, rate limiting, checksum generation.

#### [NEW] `scripts/acquisition/download_resources.py`
Python equivalent using `requests` with streaming downloads, retry logic, SHA256 checksums, quarantine-first writes.

#### [NEW] `scripts/acquisition/clone_repositories.ps1`
PowerShell script for `git clone` with shallow clones, commit pinning, secrets scanning.

#### [NEW] `scripts/acquisition/clone_repositories.py`
Python equivalent using `subprocess` for git operations.

---

### Phase 4 — Validation Scripts

#### [NEW] `scripts/validation/validate_resources.py`
Implements Section I quality gates: file integrity, schema validation, temporal validity, duplicate detection, missing-value profiling, licensing check, PII scan, synthetic-data labeling check.

#### [NEW] `scripts/validation/validate_geospatial.py`
Geospatial-specific gates: geometry validity, Karnataka bounding box check, CRS = WGS84 verification, admin-code join check.

#### [NEW] `scripts/validation/scan_sensitive_data.py`
PII/secrets scanner: regex-based detection of phone numbers, Aadhaar patterns, email addresses, real names in aggregate/synthetic data.

---

### Phase 5 — Transformation Planning

#### [NEW] `scripts/transformation/README.md`
Documents the transformation pipeline plan (Phase 6 of File 07): canonical ID assignment, date normalization to IST, Karnataka admin-code mapping, coordinate normalization, IPC→BNS mapping (flagged for human review), synthetic-data generation scripts, train/val/test splits.

---

### Phase 6 — Reports

#### [NEW] `reports/PREFLIGHT_REPORT.md`
Environment inventory, existing file inventory, domain allowlist, acquisition plan dry-run.

#### [NEW] `reports/RESOURCE_INVENTORY.md`
Status of all R001-R035: present-and-verified / present-but-stale / missing / inaccessible / restricted / not-required.

#### [NEW] `reports/DOWNLOAD_REPORT.md`
Template for tracking download outcomes per resource.

#### [NEW] `reports/VALIDATION_REPORT.md`
Template for quality gate results per acquired resource.

#### [NEW] `reports/MISSING_RESOURCES.md`
Gap analysis against blueprint requirements.

#### [NEW] `reports/LICENSE_AND_ATTRIBUTION_REPORT.md`
License compliance summary for all acquired resources.

#### [NEW] `reports/SECURITY_AND_PRIVACY_REPORT.md`
PII scan results, secrets scan results, malware scan results.

#### [NEW] `reports/ENTERPRISE_READINESS_GAP.md`
Gap analysis: verified inventory vs. challenge requirements, feature-to-data matrix, Catalyst deployment needs, demo storyline, governance requirements.

---

### Phase 7 — Logging

#### [NEW] `logs/acquisition.log`
Initial empty append-only log file for acquisition actions.

---

## Verification Plan

### Automated Tests
- `python scripts/acquisition/download_resources.py --dry-run --priority P0` — verify dry-run produces a plan without downloading
- `python scripts/validation/validate_resources.py --help` — verify all CLI flags are documented
- `python scripts/validation/scan_sensitive_data.py --help` — verify scanner runs
- Verify all manifest CSVs parse correctly with `pandas`
- Verify directory structure matches Section G exactly

### Manual Verification
- Review `AGENTS.md` for correctness of safety rules
- Review `.gitignore` for completeness
- Review `reports/PREFLIGHT_REPORT.md` for accuracy of environment inventory
- Confirm `manifests/resource_manifest.csv` matches all 35 rows from Section C

---

## Execution Order

1. Git checkpoint (commit + tag)
2. Directory structure creation
3. `.gitignore` + `AGENTS.md`
4. Manifest files (CSVs, JSON, JSONL)
5. Acquisition scripts (PS1 + Python)
6. Validation scripts (Python)
7. Transformation README
8. Reports (preflight + templates)
9. Logs initialization
10. Verification pass
11. Summary commit

**Estimated effort**: ~45 minutes of execution time. ~65 files created.
