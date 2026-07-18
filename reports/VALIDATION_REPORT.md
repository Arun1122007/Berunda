# Validation Report

> **Document ID:** BERUNDA-REP-VALIDATION-001 | **Version:** 1.0 | **Status:** PENDING
> **Classification:** INTERNAL | **Owner:** Berunda Team | **Source:** Validation agent
> **Generated:** 2026-07-18T04:30:00Z | **Last Verified:** 2026-07-18

---

## 1. Quality Gates Summary

Per Blueprint §I — a resource does not leave `quarantine/` until it passes every applicable gate:

| # | Gate | Applies To | Status | Resources Tested | Pass | Fail | Skip |
|---|------|-----------|--------|-----------------|------|------|------|
| G01 | Authenticity — source matches verified URL | All | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G02 | File integrity — checksum matches, archive extracts | All downloads | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G03 | Schema validity — required columns and types | Tabular data | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G04 | Geometry validity — valid geom, Karnataka bbox, WGS84 | Spatial data | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G05 | Temporal validity — dates parse, no impossible futures | Temporal data | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G06 | Duplicate detection — no exact-duplicate rows | Tabular data | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G07 | Missing-value profile — recorded, not silently dropped | Tabular data | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G08 | Administrative-code matching — joins boundary ref | Location data | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G09 | Licensing — license on file in `license_inventory.csv` | All | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G10 | Attribution — recorded if license requires it | All | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G11 | Secrets/malware scan — clean before execution | Repositories | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G12 | PII scan — no real PII in aggregate/synthetic data | Datasets | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G13 | Synthetic-data labeling — every file/record marked | Synthetic data | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G14 | Reproducibility — re-runnable acquisition script | All | ⏳ NOT RUN | 0 | 0 | 0 | 0 |
| G15 | Provenance — source, date, checksum in `provenance.jsonl` | All | ⏳ NOT RUN | 0 | 0 | 0 | 0 |

### Gate Status Definitions

| Status | Meaning |
|--------|---------|
| ✅ PASS | All resources of this type passed |
| ❌ FAIL | One or more resources failed (see per-resource table) |
| ⏳ NOT RUN | Validation not yet executed |
| ⏭️ SKIP | Gate not applicable to any currently downloaded resource |

---

## 2. Per-Resource Validation Status

| RSRC ID | Resource | G01 | G02 | G03 | G04 | G05 | G06 | G07 | G08 | G09 | G10 | G11 | G12 | G13 | G14 | G15 | Overall |
|---------|----------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|---------|
| RSRC-001 | Datathon ERD PDF | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | N/A (in-hand) |
| RSRC-002 | FIR Schema defs | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | N/A (in-hand) |
| RSRC-003 | Challenge rules | PEND | PEND | — | — | — | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-004 | Submission format | PEND | PEND | — | — | — | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-005 | FAQ resources | PEND | PEND | — | — | — | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-006 | Catalyst credits | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | N/A (redeem) |
| RSRC-007 | Catalyst project guide | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | N/A (manual) |
| RSRC-008 | Sample data | PEND | PEND | PEND | — | PEND | PEND | PEND | — | PEND | PEND | — | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-009–015 | Catalyst docs | PEND | PEND | — | — | — | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-016 | NCRB 2022 | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | PEND | PEND | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-017 | NCRB 2021 | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | PEND | PEND | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-018 | NCRB OGD CSVs | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | PEND | — | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-019 | KSP Crime Review | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | PEND | PEND | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-020 | KSP prev year | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | PEND | PEND | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-021 | NDAP IPC stats | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | PEND | — | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-022 | OSM Overpass POIs | PEND | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | — | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-023 | Bhuvan WMS layers | PEND | PEND | — | PEND | — | — | — | PEND | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-024 | Bhuvan satellite | PEND | PEND | — | PEND | — | — | — | PEND | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-025 | Survey of India | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | ⛔ BLOCKED (license) |
| RSRC-026–028 | Census/NDAP | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | PEND | — | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-029 | Open-Meteo weather | PEND | PEND | PEND | — | PEND | PEND | PEND | PEND | PEND | PEND | — | PEND | — | PEND | PEND | ⏳ PENDING |
| RSRC-030 | IMD rainfall | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | ⛔ BLOCKED (access) |
| RSRC-031 | ECI election dates | PEND | PEND | PEND | — | PEND | PEND | PEND | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-032 | BNS 2023 text | PEND | PEND | — | — | PEND | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-033 | BNSS text | PEND | PEND | — | — | PEND | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-034 | DPDP Act | PEND | PEND | — | — | PEND | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-035 | DPDP Rules | PEND | PEND | — | — | PEND | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-040 | FollowTheMoney | PEND | PEND | — | — | — | — | — | — | PEND | PEND | PEND | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-041 | Kepler.gl | PEND | PEND | — | — | — | — | — | — | PEND | PEND | PEND | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-042 | Neo4j CE | PEND | PEND | — | — | — | — | — | — | PEND | PEND | PEND | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-043 | NetworkX | PEND | PEND | — | — | — | — | — | — | PEND | PEND | — | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-044 | MapLibre GL JS | PEND | PEND | — | — | — | — | — | — | PEND | PEND | PEND | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-045 | Cytoscape.js | PEND | PEND | — | — | — | — | — | — | PEND | PEND | PEND | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-046 | Faker | PEND | PEND | — | — | — | — | — | — | PEND | PEND | PEND | — | — | PEND | PEND | ⏳ PENDING |
| RSRC-047 | indic-faker | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | ⛔ BLOCKED (source) |

