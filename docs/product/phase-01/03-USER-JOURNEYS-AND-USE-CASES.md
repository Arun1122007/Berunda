# 03 — User Journeys and Use Cases

**Document ID:** BERUNDA-PH1-USECASES-001
**Version:** 1.0 | **Status:** APPROVED — Authoritative Phase 1 workflow definition
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This document defines the end-to-end user journeys and detailed use cases for the Berunda MVP.
> Every screen design, API endpoint, and test case must trace to a use case here.
> Use cases marked MVP must be implemented and demoable. Stretch and Vision are documented for roadmap purposes.

---

## 1. Overview

### Use Case Priority Legend

| Tag | Meaning |
|-----|---------|
| ✅ MVP | Must be implemented and demonstrated in the hackathon |
| 🧩 STRETCH | Buildable if time permits; not required for demo |
| 🔭 VISION | Documented for roadmap; not attempted now |

### Use Cases in This Document

| UC-ID | Name | Priority | Primary Actor |
|-------|------|----------|---------------|
| UC-001 | Authenticate and Select Role | ✅ MVP | All users |
| UC-002 | Create FIR Manually | ✅ MVP | INVESTIGATOR |
| UC-003 | Upload FIR Document for AI Extraction | ✅ MVP | INVESTIGATOR |
| UC-004 | Review, Correct, and Approve AI Extraction | ✅ MVP | INVESTIGATOR |
| UC-005 | Search for a Person, Vehicle, or Case | ✅ MVP | INVESTIGATOR, SCRB_ANALYST |
| UC-006 | View Case Detail and Investigation Timeline | ✅ MVP | INVESTIGATOR |
| UC-007 | Review and Approve Entity Resolution Merge | ✅ MVP | INVESTIGATOR |
| UC-008 | View Relationship Graph for a Person or Case | ✅ MVP | INVESTIGATOR, SCRB_ANALYST |
| UC-009 | View Geospatial Hotspot Map | ✅ MVP | SHO (INVESTIGATOR), SCRB_ANALYST |
| UC-010 | View Explainable Risk Score | ✅ MVP | INVESTIGATOR, SCRB_ANALYST |
| UC-011 | Detect and View Anomaly Alerts | ✅ MVP | SHO (INVESTIGATOR), SCRB_ANALYST |
| UC-012 | Ask Berunda (Natural Language Query) | ✅ MVP | INVESTIGATOR, SCRB_ANALYST |
| UC-013 | View Fairness Verification Dashboard | ✅ MVP | COMPLIANCE |
| UC-014 | Review Audit Log | ✅ MVP | COMPLIANCE, ADMIN |
| UC-015 | Manage Users and Roles (Admin) | ✅ MVP | ADMIN |
| UC-016 | Add Investigation Notes | 🧩 STRETCH | INVESTIGATOR |
| UC-017 | Link Evidence Metadata | 🧩 STRETCH | INVESTIGATOR |
| UC-018 | Generate Statutory Report | 🧩 STRETCH | SCRB_ANALYST, COMPLIANCE |
| UC-019 | Kannada NER Extraction | 🔭 VISION | INVESTIGATOR |
| UC-020 | Real CCTNS Data Bridge | 🔭 VISION | System |

---

## 2. End-to-End User Journeys

These journeys represent the complete flows that will be demonstrated to judges.

### JOURNEY-001 — FIR Registration to Intelligence Discovery (Primary Demo Journey)

**Actor:** Inspector Ananya (INVESTIGATOR)

```
1. Ananya logs in → system authenticates and scopes her to Electronic City Division
2. Ananya opens a new FIR form
3. Ananya types or uploads the FIR document
4. System calls NER service → extracts persons, vehicles, locations, legal sections
5. Ananya reviews extraction → corrects one name → approves
6. FIR is saved → extraction is stored → entities are queued for entity resolution
7. Entity resolution engine runs → finds Ananya's suspect matches 3 prior cases
8. Ananya receives notification → opens entity resolution review page
9. Ananya reviews the match (confidence: 82%) → approves the merge
10. PersonEntity is updated → all 4 cases are now linked to one resolved identity
11. Ananya opens the PersonEntity → sees relationship graph
12. Ananya clicks "Find hidden links" → system runs shortest-path traversal
13. Graph shows Case 001 and Case 042 are connected through a shared vehicle
14. Ananya asks: "What is the connection between FIR-001 and FIR-042?" → Ask Berunda answers with a cited explanation
15. Audit log records all steps: FIR created, extraction approved, merge approved, graph viewed, RAG queried
```

**Expected duration:** 5 minutes in demo | 10-20 minutes in real use

---

### JOURNEY-002 — State Command View (SCRB Analyst Journey)

**Actor:** Analyst Priya (SCRB_ANALYST)

```
1. Priya logs in → state-wide dashboard loads
2. Priya views the Karnataka heatmap → Bengaluru Urban shows anomaly flag
3. Priya drills down: state → Bengaluru Urban district → Electronic City Division
4. Priya sees crime type breakdown: theft is elevated (z-score 4.2 this week)
5. Priya filters the entity list by crime type: theft, this week → 47 cases
6. Priya searches for a vehicle KA-01-AB-9999 → sees it appears in 5 theft cases
7. Priya views risk scores for accused persons in those 5 cases
8. Priya opens Ask Berunda: "Summarise the vehicle theft trend in Bengaluru Urban this week"
9. Ask Berunda returns a cited summary grounded in the 47 retrieved FIR records
10. Audit log records all actions
```

