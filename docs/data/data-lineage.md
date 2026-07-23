# Data Lineage

## Overview

Data lineage documents the origin, transformation, and destination of every data asset in the Berunda platform. This ensures reproducibility, auditability, and trustworthiness of all derived insights.

## Data Flow

```
External Sources (NCRB, KSP, Census, OSM, Weather)
    │
    ▼
data/quarantine/          ← Untrusted downloads, SHA-256 verified
    │  (validate_resources.py)
    ▼
data/raw/                 ← Immutable source data, never modified
    │
    ├── scripts/transformation/  (5-step pipeline)
    │
    ▼
data/interim/             ← Partially transformed (dates, admin codes, coords, categories)
    │
    ▼
data/processed/           ← Final curated datasets (feature tables for ML)
    │
    ├── apps/ (backend API consumption)
    ├── notebooks/ (analytics exploration)
    └── models/ (ML training)

Synthetic Data Path:
    scripts/data/generate_synthetic.py
    │
    ▼
data/synthetic/           ← Generated synthetic crime records
    │
    ├── scripts/transformation/
    │
    ▼
data/interim/ → data/processed/
```

## Provenance Tracking

Every data asset's provenance is recorded in `manifests/provenance.jsonl` with:
- `resource_id`: Unique identifier (e.g., RSRC-042)
- `source_url`: Original source URL
- `acquired_at`: ISO 8601 timestamp
- `acquired_by`: Acquisition script name
- `checksum_sha256`: Content hash for integrity verification
- `license`: SPDX license identifier
- `row_count`: Record count (for tabular data)
- `classification`: PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED

## Data Lifecycle

1. **Acquisition**: Download → quarantine → validate → promote to raw
2. **Transformation**: Raw → interim (cleaned/normalized) → processed (feature tables)
3. **Consumption**: Processed data used by apps, ML training, analytics
4. **Archive/Rotation**: Historical data archived per governance policy
