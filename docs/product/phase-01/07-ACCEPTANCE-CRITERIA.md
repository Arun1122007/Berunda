# 07 — Acceptance Criteria

**Document ID:** BERUNDA-PH1-AC-001
**Version:** 1.0 | **Status:** APPROVED — Authoritative Phase 1 acceptance criteria
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> Acceptance criteria are written in Given/When/Then format.
> Every P0 feature has at least one positive, one negative, one authorization, and one failure scenario.
> All criteria must pass before the MVP definition of done is satisfied.

---

## AC-AUTH-001 — Valid Login

```
Given an active user account with role INVESTIGATOR
When the user submits the correct username and password to POST /auth/login
Then the system returns HTTP 200
And the response body contains a signed JWT access token
And the JWT payload contains role: "INVESTIGATOR", user_id, district, and expiry
And the system writes an AUTH.LOGIN audit event with the user's ID, IP address, and timestamp
And the user is redirected to the Investigator case-management dashboard showing only own-district cases
```

---

## AC-AUTH-002 — Invalid Credentials

```
Given an active user account
When the user submits an incorrect password to POST /auth/login
Then the system returns HTTP 401
And the response message is "Invalid credentials" — it does not reveal whether the username or password is incorrect
And no JWT is issued
And an AUTH.LOGIN_FAILURE audit event is written
```

---

## AC-AUTH-003 — Account Lockout

```
Given an active user account
When the user submits 5 consecutive failed login attempts within 15 minutes
Then the system locks the account
And the 6th attempt returns HTTP 403 with message "Account temporarily locked"
And an AUTH.LOGIN_FAILURE audit event is written for each attempt
And the ADMIN role can unlock the account via the user management panel
```

---

## AC-AUTH-004 — Expired JWT Rejection

```
Given an authenticated user session whose access token has expired
When the user makes an API request with the expired token
Then the system returns HTTP 401
And the response message is "Token expired — please refresh your session"
And no data is returned
```

---

## AC-AUTH-005 — Role Access Control — Authorized

```
Given an authenticated user with role SCRB_ANALYST
When the user requests GET /analytics/hotspot with a valid JWT
Then the system returns HTTP 200 with hotspot data for all districts
```

---

## AC-AUTH-006 — Role Access Control — Unauthorized (403)

```
Given an authenticated user with role INVESTIGATOR
When the user requests GET /compliance/fairness-dashboard
Then the system returns HTTP 403 with message "Access denied: insufficient role"
And an AUTH.ACCESS_DENIED audit event is written
```

---

## AC-AUTH-007 — Jurisdiction Scoping Enforcement

```
Given an authenticated INVESTIGATOR user assigned to Bengaluru Urban District stations
When the user requests GET /cases returning a list of all cases
Then the system returns only cases where PoliceStationRef is in the user's assigned stations
And cases from other districts are not present in the response
And the filtering is applied at the database query level, not after retrieval
```

---

## AC-AUTH-008 — Protected-Characteristic Field Exclusion (INVESTIGATOR)

```
Given an authenticated user with role INVESTIGATOR
When the user requests GET /persons/{id} for an Accused record that has CasteRef and ReligionRef values
Then the response body does not contain a CasteRef field
And the response body does not contain a ReligionRef field
And no HTTP error is returned — the person record is returned without those fields
```

---

## AC-AUTH-009 — Protected-Characteristic Field — COMPLIANCE Role (Aggregate)

```
Given an authenticated user with role COMPLIANCE
When the user requests GET /reports/protected-field-aggregate for a district
Then the system returns aggregate counts (e.g., {"CasteRef": {"SC": 12, "OBC": 34}}) for the district
And individual-level records are not returned
And a RESTRICTED.FIELD.ACCESS audit event is written with the user's ID and the district queried
```

---

## AC-FIR-001 — Create FIR with All Required Fields

```
Given an authenticated INVESTIGATOR user assigned to Electronic City Division
When the user submits POST /fir with all required fields:
  OccurrenceDate (past), FIRDate (today), DistrictRef (valid FK),
  PoliceStationRef (valid FK in user's stations), CrimeHeadRef (valid FK),
  BriefFacts ("Suspect was seen breaking into the shop at MG Road at 02:00 on 20 July 2026")
Then the system returns HTTP 201
And the response body contains the new CaseID and an auto-generated CrimeNo
And the CrimeNo follows the format DistrictCode/StationCode/Year/Sequence
And the FIR record is saved to CaseMaster with status REGISTERED
And an AI extraction job is queued for the BriefFacts text
And an FIR.CREATE audit event is written with the case ID, user ID, district, and timestamp
```

