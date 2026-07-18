# Transformation Pipeline — Planning Document

> **Status:** PLANNING — No transformations executed yet.
> **Owner:** Berunda Team
> **Last Updated:** 2026-07-18

---

## Purpose

This directory will contain scripts that transform validated raw data
(from `data/raw/`) into processed, analysis-ready datasets (in `data/processed/`).

**Critical rule:** Never destructively modify a raw file. All transformations
produce new files, and every transformed record remains traceable back to its
exact source file and row.

---

## Planned Transformations (Phase 6 of Autonomous Agent Prompt)

### 1. Canonical ID Assignment
- Assign deterministic UUIDs to all entities based on source table + PK
- Format: `BERUNDA-{table}-{pk}` (e.g., `BERUNDA-CASEMASTER-00001`)

### 2. Date/Time Normalization
- Normalize all timestamps to IST (Asia/Kolkata, UTC+5:30)
- Standard format: `YYYY-MM-DDTHH:MM:SS+05:30`
- Fields: `IncidentFromDate`, `IncidentToDate`, `InfoReceivedPSDate`,
  `CrimeRegisteredDate`, `ArrestSurrenderDate`, `csdate`

### 3. Karnataka Administrative-Code Mapping
- Map district names → standard district IDs (from boundary reference)
- Map police station names → UnitIDs
- Resolve inconsistencies between source data and OSM/Bhuvan boundaries

### 4. Coordinate System Normalization
- Standardize all geospatial data to WGS84 (EPSG:4326)
- Validate coordinates within Karnataka bounding box
- Flag and quarantine any coordinates outside expected range

### 5. Crime-Category Mapping
- Map legacy IPC sections → BNS 2023 sections
- **⚠️ REQUIRES HUMAN LEGAL REVIEW before any auto-applied mapping**
- Generate a proposed mapping table for legal team sign-off
- Keep both IPC and BNS columns in the processed output

### 6. Person/Entity Pseudonymization
- For any dataset containing person-level fields (even synthetic):
  ensure clear SYNTHETIC labeling
- For any future real data: pseudonymize before internal use
- Hash-based pseudonymization preserving join capability

### 7. Feature-Table Construction
- Crime count aggregates by district × week × crime_type
- Rolling averages for anomaly detection baselines
- Person-case adjacency matrix for entity resolution
- Coordinate grid cells for hotspot density computation

### 8. Synthetic Data Generation
- Script: `scripts/generate_synthetic_data.py` (see `docs/05_DATA/SYNTHETIC_DATA_SPECIFICATION.md`)
- Uses Faker (`en_IN` locale) with deterministic seeds
- Planted hidden links per Section 5 of Synthetic Data Spec
- Output to `data/synthetic/` with SYNTHETIC_ prefix

### 9. Train/Validation/Test Splits
- Risk scoring model: 70/15/15 split on synthetic labeled data
- Entity resolution: planted duplicates as test set (separate from training)
- Temporal split: train on months 1-18, validate on 19-21, test on 22-24

---

## Traceability Requirement

Every row in `data/processed/` must include:
- `_source_file`: original filename from `data/raw/`
- `_source_row`: row number in the original file
- `_transform_version`: version tag of the transformation script
- `_transform_date`: ISO timestamp of when the transformation was applied

These fields enable full chain-of-custody from processed output back to raw source.

---

## Script Naming Convention

```
scripts/transformation/
├── transform_01_normalize_dates.py
├── transform_02_map_admin_codes.py
├── transform_03_normalize_coordinates.py
├── transform_04_map_crime_categories.py
├── transform_05_build_feature_tables.py
├── transform_06_generate_synthetic.py
└── transform_07_create_splits.py
```

Each script supports `--dry-run` (default) and writes to `data/interim/`
(intermediate) or `data/processed/` (final).