**Expected duration:** 3 minutes in demo | 15-30 minutes in real use

---

### JOURNEY-003 — Governance and Fairness Verification

**Actor:** Krishnamurthy (COMPLIANCE)

```
1. Krishnamurthy logs in → sees Compliance dashboard
2. Krishnamurthy opens Fairness Dashboard
3. System shows: fairness check ran this morning → all models PASS → CasteID and ReligionID are not in any feature set
4. Krishnamurthy clicks "View evidence" → sees feature importance table for risk score model → confirms no restricted features
5. Krishnamurthy opens Audit Log → searches for officer ID "ANANYA" and date range "today"
6. Audit log shows: FIR created, extraction approved, entity merge approved, graph viewed, RAG queried
7. Krishnamurthy marks the compliance review as complete
```

**Expected duration:** 2 minutes in demo | 15 minutes in real use

---

## 3. Detailed Use Cases

---

### UC-001 — Authenticate and Select Role

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-001 |
| **Priority** | ✅ MVP |
| **Actors** | All users |
| **Preconditions** | User account exists in the system; user knows their credentials |
| **Trigger** | User navigates to the Berunda URL |
| **Goal** | User is authenticated and arrives at the correct role-specific dashboard |

**Main Flow:**
1. System displays the login page with username and password fields
2. User enters credentials and submits
3. System validates credentials against stored hash (bcrypt); verifies account is active
4. System issues a signed JWT containing: user ID, role, district scope, issued-at, expiry (15 minutes)
5. System redirects to the role-specific dashboard:
   - INVESTIGATOR → Case Management view (own district)
   - SCRB_ANALYST → State Command Dashboard (all districts)
   - COMPLIANCE → Compliance and Audit Dashboard
   - ADMIN → System Administration panel

**Alternative Flows:**
- A1 (Invalid credentials): System returns a generic error — "Invalid credentials." System logs the failed attempt. After 5 consecutive failures, account is locked for 15 minutes.
- A2 (Account locked): System shows a locked message; Admin must unlock via Admin panel.
- A3 (Session expired): System detects expired JWT → redirects to login page → preserves the originally requested URL for post-login redirect.

**Postconditions:**
- User is authenticated and has an active JWT session
- User sees the correct role-specific dashboard with correctly scoped data

**Audit Event Generated:** `AUTH.LOGIN` on success; `AUTH.LOGIN_FAILURE` on failure

**Test Cases:**
- T-001.1: Valid credentials → correct dashboard for each of the 4 roles
- T-001.2: Invalid password → error message; no dashboard shown
- T-001.3: Account locked after 5 failures → locked message shown
- T-001.4: Expired JWT → redirected to login
- T-001.5: JWT does not grant access to a resource above the user's role → 403 returned

---

### UC-002 — Create FIR Manually

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-002 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (own district) |
| **Preconditions** | User is authenticated as INVESTIGATOR; Catalyst Data Store is provisioned |
| **Trigger** | User clicks "New FIR" on the Case Management dashboard |
| **Goal** | A new structured FIR record is created and saved; AI entity extraction is triggered |

**Main Flow:**
1. System presents the FIR entry form with fields: CrimeNo (auto-generated), date/time of occurrence, FIR date, DistrictRef, PoliceStationRef, CrimeHeadRef (searchable list), BriefFacts (text area), accused count, victim count
2. User fills in the required fields; user enters the BriefFacts narrative describing the incident
3. User submits the form
4. System validates required fields; validates CrimeNo format (district-year-station-sequence)
5. System saves the FIR record to `CaseMaster`
6. System triggers AI NER extraction on the BriefFacts text (asynchronous — inline task per ADR-011)
7. System shows a success banner: "FIR saved. AI extraction is running — results will appear in the Extraction tab."

**Alternative Flows:**
- A1 (Missing required fields): System highlights missing fields inline; does not save; shows field-level error messages
- A2 (Duplicate CrimeNo): System rejects the submission with a specific error message indicating the conflict
- A3 (AI extraction service unavailable): System saves the FIR successfully; shows a warning: "AI extraction is temporarily unavailable. You can trigger extraction manually from the Extraction tab."
- A4 (Network timeout on submit): System shows a retry option; if the FIR was already saved, the form shows the existing record

**Postconditions:**
- FIR exists in `CaseMaster` with status REGISTERED
- AI extraction is queued or running
- Audit event `FIR.CREATE` is recorded with user ID, case ID, timestamp, and district

**Audit Event Generated:** `FIR.CREATE`

**Test Cases:**
- T-002.1: Valid form → FIR saved → extraction triggered → success banner shown
- T-002.2: Missing required field → field-level error; no save
- T-002.3: AI service down → FIR saved; warning shown; manual trigger available
- T-002.4: SCRB_ANALYST attempts to create FIR → 403 returned from API

---

### UC-003 — Upload FIR Document for AI Extraction

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-003 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR |
| **Preconditions** | User is authenticated as INVESTIGATOR |
| **Trigger** | User clicks "Upload FIR Document" on the new FIR form or case detail page |
| **Goal** | An FIR document (PDF or image) is uploaded; AI extraction is triggered; extracted entities are presented for officer review |

