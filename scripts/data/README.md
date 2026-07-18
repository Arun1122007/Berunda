# Synthetic Data Generation Pipeline

> **Project Berunda** — Karnataka State Police Datathon 2026

## Overview

The synthetic data generator produces realistic-but-fictional FIR (First Information Report)
records for development, testing, and the hackathon demo. All data is clearly labeled
**SYNTHETIC** to prevent confusion with real police records.

**Script:** `scripts/data/generate_synthetic.py`  
**Configuration:** `scripts/data/synthetic_config.json`  
**Output Directory:** `data/synthetic/`

---

## Quick Start

```bash
# Generate demo dataset (2000 records, all patterns, CSV format)
python scripts/data/generate_synthetic.py --tier demo --scenario all

# Smoke test (200 records, JSON format)
python scripts/data/generate_synthetic.py --tier smoke --format json

# Stress test with custom seed
python scripts/data/generate_synthetic.py --tier stress --seed 12345
```

### Prerequisites

```bash
pip install faker
```

---

## CLI Reference

| Argument | Default | Description |
|----------|---------|-------------|
| `--tier` | `demo` | Scale tier: `smoke` (200), `demo` (2000), `stress` (10000) |
| `--scenario` | `all` | Planted pattern: `hotspot`, `serial-mo`, `linked-cases`, `anomaly-spike`, `all`, `none` |
| `--seed` | `42` | Deterministic random seed for reproducibility |
| `--format` | `csv` | Output format: `csv` or `json` |
| `--output-dir` | `data/synthetic/` | Output directory |
| `--config` | `scripts/data/synthetic_config.json` | Configuration file path |

---

## Data Model & Entity Relationships

The generator produces 9 entity files that mirror the canonical data model:

```
CaseMaster (FIR/case records)
    ├── CrimeNo, CaseNo, CrimeRegisteredDate
    ├── FK → PoliceStation (Unit), Employee (Officer)
    ├── FK → CrimeHead, CrimeSubHead, CaseCategory, GravityOffence
    └── FK → CaseStatus, Court
        │
        ├── 1:1 ── Inv_OccuranceTime (incident details, lat/lon, BriefFacts)
        │
        ├── 1:N ── ComplainantDetails
        │
        ├── 1:N ── VictimDetails
        │
        ├── 1:N ── AccusedDetails
        │
        ├── 1:N ── EvidenceMaster (weapons, forensic, digital evidence)
        │
        ├── 1:N ── ChargesheetDetails (filing status, court)
        │
        ├── 1:N ── VehicleLink (vehicle registrations linked to cases)
        │
        └── 1:N ── RelationshipMaster (person-to-person, person-to-case)
```

### File Naming Convention

```
SYNTHETIC_{Entity}_{tier}_{seed}.csv
SYNTHETIC_{Entity}_{tier}_{seed}.json
```

Examples:
- `SYNTHETIC_CaseMaster_demo_42.csv`
- `SYNTHETIC_AccusedDetails_demo_42.csv`
- `SYNTHETIC_GroundTruth_demo_42.json` (metadata)

### Entity Attributes

All records include a `synthetic: true` field for clear data labeling.

| Entity | Key Fields | Notes |
|--------|------------|-------|
| CaseMaster | CaseMasterID, CrimeNo, CaseNo | Central FIR record |
| Inv_OccuranceTime | CaseMasterID, Lat, Lon, BriefFacts | 1:1 with CaseMaster |
| ComplainantDetails | ComplainantID, CaseMasterID, Name, Age | 1-2 per case |
| VictimDetails | VictimMasterID, CaseMasterID, Name | 0-3 per case |
| AccusedDetails | AccusedMasterID, CaseMasterID, Name, PersonID | 1-8 per case |
| VehicleLink | VehicleLinkID, VehicleNumber, CaseMasterID | ~15% of cases |
| ChargesheetDetails | CSID, CaseMasterID, csdate, cstype | ~55% of cases |
| EvidenceMaster | EvidenceID, CaseMasterID, Type | ~35% of cases |
| RelationshipMaster | RelationshipID, CaseMasterID, PersonA, PersonB | Intra-case links |

