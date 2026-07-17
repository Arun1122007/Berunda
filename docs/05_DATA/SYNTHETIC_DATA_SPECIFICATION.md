# Synthetic Data Specification

[//]: # (Document ID: BERUNDA-DATA-006 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Purpose

Generate a realistic synthetic FIR dataset for development, testing, and the hackathon demo. All data is clearly labeled as synthetic within the system to prevent confusion with real records.

## 2. Tools

| Tool | Purpose | Justification |
|------|---------|--------------|
| Faker (Python) — `en_IN` locale | Generate Indian names, addresses, phone numbers | Primary generator for MVP English-language data |
| indic-faker (Python) | Generate Kannada names and addresses | STRETCH — for Kannada NER demo |
| Custom seed scripts | Generate FIR-specific structures (CrimeNo, CaseNo format, relationships) | Faker lacks FIR domain-specific generators |

## 3. Dataset Size

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Total FIRs | 2,000 - 5,000 | Sufficient for demo without overwhelming query performance |
| Districts | 5-7 (within Karnataka) | Allows meaningful district-level drill-down |
| Police stations | 10-15 (across districts) | Hierarchical drill-down from state → district → station |
| Person entities | 3,000 - 8,000 | Approximately 1.5-2x FIR count due to cross-case planting |
| Vehicles | 500 - 1,000 | Vehicle linking demonstration |
| Time span | 24 months (2024-01 to 2025-12) | Enough for temporal anomaly detection (z-score over weeks) |

## 4. Crime Distribution

Distribution approximates NCRB 2022 Karnataka state statistics (rounded for demo):

| Crime Head | % of Total | Approx. Count (at 5,000 FIRs) |
|------------|-----------|------------------------------|
| Theft | 25% | 1,250 |
| Assault / Hurt | 18% | 900 |
| Burglary | 12% | 600 |
| Motor Vehicle Theft | 10% | 500 |
| Robbery | 8% | 400 |
| Murder | 4% | 200 |
| Sexual Offences | 6% | 300 |
| Kidnapping | 5% | 250 |
| Other | 12% | 600 |

## 5. Planted Hidden Links (Demo Feature)

20-30 "hidden link" test cases are planted for the relationship discovery feature:

| Type | Planting Method | Count |
|------|----------------|-------|
| Same person, different names | One person appears across 3-4 FIRs with name variants | 10 persons × 3-4 FIRs each |
| Co-accused network | 5-8 persons appear as co-accused across multiple FIRs | 2-3 interconnected clusters |
| Accused-victim reversal | Person A is accused in FIR-1, victim in FIR-2 | 5 pairs |
| Vehicle linkage | Same vehicle appears in unrelated FIRs across districts | 10 vehicles |
| Family relationship | Same surname + same address across multiple FIRs | 5 clusters |
| Temporal anomaly spike | Deliberate week with 5x normal crime count in one district | 1 spike |

## 6. Generator Script Structure

```
scripts/generate_synthetic_data.py
  ├── generate_lookup_tables()
  │   ├── States (1 — Karnataka)
  │   ├── Districts (5-7 in Karnataka)
  │   ├── Units (10-15 police stations)
  │   ├── Employees (30-50 police officers)
  │   ├── Act/Section data (IPC, CrPC, NDPS relevant sections)
  │   ├── CrimeHead/CrimeSubHead (hierarchy)
  │   ├── CaseStatusMaster
  │   ├── OccupationMaster
  │   ├── CasteMaster (restricted — minimal, labeled synthetic)
  │   └── ReligionMaster (restricted — minimal, labeled synthetic)
  │
  ├── generate_cases(crime_distribution, count)
  │   ├── Pick district, station, employee, crime head
  │   ├── Generate CrimeNo (format: 1+4+4+4+5 digits)
  │   ├── Generate CaseNo (YYYY + serial)
  │   ├── Generate IncidentFromDate, IncidentToDate, InfoReceivedPSDate
  │   ├── Generate Latitude/Longitude (within district bounds)
  │   ├── Generate BriefFacts using LLM-augmented templates
  │   └── Return CaseMaster record
  │
  ├── generate_persons(case, planted_links)
  │   ├── For normal cases: 1 complainant, 1-2 victims, 1-3 accused
  │   ├── For planted links: use pre-defined alias mapping
  │   └── Write to ComplainantDetails, Victim, Accused
  │
  ├── generate_arrest_surrender(accused_list, case)
  │   └── 50-70% of accused have arrest records
  │
  ├── generate_act_sections(case, crime_head)
  │   └── Map crime heads to IPC sections (e.g., Murder → 302)
  │
  ├── generate_vehicles(case)
  │   └── 10-15% of cases have vehicle involvement
  │
  ├── generate_chargesheets(case)
  │   └── 40-60% of closed cases have chargesheets, 1-6 months after registration
  │
  ├── generate_anomaly_spike()
  │   └── One district-week with 5x baseline
  │
  └── tag_dataset_as_synthetic()
      └── Written to a dedicated flag table or metadata file
```

## 7. BriefFacts Narrative Generation

BriefFacts (FIR narrative) is generated using template-based text with randomized elements:

**Template structure:**
```
"On [DATE] at approximately [TIME], [COMPLAINANT_NAME] reported to [POLICE_STATION_NAME]
that on [INCIDENT_DATE] at [LOCATION_DESCRIPTION], [NARRATIVE_BODY].

[NARRATIVE_BODY]:
- Theft template: "unknown person(s) broke into [PREMISES_TYPE] at [ADDRESS]
  and stole [STOLEN_ITEMS] valued at approximately [AMOUNT] rupees."
- Assault template: "[ACCUSED_NAME(S)] assaulted [VICTIM_NAME(S)] using [WEAPON]
  causing [INJURY_DESCRIPTION]."
- Vehicle theft: "the accused drove away [VEHICLE_DESCRIPTION] ([VEHICLE_NUMBER])
  which was parked at [LOCATION]."
```

**Variation:** Each template has 5-10 variant phrasings selected randomly.

**LLM augmentation (STRETCH):** If time permits, use an LLM to rewrite template-based narratives into more natural-sounding text while preserving all named entities.

## 8. Data Labeling

Every synthetic record must be clearly identifiable:

- A `_synthetic_data_tag` table with a single row: `{ "dataset": "synthetic", "generated_at": "2026-07-16T00:00:00Z", "generator_version": "1.0", "faker_seed": 42 }`
- All CSV export files contain: `# GENERATED SYNTHETIC DATA — NOT REAL FIR RECORDS #` as first line
- The demo evidence pack includes a prominent "SYNTHETIC DATA" watermark

## 9. Deterministic Seeding

| Parameter | Value |
|-----------|-------|
| Faker seed | 42 |
| Random seed | 12345 |
| NumPy seed | 67890 |
| Generator version | 1.0 (incremented on schema changes) |

Deterministic seeding ensures the same synthetic dataset is generated each run, enabling reproducible testing and demo production.

## 10. Output Format

The generator produces:

1. **SQL INSERT scripts** — one per table, directly loadable into Catalyst Data Store
2. **CSV files** — one per table, for manual inspection or alternative loading
3. **Planting manifest JSON** — documents all planted hidden links for verification

```
output/
├── sql/
│   ├── 01_lookup_tables.sql
│   ├── 02_case_master.sql
│   ├── 03_persons.sql
│   ├── 04_arrest_surrender.sql
│   ├── 05_act_sections.sql
│   ├── 06_vehicles.sql
│   ├── 07_chargesheets.sql
│   └── 08_tag_synthetic.sql
├── csv/
│   ├── CaseMaster.csv
│   ├── ComplainantDetails.csv
│   └── ...
└── planting_manifest.json
```