---

## AC-FIR-002 — Create FIR with Missing Required Field

```
Given an authenticated INVESTIGATOR user
When the user submits POST /fir with BriefFacts omitted
Then the system returns HTTP 422
And the response body identifies BriefFacts as a missing required field
And no FIR record is saved
And no audit event is written
```

---

## AC-FIR-003 — Create FIR — Cross-Station Access Denied

```
Given an authenticated INVESTIGATOR user assigned to Electronic City Division
When the user submits POST /fir with a PoliceStationRef from Mysuru District
Then the system returns HTTP 403 with "You are not authorized to create FIRs for this station"
And no FIR record is saved
```

---

## AC-FIR-004 — Create FIR — Non-INVESTIGATOR Role Denied

```
Given an authenticated user with role SCRB_ANALYST
When the user submits POST /fir with valid fields
Then the system returns HTTP 403
And no FIR record is saved
```

---

## AC-FIR-005 — Upload FIR Document — Valid PDF

```
Given an authenticated INVESTIGATOR user with an active case in their jurisdiction
When the user uploads a PDF file (under 10 MB, MIME type application/pdf) to POST /fir/{id}/upload
Then the system returns HTTP 200 with the evidence record ID
And the file is stored in Catalyst Stratus
And the SHA-256 hash of the file is stored in EvidenceMaster
And the AI extraction pipeline is triggered for the uploaded file
And an FIR.UPLOAD audit event is written with the case ID, file hash, and user ID
```

---

## AC-FIR-006 — Upload FIR Document — Invalid File Type

```
Given an authenticated INVESTIGATOR user
When the user uploads a .docx file to POST /fir/{id}/upload
Then the system returns HTTP 415 with "Unsupported file type. Accepted types: PDF, JPEG, PNG"
And the file is not stored
And no extraction is triggered
```

---

## AC-FIR-007 — Upload FIR Document — File Too Large

```
Given an authenticated INVESTIGATOR user
When the user uploads a PDF file of 15 MB to POST /fir/{id}/upload
Then the system returns HTTP 413 with "File exceeds the 10 MB limit for PDFs"
And the file is not stored
```

---

## AC-FIR-008 — AI Extraction Failure — Original Text Preserved

```
Given an authenticated INVESTIGATOR user who has created an FIR with BriefFacts text
When the AI extraction service is unavailable during extraction processing
Then the system sets extraction_status to FAILED
And the original BriefFacts text is preserved unchanged in CaseMaster
And the system presents the officer with a notification: "AI extraction failed. Enter entities manually."
And the FIR record is still accessible and can be retrieved
```

---

## AC-AI-001 — NER Extraction Result Displayed as Suggestion

```
Given an FIR with BriefFacts: "Accused Venkatesh Kumar (age 28) drove vehicle KA-01-AB-9999 to the shop at MG Road"
When AI extraction completes
Then the extraction review page shows:
  - Person suggestion: "Venkatesh Kumar" — role: accused — confidence shown
  - Vehicle suggestion: "KA-01-AB-9999" — confidence shown
  - Location suggestion: "MG Road" — confidence shown
And none of these appear yet in the Accused, VehicleLink, or OccurrencePlace tables
And each suggestion shows the "AI suggestion — review required" label
```

---

## AC-AI-002 — Officer Approves AI Extraction

```
Given an extraction review page showing 3 suggestions (person, vehicle, location)
When the officer clicks "Approve" on all 3 suggestions and then "Save All"
Then the system creates records in the Accused, VehicleLink, and OccurrencePlace tables
And an AI.EXTRACTION.APPROVE audit event is written for each approved entity
And the FIR status changes to EXTRACTION_APPROVED
And the entity resolution pipeline is triggered for the newly approved person
```

---

## AC-AI-003 — Officer Edits AI Extraction Before Approving

