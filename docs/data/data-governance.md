# Data Governance

## Classification Levels

| Level | Definition | Examples | Handling Requirements |
|-------|-----------|----------|----------------------|
| **PUBLIC** | Freely shareable | Open government data, synthetic demo data | No restrictions |
| **INTERNAL** | Team-only | Design docs, configuration templates | Access controlled via repo permissions |
| **CONFIDENTIAL** | Sensitive operational data | System architecture, API keys (masked) | Encrypted at rest, role-based access |
| **RESTRICTED** | Legally protected | Real PII, case details | Never committed; placeholder only |

## Principles

1. **Raw data is immutable**: Never modify `data/raw/`. Always transform via scripts.
2. **Reproducibility**: Every dataset can be regenerated from source + scripts.
3. **Provenance**: Every data file has a recorded origin in `manifests/provenance.jsonl`.
4. **License compliance**: All data sources' licenses are tracked in `manifests/license_inventory.csv`.
5. **PII protection**: No real Personally Identifiable Information is committed. All data is synthetic or aggregated.
6. **Synthetic labeling**: All generated data is prefixed with `SYNTHETIC_` and contains appropriate metadata.

## Retention Policy

| Data Type | Environment | Retention | Action |
|-----------|------------|-----------|--------|
| Raw source data | All | Indefinite | Preserved as acquired |
| Processed data | Dev/Test | 90 days | Refresh on next pipeline run |
| Synthetic data | All | Indefinite | Versioned by seed & tier |
| Logs | Dev | 7 days | Auto-rotation |
| Logs | Prod | 90 days | Compressed archive |
| Audit logs | All | 365 days | Append-only, tamper-evident |

## Data Quality Gates

Before promotion from `quarantine/` to `raw/`, every resource must pass:
1. **Integrity**: SHA-256 hash match
2. **Parse validity**: CSV/JSON/XML schema compliance
3. **Temporal validity**: Date ranges within expected bounds
4. **Null checks**: Missing value rates below threshold
5. **Duplicate detection**: Unique key violations flagged
6. **PII scan**: No real personal data patterns detected
7. **License check**: License documented and compatible

See `docs/data/DATA_QUALITY_PROFILING_AND_VALIDATION_PLAN.md` for full details.
