# Data Directory — Governance & Organization

> **Last Updated:** 2026-07-18
> **Classification:** Internal
> **Owner:** Berunda Data Team

---

## Directory Structure

```
data/
├── raw/                    # Immutable source data, as acquired
│   ├── ncrb/               # NCRB crime reports
│   ├── census/             # Census of India data
│   ├── osm/                # OpenStreetMap extracts
│   ├── weather/            # Open-Meteo historical weather
│   ├── police/             # Police jurisdictional boundaries
│   └── legislative/        # BNS/BNSS/BSA legal texts
├── interim/                # Transformed, partially cleaned data
├── processed/              # Final curated datasets ready for consumption
├── external/               # Data from third-party partners (under NDA where applicable)
├── synthetic/              # Artificially generated demo/evaluation data
├── samples/                # Small subsets for development & testing
├── quarantine/             # New downloads awaiting validation
├── restricted-placeholders/ # Placeholder markers for data not yet acquired
├── organizer/              # Internal metadata, manifests, and lookup tables
└── README.md               # This file
```

---

## Data Classification

All data in this repository falls under one of the following classifications:

| Classification | Tag | Description | Example |
|---------------|-----|-------------|---------|
| **Public** | `public` | Freely available, no restrictions | Census India tables, OpenStreetMap extracts |
| **Internal** | `internal` | Team-internal curated views | Processed crime-rate indexes, merged geographies |
| **Confidential** | `confidential` | Restricted to named team members | Partner NDA data, pre-release analytics |
| **Restricted** | `restricted` | Legal or contractual restrictions | Live police FIR data (not yet acquired) |
| **Synthetic** | `synthetic` | Artificially generated, no real PII | Demo FIR records, test entity graphs |
| **Generated** | `generated` | Produced by pipeline code, not sourced externally | Feature-engineered tables, cache files |

Each file or subdirectory SHOULD carry a `.metadata.yml` companion or be registered in the dataset manifest under `data/organizer/`.

---

## Data Lifecycle

```
                      ┌─────────────┐
                      │  External   │
                      │   Source    │
                      └──────┬──────┘
                             │ download
                             ▼
                      ┌─────────────┐
                      │  Quarantine │  ─── validation & checksum
                      └──────┬──────┘
                             │ pass
                             ▼
                      ┌─────────────┐
                      │    Raw      │  ─── immutable, write-once
                      └──────┬──────┘
                             │ transform
                             ▼
                      ┌─────────────┐
                      │   Interim   │  ─── partial cleaning, join, normalize
                      └──────┬──────┘
                             │ curate
                             ▼
                      ┌─────────────┐
                      │  Processed  │  ─── ready for consumption
                      └─────────────┘
```

1. **Quarantine** — every new download lands here first. Must pass validation (checksum, schema check, virus scan).
2. **Raw** — immutable copy of source data. Never modified after ingestion.
3. **Interim** — working area for transformation scripts. May be regenerated.
4. **Processed** — final, versioned datasets consumed by applications and models.

---

## Data Provenance Requirements

Every dataset MUST include provenance metadata. Store as `<dataset>/_provenance.yml` or in the central manifest:

```yaml
dataset: ncrb_crime_2023
source: https://ncrb.gov.in/
acquired_at: 2026-07-18T10:00:00Z
acquired_by: acquisition-agent-v1
checksum_sha256: a1b2c3d4...
license: Government Open Data License
row_count: 15234
schema_version: 1.0
classification: public
```

Provenance is recorded in `data/organizer/dataset_manifest.csv` and `logs/acquisition.log`.

---

## PII Handling Policy

- **All demo data is synthetic.** No real personally identifiable information (PII) is ever stored in this repository.
- Synthetic data is generated using Faker with Indian-locale providers and follows the schema in `docs/05_DATA/SYNTHETIC_DATA_SPECIFICATION.md`.
- Any real data acquired (e.g., open census tables) contains only aggregate statistics, never individual-level records.
- If confidential or restricted data is ever staged, it MUST be stored in `data/restricted-placeholders/` as a pointer file only — the actual data remains outside this repository.

---

## Large File Management

- Files > 50 MB MUST NOT be committed to Git. Use Git LFS or external storage.
- Large datasets (>200 MB) require human approval before acquisition (see AGENTS.md rule 9).
- For large processed datasets, store only a sample in `data/samples/` and reference the full dataset location in the manifest.
- Binary data (shapefiles, PDFs) goes to `data/external/` with a companion metadata file.

---

## Schema Documentation

- Formal schema definitions live in `docs/05_DATA/`.
- `CANONICAL_DATA_MODEL.md` — entity definitions and relationships.
- `DATA_DICTIONARY.md` — field-level descriptions for all datasets.
- `SYNTHETIC_DATA_SPECIFICATION.md` — schema for generated demo data.
- `SOURCE_ERD_RECONCILIATION.md` — mapping from source ERDs to canonical model.
- Inline schema references should link to these documents.

---

## How to Add New Datasets

1. Create an entry in `data/organizer/dataset_manifest.csv` with dataset name, source URL, and classification.
2. Download the data to `data/quarantine/` via the appropriate acquisition script in `scripts/acquisition/`.
3. Run validation (checksum, null checks, schema conformance).
4. On pass, move to `data/raw/<dataset_name>/` as an immutable copy.
5. Create transformation script in `scripts/transform/` to produce interim and processed views.
6. Register the processed dataset in the data catalog.
7. If the dataset contains PII-like fields (even synthetic), note it in the metadata.

---

## Data Dictionary Reference

Detailed field-level definitions are maintained in:

| Document | Path | Scope |
|----------|------|-------|
| Data Dictionary | `docs/05_DATA/DATA_DICTIONARY.md` | All processed datasets |
| Canonical Data Model | `docs/05_DATA/CANONICAL_DATA_MODEL.md` | Entity-relationship model |
| Synthetic Data Spec | `docs/05_DATA/SYNTHETIC_DATA_SPECIFICATION.md` | Generated demo data |
| Entity Resolution Spec | `docs/05_DATA/ENTITY_RESOLUTION_SPECIFICATION.md` | Record linkage rules |
| Source ERD Reconciliation | `docs/05_DATA/SOURCE_ERD_RECONCILIATION.md` | Source-to-canonical mapping |
| Data Governance | `docs/05_DATA/DATA_GOVERNANCE_RETENTION_AND_PROVENANCE.md` | Retention and provenance policies |