**Main Flow:**
1. System displays a file upload area accepting: PDF (max 10 MB), JPEG / PNG image (max 5 MB)
2. User selects or drags a file
3. System validates file type (MIME check + extension check) and file size
4. System uploads the file to Catalyst Stratus; records the file hash (SHA-256)
5. System sends the document to the AI extraction pipeline (OCR if image; text extraction if PDF; then NER)
6. System shows a progress indicator: "Extracting entities from document..."
7. Extraction completes; system presents the Extraction Review page (see UC-004)

**Alternative Flows:**
- A1 (Unsupported file type): System shows a specific error: "File type not supported. Please upload a PDF or image file." File is not stored.
- A2 (File too large): System shows a specific error: "File exceeds the 10 MB limit." File is not stored.
- A3 (OCR / extraction failure): System shows a warning: "Document could not be automatically parsed. Please enter FIR data manually using the form." File is stored in quarantine for admin review.
- A4 (Stratus upload failure): System shows a generic error; does not proceed to extraction; logs the failure

**Postconditions:**
- File is stored in Catalyst Stratus with metadata record in `EvidenceMaster`
- AI extraction results are stored in the extraction queue
- Audit event `FIR.UPLOAD` is recorded with file hash and case ID

**Audit Event Generated:** `FIR.UPLOAD`

**Test Cases:**
- T-003.1: Valid PDF → upload success → extraction triggered → extraction review shown
- T-003.2: Invalid file type → type-specific error message; no upload
- T-003.3: File over size limit → size-specific error message; no upload
- T-003.4: OCR fails → warning shown; manual entry offered; file stored
- T-003.5: COMPLIANCE role attempts upload → 403 returned

---

### UC-004 — Review, Correct, and Approve AI Extraction

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-004 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR |
| **Preconditions** | AI extraction has completed for a case; user is authenticated as INVESTIGATOR with access to the case |
| **Trigger** | System navigates to Extraction Review page after UC-002 or UC-003; or user clicks the "Extraction" tab on an existing case |
| **Goal** | The officer reviews AI-suggested entity extraction results, makes corrections, and approves the extraction; the approved entities are stored and become queryable |

**Main Flow:**
1. System presents the Extraction Review page showing:
   - Extracted persons (each with name, suggested role — accused/victim/complainant — and confidence percentage)
   - Extracted vehicles (registration number, make/model if extracted)
   - Extracted locations (address, district, coordinates if geocoded)
   - Extracted legal sections (IPC / BNS sections mentioned in BriefFacts)
2. Each extracted entity shows a confidence indicator (colour-coded: green ≥ 80%, amber 60-79%, red < 60%)
3. User reviews each entity; user may:
   - Approve an entity as-is
   - Edit a field and then approve
   - Reject an entity (entity is not saved; rejection is logged)
   - Add an entity that AI missed (manual addition)
4. User clicks "Approve and Save All"
5. System saves the approved entities to the respective tables (Accused, Victim, ComplainantDetails, VehicleLink)
6. System triggers the entity resolution engine for newly added persons
7. System shows a success banner: "Extraction approved. Entity resolution is running."

**Alternative Flows:**
- A1 (No entities extracted): System shows: "AI did not extract any entities from this document. You may add entities manually using the form below." Officer can add manually.
- A2 (User rejects all entities): System asks for confirmation before clearing all suggestions. If confirmed, no entities are saved from this extraction; case remains in REGISTERED status.
- A3 (Entity resolution unavailable): System saves the approved entities; shows: "Entity resolution is temporarily unavailable. You can trigger it manually from the case detail page."
- A4 (Partial approval): System saves only the approved and edited entities; rejected entities are logged but not saved

**Postconditions:**
- Approved entities are saved to the database
- Each approval and rejection is recorded in `gov_AuditLog`
- Entity resolution is queued for newly saved persons
- FIR status changes from REGISTERED to EXTRACTION_APPROVED

**Audit Events Generated:** `AI.EXTRACTION.APPROVE` per entity (with confidence score); `AI.EXTRACTION.REJECT` per rejected entity

**Test Cases:**
- T-004.1: All entities approved as-is → all saved; entity resolution triggered
- T-004.2: Officer edits a name → corrected version saved; original suggestion logged
- T-004.3: One entity rejected → rejected entity not saved; rejection logged
- T-004.4: No entities extracted → manual add option shown
- T-004.5: AI confidence below 60% → entity shows red indicator; officer must explicitly approve

---

### UC-005 — Search for a Person, Vehicle, or Case

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-005 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (scoped to own district), SCRB_ANALYST (all districts) |
| **Preconditions** | User is authenticated; at least one FIR has been registered and extraction approved |
| **Trigger** | User enters a search query in the global search bar |
| **Goal** | The user finds a specific person, vehicle, or case quickly |

**Main Flow:**
1. User types a query in the search bar (minimum 3 characters)
2. System searches across: PersonEntity.CanonicalName, PersonEntity.aliases, VehicleLink.RegistrationNo, CaseMaster.CrimeNo
3. System applies jurisdiction scoping (INVESTIGATOR sees only own-district results; SCRB_ANALYST sees all)
4. System returns results grouped by type: Persons, Vehicles, Cases
5. User selects a result → system navigates to the entity detail view