```
Given an extraction review page showing a person suggestion: "Venkatesh Kumaar" (misspelling)
When the officer edits the name to "Venkatesh Kumar" and clicks Approve
Then the Accused record is created with name "Venkatesh Kumar"
And an AI.EXTRACTION.EDIT audit event is written recording both the original suggestion and the corrected value
And an AI.EXTRACTION.APPROVE audit event is written with the corrected value
```

---

## AC-AI-004 — Officer Rejects AI Extraction

```
Given an extraction review page with a low-confidence person suggestion
When the officer clicks "Reject" on that suggestion
Then no record is created for the rejected entity
And an AI.EXTRACTION.REJECT audit event is written with the rejected entity text
And the remaining approved entities are saved normally
```

---

## AC-AI-005 — Entity Resolution — Repeat Offender Linked (Acceptance Test)

```
Given 4 FIR records loaded with the following name variants for the same individual:
  FIR-001: Accused "Venkatesh Kumar"
  FIR-002: Accused "Venkatesh Kumaar"
  FIR-003: Accused "V. Kumar"
  FIR-004: Accused "Venkatesha Kumar"
And all 4 persons have been approved through extraction review
When the entity resolution pipeline runs
Then at least 3 merge candidates are generated
And at least one candidate has a confidence score ≥ 0.70
And the confidence score is based on phonetic name blocking and feature weighting, not on CasteRef or ReligionRef
```

---

## AC-AI-006 — Entity Merge Approval Links All Cases

```
Given a merge candidate showing PersonA (FIR-001) and PersonB (FIR-002) with confidence 82%
When the officer reviews the side-by-side comparison and clicks "Approve Merge"
Then PersonA is designated as the canonical PersonEntity
And PersonB is moved to merged state
And both FIR-001 and FIR-002 appear in PersonA's linked cases list
And an ENTITY.MERGE.APPROVE audit event is written with PersonA ID, PersonB ID, and confidence score
```

---

## AC-AI-007 — Entity Merge Rejection Preserves Both Persons

```
Given a merge candidate showing PersonA and PersonB with confidence 55%
When the officer clicks "Reject"
Then PersonA and PersonB remain as separate records
And neither person is modified
And an ENTITY.MERGE.REJECT audit event is written
```

---

## AC-AI-008 — Entity Resolution — Cross-District Access Control

```
Given an INVESTIGATOR user in District A
When the entity resolution merge review queue loads
Then merge candidates involving only persons from District B are not shown to this user
And only candidates involving at least one person from the user's assigned stations are shown
```

---

## AC-GRAPH-001 — Relationship Graph Renders for Linked PersonEntity

```
Given a PersonEntity linked to 4 FIR cases, 2 co-accused persons, and 1 vehicle
When the user clicks "Relationship Graph" on the PersonEntity profile
Then the graph renders with:
  - 1 orange circle node for the PersonEntity
  - 4 blue square nodes for the linked cases
  - 2 orange circle nodes for co-accused persons
  - 1 grey diamond node for the linked vehicle
And edges are labelled with relationship types (accused-in, co-accused-with, vehicle-linked-to)
```

---

## AC-GRAPH-002 — Hidden-Link Discovery (Demo Acceptance Test)

```
Given Case 001 and Case 042 are connected through shared vehicle KA-01-AB-9999
  (Case 001 → accused-drove → vehicle KA-01-AB-9999 → vehicle-linked-to → Case 042)
When the user selects the Case 001 node and the Case 042 node in the graph
And clicks "Find hidden link"
Then the system returns the path:
  Case 001 → [accused-drove] → Vehicle KA-01-AB-9999 → [vehicle-linked-to] → Case 042
And the path is highlighted in the graph
And a GRAPH.SHORTESTPATH.QUERY audit event is written with both node IDs and path length
```

---

## AC-GRAPH-003 — No Path Found

```
Given two case nodes with no graph connection within 5 hops
When the user requests "Find hidden link" between them
Then the system returns "No path found within 5 hops"
And no path is highlighted
And the existing graph is unchanged
```

---

## AC-MAP-001 — Hotspot Map Renders with Anomaly Badge

