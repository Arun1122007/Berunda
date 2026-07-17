# Low-Level Design

[//]: # (Document ID: BERUNDA-LLD-001 | Status: DRAFT | Classification: CONFIDENTIAL)

---

## 1. Component Design

### 1.1 FIR Ingestion Function

| Field | Detail |
|-------|--------|
| **Trigger** | HTTP POST / API file upload event |
| **Runtime** | Catalyst Function (Node.js or Python) |
| **Input** | CSV/Excel file, validated schema |
| **Output** | CaseMaster records with linked tables |
| **Key Logic** | Parse CrimeNo, extract district/station/year; validate FK references; insert with transaction |
| **Error Handling** | Row-level error reporting, no partial inserts |

**Acceptance:** A valid CSV produces complete case records. An invalid CSV returns line-level errors without data corruption.

### 1.2 NER Entity Extraction Function

| Field | Detail |
|-------|--------|
| **Trigger** | Post-ingestion event / HTTP POST |
| **Runtime** | Catalyst Function (Python) |
| **Model** | spaCy en_core_web_lg |
| **Input** | Inv_OccuranceTime.BriefFacts text |
| **Output** | Extracted entities → PersonEntityLink, VehicleLink |
| **Key Logic** | Language detection (English first); NER pipeline; confidence scoring |
| **Caveat** | Kannada NER deferred to STRETCH |

### 1.3 Entity Resolution Function

| Field | Detail |
|-------|--------|
| **Trigger** | Post-NER event |
| **Runtime** | Catalyst Function (Python) |
| **Algorithm** | Blocking: same district + age band (±3 years) |
| **Scoring** | Weighted: name phonetic (0.4) + name edit distance (0.3) + address overlap (0.2) + age match (0.1) |
| **Thresholds** | HIGH: >0.85 (auto-link), LOW: <0.50 (new entity), GREY: 0.50-0.85 (manual review) |
| **Output** | PersonEntity + PersonEntityLink records |

### 1.4 Risk Scoring (QuickML AutoML)

| Field | Detail |
|-------|--------|
| **Trigger** | Scheduled or on-demand |
| **Platform** | Catalyst QuickML AutoML (tabular) |
| **Feature Set** | Prior case count, recency (days since last), offense-type diversity, offense severity distribution, resolution outcome ratio |
| **Excluded Features** | CasteID, ReligionID, GenderID, surname-only, neighborhood-only |
| **Output** | RiskScore(score_id, person_entity_id, score_type, value, computed_at, feature_importance) |
| **Explainability** | QuickML native feature importance |

### 1.5 Link Analysis (AppSail)

| Field | Detail |
|-------|--------|
| **Trigger** | API request from dashboard |
| **Runtime** | Catalyst AppSail (Python/FastAPI + NetworkX) |
| **Algorithm** | Degree centrality, shortest path (BFS), connected components |
| **Input** | RelationshipEdge, VehicleLink, PersonEntityLink from Data Store |
| **Output** | Graph JSON for client-side rendering (node-link format) |

### 1.6 Anomaly Detection Function

| Field | Detail |
|-------|--------|
| **Trigger** | Cron schedule (nightly) |
| **Algorithm** | Z-score = (current_count - baseline_mean) / baseline_std |
| **Parameters** | Rolling window: 8 weeks baseline, threshold: z > 2.0 |
| **Dimensions** | (district, crime_type, week) |
| **Output** | Alert record with deviation magnitude |

### 1.7 RAG Query Service

| Field | Detail |
|-------|--------|
| **Platform** | Catalyst QuickML (LLM Serving + RAG) |
| **LLM** | Qwen 2.5 (via QuickML) |
| **Retrieval** | Vector similarity over curated case summary corpus |
| **Safety** | No free-form SQL generation; parameterized query templates only |
| **Role Filtering** | Retrieve only documents within user's jurisdiction |
| **Citations** | Every answer includes source document references |
| **Refusal** | "Insufficient evidence" for unanswerable queries |

## 2. Data Model Implementation Notes

### 2.1 Indexing Strategy

| Table | Index | Type |
|-------|-------|------|
| CaseMaster | (CrimeMajorHeadID, CrimeRegisteredDate, PoliceStationID) | Composite B-tree |
| CaseMaster | (DistrictID extracted from CrimeNo) | B-tree |
| Inv_OccuranceTime | (BriefFacts) | FULLTEXT |
| PersonEntityLink | (person_entity_id) | B-tree |
| RelationshipEdge | (person_entity_id_a, person_entity_id_b) | Composite B-tree |
| ComplainantDetails | (CasteID) | **NOT INDEXED for general search** |

### 2.2 CrimeNo Parsing

Format: `[1-digit CaseCategory][4-digit DistrictID][4-digit UnitID][4-digit Year][5-digit Serial]`
Example: `104430006202600001` = Category 1 (FIR), District 0443, Unit 0006, Year 2026, Serial 00001

Parse at ingestion: extract `parsed_district_id`, `parsed_unit_id`, `parsed_year`, `parsed_serial` as separate indexed columns.

### 2.3 Synthetic Data Seed

- RNG seed: `BERUNDA_2026_DEMO`
- Target: 2000-5000 FIRs
- Planted patterns: 1 repeat-offender (4 cases, 4 names), 1 shared-vehicle (3 cases), 1 hotspot week (3x spike in 1 district, 1 crime type)