### Status Key

| Code | Meaning |
|------|---------|
| ✅ PASS | Gate passed |
| ❌ FAIL | Gate failed |
| ⏳ PEND | Download not yet complete or validation not run |
| ⏭️ SKIP | Gate not applicable |
| — | Not applicable (resource is not of this type) |
| ⛔ BLOCKED | Cannot proceed without human intervention |

---

## 3. Quality Gate Detail

### G01 — Authenticity
- **Script:** `scripts/validation/check_authenticity.py`
- **Rule:** Source URL in provenance must match the verified URL from Blueprint §C
- **Failure action:** Flag for manual review, do not promote from quarantine

### G02 — File Integrity
- **Script:** `scripts/validation/verify_checksum.py`
- **Rule:** SHA256 checksum matches expected value (or is computed on first download)
- **Failure action:** Re-download, log to `manifests/failure_log.csv`

### G03 — Schema Validity
- **Script:** `scripts/validation/validate_schema.py`
- **Rule:** Required columns present, data types as expected per Blueprint §E matrix
- **Failure action:** Flag schema mismatch, do not use until reconciled

### G04 — Geometry Validity
- **Script:** `scripts/validation/validate_geometry.py`
- **Rule:** Valid geometry, coordinates inside Karnataka bbox (lat 11.5–18.5, lon 74.0–78.5), CRS = WGS84 (EPSG:4326)
- **Failure action:** Reject geometry, log to provenance

### G05 — Temporal Validity
- **Script:** `scripts/validation/validate_temporal.py`
- **Rule:** All dates parse as valid dates; no future dates for historical data; IST timezone aligned
- **Failure action:** Flag invalid dates, do not use in temporal features

### G06 — Duplicate Detection
- **Script:** `scripts/validation/find_duplicates.py`
- **Rule:** No exact-duplicate rows (all columns match)
- **Failure action:** Log and de-duplicate, record in transformation log

### G07 — Missing-Value Profile
- **Script:** `scripts/validation/profile_missing.py`
- **Rule:** Missing values recorded by column; alert if >20% missing in a required field
- **Failure action:** Log warning, feature may be degraded

### G08 — Administrative-Code Matching
- **Script:** `scripts/validation/check_admin_codes.py`
- **Rule:** District/station codes join against Karnataka boundary reference
- **Failure action:** Flag unmapped codes for manual resolution

### G09 — Licensing
- **Script:** `scripts/validation/check_license.py`
- **Rule:** License recorded in `manifests/license_inventory.csv` before resource is used
- **Failure action:** Block usage until license documented

### G10 — Attribution
- **Script:** `scripts/validation/check_attribution.py`
- **Rule:** If license requires attribution (ODbL, CC-BY-SA, MIT, BSD), text is recorded
- **Failure action:** Log warning, ensure attribution in UI/README

### G11 — Secrets/Malware Scan
- **Script:** `scripts/validation/scan_secrets.py`
- **Rule:** No API keys, tokens, credentials, or malware signatures in repository clones
- **Failure action:** Quarantine repo, do not execute any code from it

### G12 — PII Scan
- **Script:** `scripts/validation/scan_sensitive_data.py`
- **Rule:** No real person identifiers (name patterns, phone, email, Aadhaar) in aggregate/synthetic datasets
- **Failure action:** Quarantine file, flag for manual review

### G13 — Synthetic-Data Labeling
- **Script:** `scripts/validation/check_synthetic_labels.py`
- **Rule:** Every synthetic file/record has `SYNTHETIC_` prefix or metadata tag
- **Failure action:** Reject unlabeled synthetic data

### G14 — Reproducibility
- **Script:** `scripts/validation/check_reproducibility.py`
- **Rule:** Acquisition script can be re-run (dry-run mode) with same source and produce same result
- **Failure action:** Log script dependencies; re-run may need manual steps

### G15 — Provenance
- **Script:** `scripts/validation/check_provenance.py`
- **Rule:** Entry exists in `manifests/provenance.jsonl` with source_url, access_date, checksum_sha256
- **Failure action:** Do not promote from quarantine until provenance is recorded

---

## 4. Running Validation

```powershell
# Dry-run (reports what would be validated)
python scripts/validation/validate_resources.py --dry-run

# Full validation
python scripts/validation/validate_resources.py --no-dry-run

# Validate a single resource
python scripts/validation/validate_resources.py --resource RSRC-022

# Validate by priority
python scripts/validation/validate_resources.py --priority P0

# Validate by category
python scripts/validation/validate_resources.py --category D4
```

### Outputs

| Artifact | Location |
|----------|----------|
| Per-resource validation JSON | `data/processed/validation_results.json` |
| Quality gate summary | This report |
| Failure register | `manifests/failure_log.csv` |
| Promotion log | `logs/acquisition.log` |

---

## 5. Promotion Criteria

A resource is promoted from `quarantine/` to its target directory only when:

- All applicable gates (G01–G15) pass
- License is on file (G09)
- Provenance is recorded (G15)
- Human approval granted (for MANUAL-AUTHORIZED items)

---

*This report is auto-generated by `scripts/validation/validate_resources.py`.*
