# Demo Data Story and Expected Results

## 1. Objective
To provide a stable, repeatable hackathon demonstration pathway that exercises all 12 Phase 1-3 P0 requirements without exposing real PII.

## 2. Actors
- **Demo_Officer_1**: Investigating Officer at Koramangala PS.
- **Demo_Supervisor_1**: Station House Officer (SHO) at Koramangala PS.

## 3. The Walkthrough Sequence

### Step 1: FIR Ingestion & AI Extraction (F-001, F-006)
- **Action**: `Demo_Officer_1` uploads a synthetic FIR text: "Red Honda Activa KA-01-AB-1234 stolen from Koramangala BDA complex."
- **Expected Data**: AI extracts date, location, vehicle (`Honda Activa`, `Red`, `KA-01-AB-1234`).
- **Data Source**: `fir-extraction-evaluation.jsonl` (Sample EXT-001).

### Step 2: Human-in-the-Loop Review (F-007b)
- **Action**: `Demo_Officer_1` reviews the extracted fields. The UI explicitly flags this as an "AI Suggestion".
- **Action**: Officer clicks "Approve and Save to Data Store".
- **Expected Data**: Record inserted into `CaseMaster` with `human_reviewed = true`.

### Step 3: Semantic Search & Risk (F-008, F-006)
- **Action**: Officer opens the "Ask Berunda" chat and types: "Find cases with a red Honda Activa stolen recently."
- **Expected Data**: The system surfaces the newly ingested FIR, along with 2 historical synthetic FIRs involving red scooters.
- **Data Source**: `semantic-search-evaluation.jsonl` (Sample SS-002).

### Step 4: Case Linking (F-004, F-007)
- **Action**: Officer views the FIR dashboard. Berunda suggests a "Strongly Related" case from Indiranagar PS where a "Red Honda Activa" was recovered.
- **Expected Data**: Link Analysis graph shows an edge connecting the two FIRs via the `VehicleLink` node.
- **Data Source**: `related-case-evaluation.jsonl` (Sample RC-001).

### Step 5: Audit & Governance (F-010)
- **Action**: `Demo_Supervisor_1` logs in and views the Audit Dashboard.
- **Expected Data**: The dashboard shows a trail of: `AI_EXTRACTION_PERFORMED`, `HUMAN_REVIEW_ACCEPTED`, `FIR_CREATED`. All actions are tied to `Demo_Officer_1`.