**Alternative Flows:**
- A1 (No results): System shows: "No results found for '[query]'. Check spelling or broaden your search."
- A2 (Too many results — over 100): System shows top 100 with a filter prompt: "Refine by district, crime type, or date range to narrow results."
- A3 (Query includes special characters): System sanitises and searches; logs the query for audit if it contains suspicious patterns

**Postconditions:**
- User arrives at the selected entity detail view
- Audit event `PERSON.READ`, `VEHICLE.READ`, or `CASE.READ` is generated on navigation to the detail view

**Test Cases:**
- T-005.1: Exact name match → result shown; navigation to PersonEntity detail
- T-005.2: Partial name (phonetic variant) → PersonEntity aliases searched; result includes canonical name
- T-005.3: Vehicle registration → VehicleLink record returned
- T-005.4: INVESTIGATOR searches for a case from another district → result excluded from results
- T-005.5: Empty search → search is not submitted; no results shown

---

### UC-006 — View Case Detail and Investigation Timeline

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-006 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (own district), SCRB_ANALYST (all), COMPLIANCE (all) |
| **Preconditions** | At least one FIR has been registered |
| **Trigger** | User clicks a case from search results or case list |
| **Goal** | User sees the full case record including: FIR details, extracted entities, investigation notes, AI analysis, and case status |

**Main Flow:**
1. System loads the case detail view with tabs:
   - **Overview:** CrimeNo, date, station, crime type, BriefFacts text
   - **Entities:** List of accused, victims, complainants with links to PersonEntity profiles
   - **Extraction:** AI extraction result and officer approval status
   - **Graph:** Relationship graph (shortcut to UC-008)
   - **Risk:** Risk scores for accused persons (shortcut to UC-010)
   - **Notes:** [Not in MVP scope — UC-016 is Phase 2 / STRETCH]
2. User can navigate between tabs
3. User can click a PersonEntity to navigate to the person profile