```
Given 5000 synthetic FIR records loaded with a planted 5× spike in theft cases in Bengaluru Urban district for week 30
When the SCRB_ANALYST user opens the hotspot map
Then the Karnataka heatmap renders with district-level density overlay
And Bengaluru Urban district shows a HIGH severity anomaly badge (z-score > 4.0)
And other districts with normal case rates show no anomaly badge
```

---

## AC-MAP-002 — District Drill-Down

```
Given the hotspot map is displaying Bengaluru Urban with an anomaly badge
When the user clicks on Bengaluru Urban district
Then the map zooms to Bengaluru Urban
And a side panel lists police stations in Bengaluru Urban with their case counts
And Electronic City Division shows a case count consistent with the planted spike
```

---

## AC-MAP-003 — Crime Type Filter

```
Given the hotspot map is showing all crime types
When the user selects "Theft" from the crime head dropdown filter
Then the heatmap density updates to reflect only theft cases
And other crime type cases are excluded from the density calculation
And the anomaly badge for Bengaluru Urban remains visible (as the spike is in theft)
```

---

## AC-MAP-004 — INVESTIGATOR Sees Only Own District

```
Given an INVESTIGATOR user assigned to Electronic City Division, Bengaluru Urban District
When the user opens the hotspot map
Then the map shows only the Bengaluru Urban district view
And other Karnataka districts are not shown or are grayed out
```

---

## AC-RISK-001 — Risk Score Displayed with Feature Importance

```
Given a PersonEntity with 5 linked cases as accused, most recent case 10 days ago, 3 distinct crime types
When the INVESTIGATOR views the risk score panel for this person
Then the system displays a risk score value (0.0 – 1.0) with a severity label
And a bar chart shows the top 5 contributing features with their weights
And the feature labels are in plain English: "Number of prior cases", "Days since last case", etc.
And a "Fairness verified" badge is visible
And CasteRef and ReligionRef do not appear anywhere in the feature list or labels
```

---

## AC-RISK-002 — Risk Score Not Shown for Person with No Prior Cases

```
Given a PersonEntity with 0 or 1 prior linked cases
When the user views the risk score panel
Then the system displays "Insufficient case history to compute a risk score"
And no score value is shown
```

---

## AC-RISK-003 — Fairness Check Failure Blocks Score Display

```
Given a fairness check result for the current model run is FAIL
When any user attempts to view a risk score
Then the system displays a warning banner: "⚠ Fairness check failed. This score has been flagged for review. Contact the Compliance Officer before acting on this score."
And no score value is displayed to any role except ADMIN
```

---

## AC-RAG-001 — Ask Berunda Answers with Citations

```
Given the RAG corpus contains FIR records including FIR-001 and FIR-042 which share vehicle KA-01-AB-9999
When the user asks: "What is the connection between FIR-001 and FIR-042?"
Then the system returns an answer that references both FIR CrimeNos
And the answer explains the shared vehicle as the connection
And the citations section lists both FIR CrimeNos as source documents
And the answer includes the disclaimer "This is an AI-generated summary. Verify against case records before taking action."
And a RAG.QUERY audit event is written with the question text and retrieved case IDs
```

---

## AC-RAG-002 — Ask Berunda — Vehicle Query

```
Given FIR records involving vehicle KA-01-AB-9999 in 5 cases
When the user asks: "What cases involve vehicle KA-01-AB-9999?"
Then the system returns an answer listing the 5 FIR CrimeNos
And the citations section lists all 5 FIR CrimeNos
```

---

## AC-RAG-003 — Ask Berunda — Protected-Characteristic Query Refused

```
Given any authenticated user
When the user asks: "What is Venkatesh Kumar's caste?"
Then the system returns: "I cannot provide information on caste, religion, or other protected characteristics. Access to this data requires a Compliance role."
And no caste or religion data is returned in the response
And a RAG.QUERY audit event is written noting the protected-characteristic refusal
```

---

## AC-RAG-004 — Ask Berunda — Jurisdiction Scoping

```
Given an INVESTIGATOR user in District A
When the user asks a question about a case that exists only in District B
Then the system either returns "I could not find relevant case records to answer this question"
Or returns an answer grounded only in cases from District A
And no District B case IDs appear in the citations
```

---

## AC-RAG-005 — Ask Berunda — MockProvider Fallback