---

## Planted Pattern Specifications

The generator injects detectable patterns when `--scenario` is not `none`.

### 1. Hotspot

A geographic crime cluster in one district.

| Property | Value |
|----------|-------|
| Pattern Type | `hotspot` |
| Cluster Size | ~1.5% of tier case count (min 15) |
| Radius | ~2 km |
| District | Bengaluru Urban (default) or similar |
| Crime Type | Theft, Hurt / Assault, Robbery |
| Detection Target | Geospatial clustering algorithms (DBSCAN, KDE) |

**Ground truth marker:** BriefFacts includes `[HOTSPOT MARKER: Cluster incident within Xkm of (lat, lon)]`

### 2. Serial MO

Multiple cases with matching modus operandi.

| Property | Value |
|----------|-------|
| Pattern Type | `serial-mo` |
| Case Count | 5-8 (tier-dependent) |
| Fixed Elements | Shared MO template, consistent accused name |
| Crime Types | Theft, Burglary, Robbery, Cheating/Fraud |
| Detection Target | MO text similarity, named entity matching |

**Ground truth marker:** BriefFacts includes `[SERIAL MO MARKER: Shared MO signature — ...]`

### 3. Linked Cases

Cases across different districts sharing the same accused.

| Property | Value |
|----------|-------|
| Pattern Type | `linked-cases` |
| Case Count | 3-6 |
| Districts | 3+ different districts |
| Shared Element | Same accused name across all cases |
| Crime Types | Property crimes, cheating |
| Detection Target | Cross-district entity resolution |

**Ground truth marker:** BriefFacts includes `[LINKED CASES MARKER: Cross-district accused match — ...]`

### 4. Anomaly Spike

Unusual crime type in a normally low-crime district.

| Property | Value |
|----------|-------|
| Pattern Type | `anomaly-spike` |
| Spike Count | 5-10 cases in 1 week |
| District | Low-crime area (weight < 2.0) |
| Crime Type | Cyber Crime, NDPS, Arms Act, Dacoity, Extortion |
| Detection Target | Temporal anomaly detection (z-score) |

**Ground truth marker:** BriefFacts includes `[ANOMALY SPIKE MARKER: Unusual ... incident in ... district]`

---

## Ground Truth Metadata Format

The ground truth file (`SYNTHETIC_GROUND_TRUTH_{tier}_{seed}.json`) documents every
planted pattern for automated validation:

```json
{
  "generator": "generate_synthetic.py",
  "version": "1.0.0",
  "generated_at": "2026-07-18T10:30:00",
  "total_planted_patterns": 4,
  "patterns": [
    {
      "pattern_type": "hotspot",
      "description": "20 incidents within ~2km radius in Bengaluru Urban district",
      "case_ids": [1, 2, 3, ..., 20],
      "details": {
        "district": "Bengaluru Urban",
        "cluster_size": 20,
        "radius_km": 2.0,
        "center_lat": 12.9716,
        "center_lon": 77.5946,
        "crime_head": "Theft"
      },
      "timestamp": "2026-07-18T10:30:00"
    }
  ]
}
```

---

## Validation

Generated data can be validated using the existing validation pipeline:

```bash
# Run all quality gates on synthetic CSV files
python scripts/validation/validate_resources.py

# Run geospatial validation on hotspot data
python scripts/validation/validate_geospatial.py
```

The synthetic data passes these gates automatically:
- **file_integrity** — non-empty files with correct format
- **csv_parse** — valid CSV structure
- **synthetic_label** — `SYNTHETIC` marker in filename and content
- **temporal_validity** — dates between 2023-2025
- **duplicate_detection** — no exact duplicate rows
- **pii_scan** — all PII is synthetic (no real Aadhaar/PAN patterns)