**Alternative Flows:**
- A1 (Case not in user's district — INVESTIGATOR): 403 shown; case not loaded
- A2 (Case exists but extraction not yet complete): Extraction tab shows "AI extraction in progress"

**Postconditions:**
- Audit event `CASE.VIEW` recorded with case ID, user ID, timestamp
- If restricted fields (CasteRef, ReligionRef) are in the dataset and the user is not COMPLIANCE or ADMIN: those fields are not rendered in any tab

**Test Cases:**
- T-006.1: Case in own district → all tabs load correctly
- T-006.2: INVESTIGATOR tries to access case from another district → 403
- T-006.3: Restricted fields not visible to INVESTIGATOR or SCRB_ANALYST in any tab

---

### UC-007 — Review and Approve Entity Resolution Merge

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-007 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (own-district entities) |
| **Preconditions** | Entity resolution engine has produced merge candidates; user is authenticated as INVESTIGATOR |
| **Trigger** | System shows a notification or badge: "N entity merge suggestions pending review"; user clicks |
| **Goal** | Officer reviews a proposed person identity match, sees the supporting evidence and confidence score, and approves or rejects the merge |

**Main Flow:**
1. System shows the Entity Resolution Review queue
2. Each candidate shows:
   - PersonA: name, cases, station
   - PersonB: name, cases, station
   - Confidence score (e.g., 82%)
   - Evidence: shared phonetic token, similar date of birth, shared phone number suffix (if available)
   - Matching signals: name blocking match (Soundex), DOB similarity, address overlap
3. Officer clicks "View side-by-side" → sees a comparison card with all available fields for both persons
4. Officer clicks "Approve Merge" → PersonA and PersonB are unified under a single PersonEntity with all 4 cases linked
5. Officer clicks "Reject" → the candidate is dismissed; both persons remain separate; rejection is logged

**Alternative Flows:**
- A1 (Confidence below 60%): System marks the candidate as "Low confidence — high caution required" in red before officer makes a decision. No auto-rejection; human decision is still required.
- A2 (Officer is unsure — wants to defer): Officer can click "Skip for now." The candidate returns to the queue with a deferred flag. After 7 days unresolved it escalates to ADMIN.
- A3 (Person is from another district): If the merge candidate spans districts, it is routed to SCRB_ANALYST for approval (Phase 2 rule). In Phase 1, ADMIN approves cross-district merges.

**Postconditions:**
- Approved merge: PersonEntity updated; all linked cases visible under one entity; confidence score stored
- Rejected merge: Both persons remain separate; rejection logged with reason if provided
- Audit event `ENTITY.MERGE.APPROVE` or `ENTITY.MERGE.REJECT` recorded with candidate ID, confidence, and officer ID

**Test Cases:**
- T-007.1: High-confidence candidate (≥ 80%) → officer approves → PersonEntity updated; 4 cases linked
- T-007.2: Low-confidence candidate (< 60%) → red indicator shown; officer can still approve or reject
- T-007.3: Officer rejects → persons remain separate; rejection logged
- T-007.4: SCRB_ANALYST attempts to approve merge for INVESTIGATOR-scoped entity → 403
- T-007.5: Planted repeat offender test — 4 FIRs with name variations → entity resolution produces a merge candidate → acceptance test passes

---

### UC-008 — View Relationship Graph for a Person or Case

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-008 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (own district), SCRB_ANALYST (all) |
| **Preconditions** | At least one PersonEntity has been resolved; cases are loaded |
| **Trigger** | User clicks "Relationship Graph" on a PersonEntity profile or case detail page |
| **Goal** | User sees an interactive force-directed graph showing the selected entity's connections, with the ability to discover hidden links |

**Main Flow:**
1. System loads the graph for the selected entity (person or case)
2. Graph shows nodes: cases (blue squares), persons (orange circles), vehicles (grey diamonds), locations (green triangles)
3. Edges show relationships: accused-in, victim-in, co-accused-with, vehicle-linked-to, located-at
4. User can click any node to see its detail panel on the right
5. User can expand a node to load its second-degree connections
6. User can select two nodes and click "Find hidden link" → system runs shortest-path traversal (NetworkX BFS) → highlights the path in the graph

**Alternative Flows:**
- A1 (Graph too large — over 500 nodes): System shows the first 500 nodes with a filter prompt. User can filter by crime type, date range, or district to reduce graph size.
- A2 (No connections found): System shows: "No connections found for this entity beyond the direct case associations."
- A3 (Shortest path not found): System shows: "No path found between the selected entities within 5 hops."

**Postconditions:**
- User has seen the relationship network
- If "Find hidden link" was used: audit event `GRAPH.SHORTESTPATH.QUERY` recorded with node IDs and depth
- No data is modified

**Test Cases:**
- T-008.1: Person with 4 linked cases → graph shows 4 case nodes connected to person node
- T-008.2: "Find hidden link" between Case 001 and Case 042 → path via shared vehicle or person highlighted
- T-008.3: Graph expand → second-degree co-accused nodes load
- T-008.4: INVESTIGATOR selects a node from outside their district → node data is not returned

---

### UC-009 — View Geospatial Hotspot Map

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-009 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (own district), SCRB_ANALYST (all) |
| **Preconditions** | FIRs with DistrictRef and station data are loaded |
| **Trigger** | User navigates to the Hotspot Map tab |
| **Goal** | User sees a heatmap of crime density over Karnataka (or own district), drills down to station level, and identifies emerging patterns |

**Main Flow:**
1. System loads a MapLibre GL map centred on Karnataka
2. Heatmap overlay shows crime density by district (aggregated from case locations)
3. User can apply filters: crime type (searchable dropdown), date range (last 7 / 30 / 90 days), crime head
4. SCRB_ANALYST sees all districts; INVESTIGATOR sees only own district
5. User clicks a district → map zooms in; station-level breakdown loads
6. User clicks a station → list of cases for that station in the selected time period appears in a side panel
7. Anomaly badges appear on districts with active anomaly alerts (red badge with count)

**Alternative Flows:**
- A1 (No cases in selected filters): Map shows empty heatmap; side panel shows "No cases match the selected filters."
- A2 (Map tiles unavailable): System shows the district list as a table fallback with case counts

**Postconditions:**
- No data is modified
- No audit event required for map view (browsing-level action)

**Test Cases:**
- T-009.1: SCRB_ANALYST view → all districts shown on map; heatmap reflects case counts
- T-009.2: INVESTIGATOR view → only own district shown
- T-009.3: District with planted anomaly spike → red badge visible; drill-down shows elevated case count
- T-009.4: Filter by crime type → heatmap updates to show only cases of that type

---

### UC-010 — View Explainable Risk Score

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-010 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (own district), SCRB_ANALYST (all) |
| **Preconditions** | At least one PersonEntity has been resolved; risk scoring model has run |
| **Trigger** | User clicks "Risk Score" on a PersonEntity profile or case accused list |
| **Goal** | User sees the risk score for a person, with a feature-importance breakdown, confirming the score is based only on case history features — not protected characteristics |

**Main Flow:**
1. System displays the risk score panel for the selected PersonEntity:
   - Score: numeric (e.g., 85%) with a label (Low / Medium / High based on thresholds)
   - Score explanation: "This score reflects the likelihood of future case involvement based on historical patterns."
   - Feature importance bar chart: top 5 features contributing to the score with their weights
   - Features include: PriorCaseCount, DaysSinceLastCase, CrimeTypeCount (diversity), AverageSeverityScore
   - A "Fairness verified" badge confirms CasteID and ReligionID are not in the feature set
2. User can click "View model details" → links to the fairness check result for the most recent model run

**Alternative Flows:**
- A1 (Score not yet computed): System shows: "Risk score is being computed. Check back in a few minutes." with a "Recalculate" button for SCRB_ANALYST and ADMIN.
- A2 (Person has no prior cases): System shows: "Insufficient case history to compute a risk score. This person has 0 prior cases."
- A3 (Fairness check failed): System shows a warning banner: "⚠ Fairness check failed. This score has been flagged for review. Contact the Compliance Officer before acting on this score." No score value is displayed.

**Postconditions:**
- Audit event `RISK.VIEW` recorded with: user ID, entity ID, score value, feature importance (top 5 features and weights)
- No data is modified

**Test Cases:**
- T-010.1: Person with 5 prior cases → score computed; feature importance shows PriorCaseCount as top feature
- T-010.2: CasteID and ReligionID are absent from feature importance → "Fairness verified" badge shows
- T-010.3: Fairness check failed → warning banner shown; score value not displayed
- T-010.4: INVESTIGATOR views score for a person from another district → 403

---

### UC-011 — Detect and View Anomaly Alerts

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-011 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (own district), SCRB_ANALYST (all) |
| **Preconditions** | Anomaly detection has run; a spike above baseline has been detected |
| **Trigger** | User sees an anomaly badge on the hotspot map or dashboard; user clicks the badge |
| **Goal** | User understands that a crime rate spike has been detected, sees its severity, and can drill down to the contributing cases |

**Main Flow:**
1. System displays an anomaly alert card:
   - District and station
   - Crime type
   - Z-score (deviation from historical baseline)
   - Alert severity: LOW (z > 2.0), MEDIUM (z > 3.0), HIGH (z > 4.0)
   - Alert message: "Bengaluru Urban — Theft: z-score 4.2 this week — 5× the historical average"
2. User clicks "View contributing cases" → filtered case list for that district, crime type, and week
3. User can dismiss the alert after reviewing (dismissed alerts remain in the alert history)

**Alternative Flows:**
- A1 (No active anomalies): Anomaly section shows: "No anomalies detected in the current period."
- A2 (Alert acknowledged but spike continues): Alert reappears on the next detection run if spike persists

**Postconditions:**
- No data is modified
- If user dismisses the alert, a dismissal event is logged

**Test Cases:**
- T-011.1: Planted spike (3× normal rate for a week) → anomaly detected; z-score > 3.0; alert shown
- T-011.2: Alert drill-down → contributing cases match the planted spike cases
- T-011.3: INVESTIGATOR sees only own-district alerts; SCRB_ANALYST sees all-district alerts

---

### UC-012 — Ask Berunda (Natural Language Query)

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-012 |
| **Priority** | ✅ MVP |
| **Actors** | INVESTIGATOR (own-district scope), SCRB_ANALYST (all) |
| **Preconditions** | FIRs are loaded; RAG corpus has been built |
| **Trigger** | User types a question in the "Ask Berunda" chat interface |
| **Goal** | User receives a grounded, cited answer to an investigative question |

**Main Flow:**
1. User types a plain-English question, e.g. "What is the connection between FIR-001 and FIR-042?"
2. System sends the question to the RAG pipeline:
   a. Query is embedded
   b. Top-K relevant case chunks are retrieved from the corpus (scoped to user's access)
   c. Retrieved chunks are injected into the LLM prompt as grounding context
   d. LLM generates an answer grounded in the retrieved chunks
3. System displays the answer with:
   - The answer text
   - Source citations: case numbers from which the answer is grounded
   - Confidence indicator if the LLM expresses uncertainty
4. System appends a disclaimer: "This is an AI-generated summary. Verify against case records before taking action."

**Alternative Flows:**
- A1 (LLM API unavailable): System shows: "Ask Berunda is temporarily unavailable. Please search for the cases manually."
- A2 (Query not grounded in any retrieved document): System shows: "I could not find relevant case records to answer this question. Try rephrasing or searching directly."
- A3 (Query asks for protected-characteristic information): System responds: "I cannot provide information on caste, religion, or other protected characteristics. Access to this data requires a Compliance role."
- A4 (Query scope violates jurisdiction): Retrieved documents are pre-filtered to user's district; no out-of-scope documents are returned

**Postconditions:**
- Audit event `RAG.QUERY` recorded with: user ID, question text (not the answer), case IDs retrieved, timestamp
- No data is modified

**Test Cases:**
- T-012.1: "What is the connection between FIR-001 and FIR-042?" → answer cites both FIR IDs and explains the shared entity
- T-012.2: "What cases involve vehicle KA-01-AB-9999?" → answer cites all cases containing the vehicle registration
- T-012.3: "What is Venkatesh Kumar's caste?" → system returns the protected-characteristic refusal message
- T-012.4: LLM unavailable → graceful error message; no unhandled exception
- T-012.5: INVESTIGATOR question scoped to only own-district FIRs — confirmed by checking retrieved chunk case IDs

---

### UC-013 — View Fairness Verification Dashboard

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-013 |
| **Priority** | ✅ MVP |
| **Actors** | COMPLIANCE (full), SCRB_ANALYST (read-only) |
| **Preconditions** | At least one fairness check has completed |
| **Trigger** | User navigates to the Fairness Dashboard |
| **Goal** | Compliance officer can confirm that all predictive models exclude CasteID and ReligionID, with programmatic evidence |

**Main Flow:**
1. System displays the fairness dashboard:
   - Last fairness check run: timestamp
   - Overall status: PASS or FAIL
   - Per-model status table: model name | features checked | CasteID in features? | ReligionID in features? | Status
   - Feature importance table for the risk scoring model (top 10 features and weights)
2. User clicks "View evidence" for a model → system shows the full feature list for the last model run
3. If status is PASS: green banner — "All models pass the protected-characteristic exclusion check."
4. If status is FAIL: red banner — "FAIL. One or more models include a protected characteristic. Immediate review required."

**Alternative Flows:**
- A1 (No fairness check has run): System shows: "No fairness check results available. Ask the Admin to trigger a check."
- A2 (FAIL status): COMPLIANCE role sees a "Create incident" button → escalates to ADMIN via an incident record

**Postconditions:**
- Audit event `FAIRNESS.DASHBOARD.VIEW` recorded

**Test Cases:**
- T-013.1: All models pass → PASS banner; feature importance shows no CasteID or ReligionID
- T-013.2: Hypothetical FAIL scenario (seeded for test) → FAIL banner; affected model shown
- T-013.3: INVESTIGATOR navigates to fairness dashboard → 403

---

### UC-014 — Review Audit Log

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-014 |
| **Priority** | ✅ MVP |
| **Actors** | COMPLIANCE (all entries), ADMIN (all entries), INVESTIGATOR / SCRB_ANALYST (own entries only) |
| **Preconditions** | At least one audit event has been recorded |
| **Trigger** | User navigates to the Audit Log view |
| **Goal** | User can search, filter, and view audit entries to understand who accessed what, when, and what AI outputs were generated |

**Main Flow:**
1. System displays the audit log with columns: Timestamp, User ID, Action, Resource ID, Resource Type, District, Details
2. User can filter by: date range, user ID, action type, resource type
3. User applies a filter: officer ID "ANANYA", date "today" → sees all actions taken by Ananya today
4. Each entry shows the action detail (e.g., "Approved entity resolution merge for PersonEntity-042 with confidence 82%")
5. COMPLIANCE and ADMIN see all entries. INVESTIGATOR and SCRB_ANALYST see only their own entries (enforced at query level)

**Alternative Flows:**
- A1 (No entries match filter): System shows: "No audit events match the selected filters."
- A2 (Attempt to delete an audit entry): All delete buttons are absent from the UI; API returns 405 if attempted

**Postconditions:**
- No data is modified
- Viewing the audit log does not itself generate another audit event (to avoid infinite recursion)

**Test Cases:**
- T-014.1: COMPLIANCE views full audit log → all users' entries visible
- T-014.2: INVESTIGATOR views audit log → only own entries visible; filter for other users returns empty
- T-014.3: Filter by action type "AI.EXTRACTION.APPROVE" → shows only extraction approval events
- T-014.4: API DELETE on audit log entry → 405 returned regardless of role

---

### UC-015 — Manage Users and Roles (Admin)

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-015 |
| **Priority** | ✅ MVP |
| **Actors** | ADMIN |
| **Preconditions** | User is authenticated as ADMIN |
| **Trigger** | ADMIN navigates to the User Management panel |
| **Goal** | ADMIN can create demo users, assign correct roles, and unlock accounts |

**Main Flow:**
1. System displays the user list with: username, display name, role, district, station, status (active/locked)
2. ADMIN clicks "New User" → fills in: username, display name, initial password (or sends invite), role, district, assigned stations
3. ADMIN submits → user is created; audit event `ADMIN.USER.CREATE` recorded
4. ADMIN can change a user's role: select user → change role dropdown → save → audit event `ADMIN.ROLE.CHANGE` recorded
5. ADMIN can unlock a locked account: select user → click "Unlock" → account unlocks

**Postconditions:**
- User is created or updated
- Audit event recorded for every change

**Test Cases:**
- T-015.1: Create demo users (Ananya, Ramesh, Priya, Krishnamurthy) with correct roles and districts → all can log in
- T-015.2: Change a user's role → old sessions with old role are invalidated (or JWT expiry forces re-login)
- T-015.3: INVESTIGATOR attempts to access admin panel → 403

---

### UC-016 — Add Investigation Notes (STRETCH)

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-016 |
| **Priority** | 🧩 STRETCH |
| **Actors** | INVESTIGATOR (assigned cases) |
| **Goal** | INVESTIGATOR adds timestamped, signed investigation notes to a case |
| **Note** | Not required for demo; implement if entity resolution and UI are complete before Day 8 |

---

### UC-017 — Link Evidence Metadata (STRETCH)

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-017 |
| **Priority** | 🧩 STRETCH |
| **Actors** | INVESTIGATOR (assigned cases) |
| **Goal** | INVESTIGATOR links a file hash or evidence reference to a case record for chain-of-custody tracking |
| **Note** | Not required for demo; implement if time permits |

---

### UC-018 — Generate Statutory Report (STRETCH)

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-018 |
| **Priority** | 🧩 STRETCH |
| **Actors** | SCRB_ANALYST, COMPLIANCE |
| **Goal** | Generate a downloadable PDF/CSV aggregate crime report by district, crime head, and time period; restricted-field data appears only in aggregate counts |
| **Note** | Not required for demo; implement if time permits |

---

### UC-019 — Kannada NER Extraction (VISION)

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-019 |
| **Priority** | 🔭 VISION |
| **Goal** | Extract entities from FIR narratives written in Kannada using AI4Bharat NLP models |
| **Target Phase** | Phase 2 |

---

### UC-020 — Real CCTNS Data Bridge (VISION)

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-020 |
| **Priority** | 🔭 VISION |
| **Goal** | Establish a secure, MOU-approved data pipeline from CCTNS to Berunda for real case records |
| **Target Phase** | Phase 2 |

---

## 4. Use Case to Feature Mapping

| UC-ID | SRS FR Reference | PRD Feature | Demo Day |
|-------|-----------------|-------------|---------|
| UC-001 | FR-001 | F-009 Auth + RBAC | Day 3 |
| UC-002 | FR-002 | F-001 Synthetic FIR import + manual entry | Day 2 |
| UC-003 | FR-003 | F-001 FIR import | Day 2 |
| UC-004 | FR-004 | F-002 English NER entity extraction | Day 3 |
| UC-005 | FR-005 | F-003 Cross-case PersonEntity resolution | Day 4 |
| UC-006 | FR-006 | F-001 (case detail) | Day 3 |
| UC-007 | FR-007 | F-003 Entity resolution | Day 4-5 |
| UC-008 | FR-008 | F-004 Relationship graph + hidden-link UI | Day 5 |
| UC-009 | FR-009 | F-005 Geospatial hotspot map | Day 4 |
| UC-010 | FR-010 | F-006 Explainable risk scoring | Day 5-6 |
| UC-011 | FR-011 | F-007 Anomaly/spike detection | Day 5 |
| UC-012 | FR-012 | F-008 Ask Berunda RAG | Day 6 |
| UC-013 | FR-013 | F-011 Live fairness check | Day 6-7 |
| UC-014 | FR-014 | F-010 Audit logging | Day 3 |
| UC-015 | FR-015 | F-009 Auth + RBAC | Day 3 |
| UC-016 | FR-016 | STRETCH | Day 8+ |
| UC-017 | FR-017 | STRETCH | Day 8+ |
| UC-018 | FR-018 | STRETCH | Day 9+ |

---

## 5. Use Case to Persona Mapping

| UC-ID | PERSONA-001 Ananya (IO) | PERSONA-002 Ramesh (SHO) | PERSONA-003 Priya (Analyst) | PERSONA-004 Krishnamurthy (Compliance) | PERSONA-005 Admin |
|-------|:---:|:---:|:---:|:---:|:---:|
| UC-001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| UC-002 | ✅ | ✅ | ❌ | ❌ | ✅ |
| UC-003 | ✅ | ✅ | ❌ | ❌ | ✅ |
| UC-004 | ✅ | ✅ | ❌ | ❌ | ✅ |
| UC-005 | ✅ | ✅ | ✅ | ✅ | ✅ |
| UC-006 | ✅ | ✅ | ✅ | ✅ | ✅ |
| UC-007 | ✅ | ✅ | ❌ | ❌ | ✅ |
| UC-008 | ✅ | ✅ | ✅ | ❌ | ✅ |
| UC-009 | ✅ (own district) | ✅ (own district) | ✅ (all) | ❌ | ✅ |
| UC-010 | ✅ | ✅ | ✅ | ❌ | ✅ |
| UC-011 | ✅ | ✅ | ✅ | ❌ | ✅ |
| UC-012 | ✅ | ✅ | ✅ | ✅ | ✅ |
| UC-013 | ❌ | ❌ | ✅ (read-only) | ✅ (full) | ✅ |
| UC-014 | ✅ (own) | ✅ (own) | ✅ (own) | ✅ (all) | ✅ (all) |
| UC-015 | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 6. Happy Path Test Matrix for Demo

The following test cases must pass before the demo rehearsal on Day 10.

| Test ID | Use Cases Covered | Scenario | Expected Result |
|---------|------------------|---------|----------------|
| DEMO-T01 | UC-001 | Login as Ananya (INVESTIGATOR) | Investigator dashboard loads with Electronic City Division scope |
| DEMO-T02 | UC-003, UC-004 | Upload synthetic FIR document | AI extraction completes; persons, vehicles, sections shown |
| DEMO-T03 | UC-004 | Approve AI extraction | Entities saved; entity resolution triggered |
| DEMO-T04 | UC-007 | Review entity resolution for planted repeat offender | Merge candidate shown with ≥ 80% confidence; approval links 4 cases |
| DEMO-T05 | UC-008 | View relationship graph for linked PersonEntity | Graph shows 4 case nodes, co-accused, and linked vehicle |
| DEMO-T06 | UC-008 | Find hidden link between Case 001 and Case 042 | Path highlighted through shared vehicle or person |
| DEMO-T07 | UC-009 | View hotspot map as SCRB_ANALYST | Karnataka heatmap renders; anomaly badge visible on planted district |
| DEMO-T08 | UC-011 | View anomaly alert | Z-score > 4.0 for Bengaluru Urban theft shown; drill-down matches planted cases |
| DEMO-T09 | UC-010 | View risk score for high-risk accused person | Score shown with feature importance; "Fairness verified" badge present |
| DEMO-T10 | UC-012 | Ask Berunda: "What is the connection between FIR-001 and FIR-042?" | Grounded answer with both case IDs cited; disclaimer shown |
| DEMO-T11 | UC-012 | Ask Berunda: "What cases involve vehicle KA-01-AB-9999?" | All planted vehicle cases cited in answer |
| DEMO-T12 | UC-012 | Ask Berunda: "What is Venkatesh's caste?" | Refusal message returned; no restricted data revealed |
| DEMO-T13 | UC-013 | Open fairness dashboard as Compliance role | PASS status; no CasteID or ReligionID in feature importance |
| DEMO-T14 | UC-014 | View audit log as Compliance role filtering by Ananya's actions today | All of Ananya's actions from DEMO-T01 through DEMO-T12 appear |
| DEMO-T15 | UC-001 | Login as INVESTIGATOR; try to access fairness dashboard | 403 returned; access denied message shown |

---

*End of 03-USER-JOURNEYS-AND-USE-CASES.md*