```
Given the LLM API key is invalid or the provider is unreachable
When the user submits any question to Ask Berunda
Then the system activates the MockProvider within 5 seconds
And a banner displays "AI assistant is in limited mode — contact admin if this persists"
And a structurally valid mock response is returned
And no unhandled error or crash occurs
```

---

## AC-FAIR-001 — Fairness Dashboard — PASS Status

```
Given the fairness check has run and CasteRef and ReligionRef are absent from all model feature lists
When the COMPLIANCE user opens the Fairness Dashboard
Then the dashboard displays overall status: PASS with a green indicator
And the per-model table shows each model with CasteID_in_features: false and ReligionID_in_features: false
And the feature importance table for the risk score model shows the top features with no mention of CasteRef or ReligionRef
```

---

## AC-FAIR-002 — Fairness Dashboard — INVESTIGATOR Denied

```
Given an authenticated user with role INVESTIGATOR
When the user navigates to /compliance/fairness-dashboard
Then the system returns HTTP 403
And the dashboard is not rendered
```

---

## AC-FAIR-003 — Fairness Check Blocks Scoring on FAIL

```
Given CasteRef has been injected into the model feature list (test scenario only)
When the fairness verification check runs before batch scoring
Then the check returns status FAIL
And batch scoring is halted
And a FAIRNESS.CHECK.RUN audit event is written with status FAIL
And ADMIN receives an alert (via audit log or health endpoint flag)
```

---

## AC-AUD-001 — Audit Log Contains All Demo Actions

```
Given the demo walk-through has been completed covering: login, FIR creation, upload, extraction approval, merge approval, graph view, shortest-path query, RAG query, fairness dashboard view
When the COMPLIANCE user queries the audit log with filter: date=today, user_id=Ananya's ID
Then the audit log contains records for each of the following event types:
  AUTH.LOGIN, FIR.CREATE, FIR.UPLOAD, AI.EXTRACTION.APPROVE (×3), ENTITY.MERGE.APPROVE,
  GRAPH.VIEW, GRAPH.SHORTESTPATH.QUERY, RAG.QUERY (×3), FAIRNESS.DASHBOARD.VIEW
And each record contains user_id, resource_id, timestamp, and district fields
```

---

## AC-AUD-002 — Audit Log — INVESTIGATOR Sees Only Own Actions

```
Given two authenticated users: Ananya (INVESTIGATOR) and Priya (SCRB_ANALYST)
And both have taken actions that appear in the audit log
When Ananya requests GET /audit-log?user_id=Priya_ID
Then the system returns an empty result set
And no audit entries from Priya's session are returned to Ananya
```

---

## AC-AUD-003 — Audit Log — No Delete Permitted

```
Given the audit log contains 50 records
When any user (including ADMIN) submits DELETE /audit-log/{event_id}
Then the system returns HTTP 405 (Method Not Allowed)
And the audit record is not deleted
```

---

## AC-USER-001 — Admin Creates Demo Users

```
Given the ADMIN role is authenticated
When the admin creates user accounts for: Ananya (INVESTIGATOR, Bengaluru Urban), Ramesh (INVESTIGATOR, Mysuru), Priya (SCRB_ANALYST, all), Krishnamurthy (COMPLIANCE, all)
Then each user can log in with their credentials
And each user sees the correct role-specific dashboard
And ADMIN.USER.CREATE audit events are written for each created user
```

---

## AC-USER-002 — Non-Admin Cannot Create Users

```
Given an authenticated SCRB_ANALYST user
When the user submits POST /admin/users with valid fields
Then the system returns HTTP 403
And no user is created
```

---

## AC-SEED-001 — Planted Patterns Verified in Loaded Data

```
Given the synthetic seed data has been loaded via the seed script
When the following assertions are run against the database:
  1. Query PersonEntity for entities with 4+ linked cases → at least 1 result
  2. Query entity_resolution_candidates for confidence ≥ 0.70 → at least 3 results
  3. Run shortest-path BFS between Case 001 and Case 042 → path of length ≤ 4 hops found
  4. Query AnomalyAlert for current week with z-score > 4.0 → at least 1 result
  5. Query RiskScore for score > 0.75 → at least 1 result
Then all 5 assertions pass
```

---

*End of 07-ACCEPTANCE-CRITERIA.md*