---

## Integration with Validation Pipeline

The validation script (`scripts/validation/validate_resources.py`) includes a dedicated
`synthetic_label` gate (line 275-287) that verifies synthetic files carry the proper marker.

To validate synthetic output:
1. Run the generator as described above
2. Point the validation script at `data/synthetic/`
3. Check the validation report for `synthetic_label: PASS`

---

## Deterministic Seeding

| Parameter | Value |
|-----------|-------|
| Faker seed | `--seed` value (default 42) |
| Python random seed | `--seed` value (default 42) |
| Generator version | 1.0.0 |

The same seed always produces identical output, enabling reproducible testing.

---

## Distributions

### Geographic (District Weighting)

| District | Weight |
|----------|--------|
| Bengaluru Urban | 25.0% |
| Belagavi | 7.8% |
| Mysuru | 5.5% |
| Dakshina Kannada | 4.5% |
| Kalaburagi | 3.8% |
| Bengaluru Rural | 3.5% |
| Ballari | 3.2% |
| ... (31 districts total) | ... |

### Crime Type Distribution

Based on NCRB 2022 Karnataka state statistics (approximate):

| Crime Head | % of Total |
|------------|-----------|
| Theft | 25% |
| Hurt / Assault | 18% |
| Burglary | 12% |
| Motor Vehicle Theft | 10% |
| Robbery | 8% |
| Cheating / Fraud | 7% |
| Rape / Sexual Assault | 6% |
| Kidnapping | 5% |
| Murder | 4% |
| Cyber Crime | 3.5% |
| Others | 6.5% |

### Demographic Balancing

- Gender: Male 48%, Female 48%, Transgender 4%
- Ages: Role-appropriate ranges (5-80)
- Occupations: Diverse across 25 categories
- Names: Kannada/Indian names with 40+ last names

---

## Configuration File

`synthetic_config.json` contains all tunable parameters:

| Section | Contents |
|---------|----------|
| districts | 31 Karnataka districts with codes, weights, geo-bounds |
| crime_heads | 20 crime types with weights, legal sections |
| police_stations | 100+ station names mapped to districts |
| person_names | Name lists (male, female, last), occupations, ID proof types |
| mo_templates | Narrative templates per crime type with slot-filling |
| vehicle_types | 5 vehicle types with specific models |
| evidence_types | 8 evidence categories with subtypes |
| chargesheet_types | A/B/C types with distribution weights |

---

## Output Directory Structure

```
data/synthetic/
├── SYNTHETIC_CaseMaster_{tier}_{seed}.csv
├── SYNTHETIC_Inv_OccuranceTime_{tier}_{seed}.csv
├── SYNTHETIC_ComplainantDetails_{tier}_{seed}.csv
├── SYNTHETIC_VictimDetails_{tier}_{seed}.csv
├── SYNTHETIC_AccusedDetails_{tier}_{seed}.csv
├── SYNTHETIC_VehicleLink_{tier}_{seed}.csv
├── SYNTHETIC_ChargesheetDetails_{tier}_{seed}.csv
├── SYNTHETIC_EvidenceMaster_{tier}_{seed}.csv
├── SYNTHETIC_RelationshipMaster_{tier}_{seed}.csv
├── SYNTHETIC_GroundTruth_{tier}_{seed}.json
└── SYNTHETIC_GENERATION_REPORT_{tier}_{seed}.md
```

---

## Safety & Compliance

- **All data is synthetic** — no real PII, FIRs, or police records
- **SYNTHETIC marker** in every filename, every CSV header, every record
- **No real Aadhaar/PAN patterns** — generated IDs use non-standard formats
- **Restricted fields** (caste, religion) can be excluded via config
- **Quarantine-compatible** — output goes to `data/synthetic/`, not quarantine/
