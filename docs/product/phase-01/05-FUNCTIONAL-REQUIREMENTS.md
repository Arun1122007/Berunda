# 05 — Functional Requirements

## Group ERR — Error Handling

> [!NOTE]
> This group was added per Phase 1 verification (P1V-MAJ-006/P1V-MAJ-011). Error handling was previously covered by NFRs only; these requirements make the error-handling capability explicit at the FR level.

### FR-ERR-001 — System Error Handling and Graceful Degradation

| Field | Value |
|-------|-------|
| **FR-ID** | FR-ERR-001 |
| **Name** | System Error Handling and Graceful Degradation |
| **Priority** | P0 (IN MVP) |
| **Feature** | FEAT-006 |
| **Description** | The system shall handle service unavailability (AI extraction, LLM, geocoding, entity resolution), invalid inputs, network timeouts, and resource conflicts (e.g., duplicate upload) without producing an unhandled error or crashing. Each failure mode shall produce a user-visible message indicating what went wrong and, where possible, an alternative action. |
| **Rationale** | AI services (NER, LLM, entity resolution) may be unavailable during the demo. The system must degrade gracefully and continue to serve other features without crashing. |
| **Authorization** | All authenticated users |
| **Verification** | Integration test — disable each AI service endpoint; verify the system returns a graceful error message and continues to serve other endpoints |
| **AC Reference** | AC-AI-004 (extraction failure), AC-RAG-005 (MockProvider fallback), AC-FIR-009 (duplicate upload) |

**Document ID:** BERUNDA-PH1-FR-001
**Version:** 1.0 | **Status:** APPROVED — Authoritative Phase 1 functional requirements
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> Only approved MVP features are documented here.
> Every requirement uses mandatory language: "The system shall…" or "The authorized user shall be able to…"
> No requirement uses vague terms such as user-friendly, fast, secure, or intelligent without a measurable definition.

---

## Group AUTH — Authentication and Authorization

### FR-AUTH-001 — User Authentication

**Requirement:** The system shall authenticate users via a username and password submitted over HTTPS. Upon successful authentication the system shall issue a signed JWT containing the user's ID, role, district scope, issued-at timestamp, and an expiry of 15 minutes for the access token. The system shall issue a refresh token valid for 7 days.

**Rationale:** Prevents unauthorized access to sensitive case records.
**User role:** All users
**Related feature:** FEAT-001
**Preconditions:** User account exists and is active; system is running
**Inputs:** Username (string), password (string)
**Expected behavior:** Valid credentials → JWT issued → user redirected to role-specific dashboard; invalid credentials → HTTP 401 with generic message "Invalid credentials"
**Validation:** Username must be non-empty; password must be non-empty; no other client-side credential constraints
**Authorization:** No role required for this endpoint
**Error behavior:** On 5 consecutive failures within 15 minutes, system shall lock the account for 15 minutes and return HTTP 403 with message "Account temporarily locked"
**Audit behavior:** System shall write an `AUTH.LOGIN` event on success; `AUTH.LOGIN_FAILURE` event on failure; both events include IP address, timestamp, and user ID
**Priority:** P0
**Verification method:** Integration test — submit valid and invalid credentials; verify JWT contents; verify lockout behavior
**Dependencies:** User table provisioned in Catalyst Data Store

---

### FR-AUTH-002 — Session Expiry and Token Refresh

**Requirement:** The system shall reject any API request whose JWT access token has expired with HTTP 401. The system shall provide a token-refresh endpoint that accepts a valid, unexpired refresh token and issues a new access token. The system shall invalidate a refresh token after it has been used once.

**Rationale:** Limits the window of opportunity for stolen token misuse.
**User role:** All users
**Related feature:** FEAT-005
**Preconditions:** User is authenticated
**Inputs:** Expired access token (Authorization header), valid refresh token
**Expected behavior:** Expired access token → 401; valid refresh token → new access token issued; used refresh token → 401 on reuse attempt
**Audit behavior:** System shall write `AUTH.TOKEN_REFRESH` on refresh; `AUTH.SESSION_EXPIRED` on expired-token rejection
**Priority:** P0
**Verification method:** Integration test — use expired token; verify 401; use refresh token; verify new access token; reuse refresh token; verify 401

---

### FR-AUTH-003 — Role-Based Access Control

**Requirement:** The system shall enforce role-based access control (RBAC) on every API endpoint. The system shall read the user's role from the verified JWT claim. The system shall return HTTP 403 if the authenticated user's role does not have the required permission for the requested resource or action. The four permitted roles are INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, and ADMIN.

**Rationale:** Prevents unauthorized access to case data, restricted fields, and administrative functions.
**User role:** All users
**Related feature:** FEAT-002
**Preconditions:** User is authenticated; JWT is valid
**Inputs:** JWT (role claim), requested resource, HTTP method
**Expected behavior:** Role matches required permission → request processed; role does not match → HTTP 403 with message "Access denied: insufficient role"
**Audit behavior:** System shall write `AUTH.ACCESS_DENIED` on every 403 response
**Priority:** P0
**Verification method:** Integration test — attempt each protected endpoint with each role; verify 403 for unauthorized combinations; verify 200 for authorized combinations

---

### FR-AUTH-004 — Jurisdiction Scoping for INVESTIGATOR Role

**Requirement:** The system shall, for all API responses returning case records, persons, vehicles, or derived data (risk scores, entity resolution results, graph data), filter results to records where the associated `CaseMaster.PoliceStationRef` is in the authenticated INVESTIGATOR user's assigned stations. The system shall apply this filter at the database query level, not at the serialization level. SCRB_ANALYST, COMPLIANCE, and ADMIN roles shall receive unfiltered results.

**Rationale:** Prevents cross-station data leakage between jurisdictions.
**User role:** INVESTIGATOR
**Related feature:** FEAT-003
**Preconditions:** User is INVESTIGATOR; JWT contains district and station assignments
**Error behavior:** If station assignment is missing from JWT, system shall return HTTP 403 with "Jurisdiction scope not configured for this account"
**Audit behavior:** No separate audit event; jurisdiction scoping is a query-level control
**Priority:** P0
**Verification method:** Integration test — create cases in two different districts; log in as INVESTIGATOR from District A; confirm District B cases are not returned

---

### FR-AUTH-005 — Protected-Characteristic Field Access Control

**Requirement:** The system shall exclude `CasteRef` and `ReligionRef` columns from all API responses for users with roles INVESTIGATOR and SCRB_ANALYST. The system shall apply this exclusion at the ORM query level by omitting those columns from the SELECT statement, not by nulling them at serialization. For users with the COMPLIANCE role, the system shall return only aggregate counts of `CasteRef` and `ReligionRef` values per district and crime head, never individual-level records. The ADMIN role may access individual-level `CasteRef` and `ReligionRef` values for system management purposes only.

**Rationale:** Implements ADR-007 (protected-characteristic exclusion) and resolves CONFLICT-005.
**User role:** All — differential behavior by role
**Related feature:** FEAT-064
**Preconditions:** User is authenticated; request targets Accused, Victim, or ComplainantDetails records
**Audit behavior:** System shall write `RESTRICTED.FIELD.ACCESS` with the user's role, user ID, and requested resource when COMPLIANCE or ADMIN accesses CasteRef or ReligionRef
**Priority:** P0
**Verification method:** Integration test — query Accused with INVESTIGATOR and SCRB_ANALYST roles; verify CasteRef and ReligionRef are absent from response; query with COMPLIANCE; verify only aggregate response

---

### FR-AUTH-006 — User Management (Admin)

**Requirement:** The authorized ADMIN user shall be able to: create a new user account with a specified username, role, district assignment, and initial password; change an existing user's role; deactivate an existing user account; unlock a locked user account. The system shall reject any user-management operation submitted by a non-ADMIN role with HTTP 403.

**Rationale:** Demo requires provisioning of test accounts; production requires administrative user lifecycle management.
**User role:** ADMIN
**Related feature:** FEAT-081
**Inputs:** Username, display name, role (enum: INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, ADMIN), district code, password
**Expected behavior:** Valid inputs → user created; role assigned; audit event written; duplicate username → HTTP 409 with "Username already exists"
**Audit behavior:** `ADMIN.USER.CREATE`, `ADMIN.ROLE.CHANGE`, `ADMIN.USER.DEACTIVATE`, `ADMIN.USER.UNLOCK` events, each with admin's user ID and affected user ID
**Priority:** P0
**Verification method:** Integration test — create user via ADMIN API; attempt same via INVESTIGATOR; verify 403

---

## Group FIR — FIR Registration and Management

### FR-FIR-001 — Manual FIR Creation

**Requirement:** The authorized INVESTIGATOR or ADMIN user shall be able to create a new FIR record by submitting the following required fields: occurrence date and time, FIR date, district reference (from the district lookup table), police station reference (from the station lookup table), crime head reference (from the CrimeHead lookup table), and BriefFacts text (minimum 10 characters, maximum 5000 characters). The system shall save the record to `CaseMaster` and return the new record ID and the auto-generated CrimeNo.

**Rationale:** Core FIR registration workflow — required for JOURNEY-001.
**User role:** INVESTIGATOR (own district), ADMIN (all)
**Related feature:** FEAT-010
**Preconditions:** User is authenticated; Catalyst Data Store is provisioned; CrimeHead, DistrictRef, and PoliceStation lookup tables are populated
**Inputs:** OccurrenceDate, OccurrenceTime, FIRDate, DistrictRef (FK), PoliceStationRef (FK), CrimeHeadRef (FK), BriefFacts (text)
**Expected behavior:** Valid inputs → FIR saved with status REGISTERED → CrimeNo generated → NER extraction queued → HTTP 201 with new case ID and CrimeNo
**Validation:** All required fields present; OccurrenceDate not in the future; BriefFacts ≥ 10 characters; DistrictRef, PoliceStationRef, CrimeHeadRef must exist in lookup tables; for INVESTIGATOR, PoliceStationRef must be in user's assigned stations
**Error behavior:** Missing required field → HTTP 422 with field-level error messages identifying each missing or invalid field
**Audit behavior:** `FIR.CREATE` event with case ID, user ID, district, and timestamp
**Priority:** P0
**Verification method:** Integration test — submit valid and invalid FIR forms; verify saved record; verify CrimeNo format; verify audit event

---

### FR-FIR-002 — CrimeNo Auto-Generation

**Requirement:** The system shall auto-generate a unique CrimeNo for every new FIR in the format: `{DistrictCode}/{StationCode}/{Year}/{SequenceNumber}` where SequenceNumber is a zero-padded 4-digit integer incremented per station per year. The system shall guarantee uniqueness of CrimeNo within the Data Store. The system shall not accept a user-supplied CrimeNo.

**Rationale:** Manual CrimeNo entry causes duplicates and format errors.
**User role:** System (no user input required)
**Related feature:** FEAT-012
**Inputs:** DistrictRef, PoliceStationRef, FIRDate (year component)
**Error behavior:** If sequence number generation fails, system shall return HTTP 500 and log the failure; the FIR shall not be saved
**Priority:** P0
**Verification method:** Integration test — create 3 FIRs for the same station in the same year; verify CrimeNos are sequential; attempt duplicate CrimeNo insert; verify it is rejected

---

### FR-FIR-003 — FIR Document Upload

**Requirement:** The authorized INVESTIGATOR shall be able to upload a document file (PDF, JPEG, or PNG; maximum 10 MB for PDF, 5 MB for image) to associate with an FIR. The system shall validate the file type by reading the MIME type from the file content (not the file extension). The system shall store the file in Catalyst Stratus and record the SHA-256 hash, file name, upload timestamp, uploading user ID, and associated case ID in `EvidenceMaster`. The system shall then trigger the AI extraction pipeline for the uploaded file.

**Rationale:** FIR documents submitted on paper must be digitized and extracted; officers should not have to retype content manually.
**User role:** INVESTIGATOR (own district), ADMIN
**Related feature:** FEAT-011
**Inputs:** File (binary), case ID
**Expected behavior:** Valid file → uploaded to Stratus → hash recorded → extraction triggered → HTTP 200 with evidence record ID
**Validation:** MIME type must be application/pdf, image/jpeg, or image/png; file size within limits; case ID must exist and be in user's jurisdiction
**Error behavior:** Invalid type → HTTP 415 with "Unsupported file type. Accepted types: PDF, JPEG, PNG"; file too large → HTTP 413 with size limit stated; Stratus unavailable → HTTP 503 with retry guidance; OCR failure → file stored; HTTP 200 returned with extraction_status: FAILED and message "Extraction failed. Enter data manually."
**Audit behavior:** `FIR.UPLOAD` event with case ID, file hash, file size, and user ID
**Priority:** P0
**Verification method:** Integration test — upload valid and invalid files; verify Stratus storage; verify hash in EvidenceMaster; verify MIME validation rejects misnamed files

---

### FR-FIR-004 — FIR Status Lifecycle

**Requirement:** The system shall maintain and enforce a status lifecycle for each FIR record: `REGISTERED` (initial state after creation) → `EXTRACTION_PENDING` (after upload triggers extraction) → `EXTRACTION_APPROVED` (after officer approves AI extraction) → `UNDER_INVESTIGATION` (after case is assigned to an IO) → `CLOSED` (after case resolution). The system shall reject any status transition that skips a required intermediate state. Status updates shall only be made by authorized roles.

**Rationale:** Structured status tracking supports supervisor oversight and case-load reporting.
**User role:** INVESTIGATOR (limited transitions), SCRB_ANALYST (status update), ADMIN (all transitions)
**Related feature:** FEAT-015
**Audit behavior:** `FIR.STATUS_CHANGE` event with old status, new status, case ID, and user ID on every valid status change
**Priority:** P0
**Verification method:** Integration test — attempt valid and invalid status transitions; verify enforcement

---

### FR-FIR-005 — FIR Detail View

**Requirement:** The authorized user shall be able to retrieve the complete detail of a single FIR by case ID. The response shall include: CaseMaster record, list of accused persons (excluding CasteRef/ReligionRef for non-COMPLIANCE roles), list of victim persons (same exclusion), complainant details (same exclusion), linked vehicles, occurrence place, AI extraction status, investigation notes (if any), and current case status. The system shall apply jurisdiction scoping for INVESTIGATOR users.

**Rationale:** Officers need a structured case overview to make investigation decisions.
**User role:** INVESTIGATOR (own district), SCRB_ANALYST (all), COMPLIANCE (all), ADMIN (all)
**Related feature:** FEAT-013
**Audit behavior:** `CASE.VIEW` event with case ID, user ID, and timestamp
**Priority:** P0
**Verification method:** Integration test — request case detail; verify all sections; verify restricted fields are absent for non-COMPLIANCE roles

---

## Group AI — AI Assistance

### FR-AI-001 — Named Entity Recognition Extraction

**Requirement:** After a BriefFacts text is submitted (via manual FIR creation or document upload), the system shall execute a Named Entity Recognition pipeline using the approved spaCy English model to extract: person names (with suggested roles: accused, victim, complainant, or unknown), vehicle registration numbers in Karnataka format (two letters, two digits, two letters, four digits), and location names (districts, areas, landmarks). The system shall store each extracted entity as a suggestion in the extraction queue with its text span, entity type, and confidence score. The system shall not directly save extracted entities to the main person, vehicle, or location tables without officer approval.

**Rationale:** Automates structured extraction from unstructured FIR narratives; officer review gate ensures no AI error becomes official record.
**User role:** System (triggered automatically)
**Related feature:** FEAT-020
**Preconditions:** BriefFacts text is at least 10 characters; spaCy model is loaded
**Error behavior:** If spaCy model is unavailable, system shall set extraction_status to FAILED, log the failure, and notify the officer that manual entry is required. The original BriefFacts text shall be preserved.
**Audit behavior:** `AI.EXTRACTION.TRIGGERED` event with case ID and extraction queue ID
**Priority:** P0
**Verification method:** Integration test — submit BriefFacts containing a person name, vehicle registration, and location; verify extracted entities in queue; verify none are saved to main tables before approval

---

### FR-AI-002 — AI Confidence Score Display

**Requirement:** The system shall display a confidence percentage alongside each AI-extracted entity suggestion. The system shall visually distinguish confidence levels: green for ≥ 80%, amber for 60–79%, red for below 60%. The confidence percentage shall be stored in the extraction record and preserved in the audit log when the officer approves or rejects the entity.

**Rationale:** Officers need to know how reliable each suggestion is before approving.
**User role:** INVESTIGATOR
**Related feature:** FEAT-055
**Priority:** P0
**Verification method:** UI test — verify colour coding; integration test — verify confidence stored in audit event

---

### FR-AI-003 — Human Review and Correction of AI Extraction

**Requirement:** The authorized INVESTIGATOR shall be able to, for each AI-extracted entity suggestion: approve the entity as-is, edit one or more fields and then approve, or reject the entity. The system shall not create a person, vehicle, or location record from an AI suggestion until the officer takes an explicit approve action. When an entity is approved, the system shall create the corresponding record. When an entity is rejected, the system shall log the rejection and take no further action on that entity. The officer shall be able to add entities that AI did not extract by using a manual add form.

**Rationale:** AI outputs require human review; no AI suggestion may become an official record without officer action.
**User role:** INVESTIGATOR (own district), ADMIN
**Related feature:** FEAT-021
**Audit behavior:** `AI.EXTRACTION.APPROVE` event per approved entity (with confidence score); `AI.EXTRACTION.REJECT` per rejected entity; `AI.EXTRACTION.EDIT` when the officer modifies the suggested value before approving
**Priority:** P0
**Verification method:** Integration test — approve one entity, edit another, reject a third; verify database contains only the approved and edited entities; verify audit log contains all three event types

---

### FR-AI-004 — AI Extraction Failure Preservation

**Requirement:** The system shall preserve the original BriefFacts text and all uploaded document files in the event of any AI extraction failure. The system shall not delete, overwrite, or modify the original input if extraction fails. The system shall set the extraction status to FAILED and present the officer with the option to proceed with manual entity entry.

**Rationale:** Prevents data loss when AI services are unavailable.
**User role:** System
**Related feature:** FEAT-006
**Priority:** P0
**Verification method:** Integration test — simulate extraction failure; verify original text intact; verify manual entry option shown

---

### FR-AI-005 — Cross-Case Entity Resolution

**Requirement:** The system shall execute an entity resolution pipeline on newly approved person records. The pipeline shall use rule-based blocking (Soundex phonetic blocking on surname) followed by weighted feature scoring (name similarity weight: 0.4, date-of-birth similarity weight: 0.3, address token overlap weight: 0.2, phone number last-4 match weight: 0.1). The pipeline shall produce merge candidates where the weighted score exceeds 0.50. The system shall store each merge candidate in the entity resolution queue with: PersonA ID, PersonB ID, confidence score, and the top 3 contributing matching signals.

**Rationale:** Connects persons across FIRs who appear under name variations; surfaces repeat offenders.
**User role:** System (triggered after extraction approval)
**Related feature:** FEAT-022
**Preconditions:** At least 2 approved person records exist
**Error behavior:** If the pipeline fails, system shall log the failure and set the candidate's status to PIPELINE_ERROR; the underlying person records are not affected
**Audit behavior:** `ENTITY.RESOLUTION.CANDIDATE.CREATED` event with candidate ID and confidence
**Priority:** P0
**Verification method:** Integration test — approve 4 persons with name variations for the same individual; verify a merge candidate appears with confidence ≥ 0.70

---

### FR-AI-006 — Entity Resolution Merge Review

**Requirement:** The authorized INVESTIGATOR shall be able to view entity resolution merge candidates for persons in their jurisdiction. For each candidate, the system shall display: PersonA and PersonB side-by-side with all non-restricted fields, the confidence score, and the top 3 matching signals. The officer shall be able to approve a merge, reject a merge, or defer a merge. On approval, the system shall designate one PersonEntity as the canonical record, link all cases from both persons to the canonical record, and move the non-canonical record to a merged state. On rejection, both persons remain separate. On deferral, the candidate is re-queued and returned 7 days later.

**Rationale:** Human approval is required for all entity resolution decisions; automated merges could corrupt case records.
**User role:** INVESTIGATOR (own district), ADMIN (cross-district)
**Related feature:** FEAT-023
**Audit behavior:** `ENTITY.MERGE.APPROVE` with confidence score, both person IDs, and canonical ID; `ENTITY.MERGE.REJECT`; `ENTITY.MERGE.DEFER`
**Priority:** P0
**Verification method:** Integration test — approve merge of planted repeat-offender candidates; verify all 4 cases linked to one PersonEntity

---

### FR-AI-007 — PersonEntity Canonical Profile

**Requirement:** The system shall provide a PersonEntity profile view that aggregates: the canonical name, all known name aliases, all case IDs linked to this entity, the risk score (if computed), and a summary count of cases by role (accused, victim, complainant). The system shall apply jurisdiction scoping for INVESTIGATOR users.

**Rationale:** Officers need a unified person view across all cases.
**User role:** INVESTIGATOR (own district), SCRB_ANALYST (all), ADMIN (all)
**Related feature:** FEAT-024
**Priority:** P0
**Verification method:** Integration test — create entity with 4 linked cases; verify profile shows all 4 case IDs and correct alias list

---

### FR-AI-008 — Relationship Graph Rendering

**Requirement:** The system shall render a force-directed graph using Cytoscape.js for a selected PersonEntity or case. The graph shall represent: cases as blue square nodes, person entities as orange circular nodes, vehicles as grey diamond nodes, and locations as green triangular nodes. Edges shall represent relationships: accused-in, victim-in, co-accused-with, vehicle-linked-to, located-at. The system shall apply jurisdiction scoping when building the graph data for INVESTIGATOR users.

**Rationale:** Visual relationship graph is the primary differentiating capability of the demo.
**User role:** INVESTIGATOR (own district), SCRB_ANALYST (all)
**Related feature:** FEAT-030
**Audit behavior:** `GRAPH.VIEW` event with entity ID and graph node count
**Priority:** P0
**Verification method:** UI test — render graph for planted PersonEntity with 4 linked cases; verify all case nodes and edge types are visible

---

### FR-AI-009 — Hidden-Link Discovery (Shortest Path)

**Requirement:** The authorized user shall be able to select any two nodes in the relationship graph and request the shortest path between them. The system shall compute the shortest path using a breadth-first search (BFS) on the in-memory NetworkX graph with a maximum depth of 5 hops. The system shall highlight the path in the graph and list the intermediate nodes with their relationship types. If no path exists within 5 hops, the system shall display "No path found within 5 hops."

**Rationale:** Discovering indirect connections between cases is the most compelling investigative feature.
**User role:** INVESTIGATOR (own district scope), SCRB_ANALYST (all)
**Related feature:** FEAT-031
**Audit behavior:** `GRAPH.SHORTESTPATH.QUERY` with source node ID, target node ID, and path length
**Priority:** P0
**Verification method:** Integration test — call shortest-path API for planted Case 001 and Case 042 that share a vehicle; verify path returns through the shared vehicle node

---

### FR-AI-010 — RAG Natural-Language Query

**Requirement:** The system shall provide a natural-language query interface that accepts a plain-English question from the authenticated user. The system shall: (1) embed the query; (2) retrieve the top-K most relevant FIR text chunks from the RAG corpus that the user is authorized to access; (3) inject the retrieved chunks into an LLM prompt as grounding context; (4) return the LLM-generated answer. The system shall apply the user's jurisdiction scope when retrieving chunks — INVESTIGATOR users shall not receive chunks from cases outside their assigned stations.

**Rationale:** Natural-language access is the most accessible demo feature for non-technical judges.
**User role:** INVESTIGATOR (jurisdiction-scoped), SCRB_ANALYST (all)
**Related feature:** FEAT-050
**Preconditions:** RAG corpus has been built from loaded FIR records; LLM provider is available or MockProvider is active
**Error behavior:** LLM unavailable → MockProvider activated; system returns a mock answer with disclaimer "AI assistant is in limited mode."
**Audit behavior:** `RAG.QUERY` event with user ID, question text (not the answer), and list of retrieved case IDs
**Priority:** P0
**Verification method:** Integration test — submit 3 rehearsed questions; verify cited case IDs appear in response; verify jurisdiction scoping on chunk retrieval

---

### FR-AI-011 — AI MockProvider Fallback

**Requirement:** The system shall maintain a MockProvider implementation for all AI services (NER extraction, RAG query, FIR summarisation) that returns pre-defined, structurally valid responses without calling any external API. The system shall automatically switch to the MockProvider if the primary AI provider returns a connection error or HTTP 5xx. The system shall indicate to the user when the MockProvider is active via a visible banner: "AI assistant is in limited mode — contact admin if this persists."

**Rationale:** Demo failure due to API unavailability is a Very High risk; MockProvider eliminates this failure mode.
**User role:** System
**Related feature:** FEAT-056
**Priority:** P0
**Verification method:** Integration test — set LLM API key to invalid; verify MockProvider is activated; verify banner is shown; verify response is structurally valid

---

### FR-AI-012 — RAG Answer Source Citation

**Requirement:** Every RAG answer shall include a citations section listing the case IDs (CrimeNos) of the FIR chunks retrieved to ground the answer. The system shall not present a RAG answer without at least one citation. If no relevant chunks are retrieved, the system shall return "I could not find relevant case records to answer this question. Try rephrasing or searching directly."

**Rationale:** Prevents hallucinated answers; maintains auditability of AI outputs.
**User role:** System
**Related feature:** FEAT-054
**Priority:** P0
**Verification method:** Integration test — submit a question about a planted case; verify citation contains the expected CrimeNo

---

### FR-AI-013 — Explainable Risk Scoring

**Requirement:** The system shall compute a repeat-offender risk score for each resolved PersonEntity that has at least 2 prior case links. The risk score shall be a value between 0.0 and 1.0 computed using a scikit-learn classifier trained on the following features: PriorCaseCount (integer), DaysSinceLastCase (integer), CrimeTypeCount (integer count of distinct crime head categories), and AverageSeverityScore (float from crime head severity lookup). The system shall explicitly verify that CasteRef and ReligionRef are not present in the feature set before training. The score shall be stored in the RiskScore table with the model version and computation timestamp.

**Rationale:** Provides data-driven prioritisation for investigations; explainability is required for responsible AI.
**User role:** System (batch computation); INVESTIGATOR and SCRB_ANALYST (view)
**Related feature:** FEAT-060
**Audit behavior:** `RISK.VIEW` event when a user views a risk score, including score value and top 5 feature weights
**Priority:** P0
**Verification method:** Integration test — load PersonEntity with 5 prior cases; verify score is computed; verify CasteRef and ReligionRef are not in the feature list

---

### FR-AI-014 — Feature Importance Display

**Requirement:** The system shall display the top 5 features contributing to a risk score alongside their weights. The feature importance shall be derived from the model's coefficient magnitudes or SHAP values. The display shall include a label for each feature in plain English (e.g., "Number of prior cases", "Days since last case"). The system shall never display CasteRef or ReligionRef as a feature.

**Rationale:** Black-box risk scores are not acceptable in a policing context; officers must be able to verify what the score is based on.
**User role:** INVESTIGATOR, SCRB_ANALYST
**Related feature:** FEAT-061
**Priority:** P0
**Verification method:** UI test — verify feature importance bar chart shows 5 features with human-readable labels

---

### FR-AI-015 — Fairness Verification Check

**Requirement:** The system shall run a fairness verification check on the risk scoring model before each batch scoring run. The check shall: (1) verify that CasteRef and ReligionRef column names are absent from the model's feature list; (2) verify that no column correlated > 0.7 with CasteRef or ReligionRef is included in the feature list. The check result shall be stored in `gov_FairnessCheckResult` with: timestamp, model version, check status (PASS or FAIL), and the list of features checked. If the check fails, the system shall halt scoring and alert the ADMIN role.

**Rationale:** Prevents discriminatory scoring; ADR-007 requires programmatic verification.
**User role:** System
**Related feature:** FEAT-062
**Audit behavior:** `FAIRNESS.CHECK.RUN` event with check result, model version, and timestamp
**Priority:** P0
**Verification method:** Integration test — inject CasteRef into test feature list; verify check returns FAIL; verify scoring is halted

---

### FR-AI-016 — Fairness Dashboard

**Requirement:** The system shall provide a fairness verification dashboard accessible to COMPLIANCE and SCRB_ANALYST roles. The dashboard shall display: the timestamp of the last fairness check, the overall status (PASS or FAIL), a per-model table showing each model name, the features checked, whether CasteRef appears, whether ReligionRef appears, and the status. COMPLIANCE users shall be able to view the full feature list for any model. SCRB_ANALYST users shall see a read-only summary without the full feature list.

**User role:** COMPLIANCE (full), SCRB_ANALYST (read-only)
**Related feature:** FEAT-063
**Priority:** P0
**Verification method:** UI test — log in as COMPLIANCE; verify full feature list visible; log in as SCRB_ANALYST; verify read-only summary; log in as INVESTIGATOR; verify 403

---

## Group SRCH — Search

### FR-SRCH-001 — Global Entity Search

**Requirement:** The authorized user shall be able to submit a search query of at least 3 characters against the global search index. The system shall search across: PersonEntity.CanonicalName, PersonEntity.aliases (array field), VehicleLink.RegistrationNo, and CaseMaster.CrimeNo. The system shall apply jurisdiction scoping for INVESTIGATOR users. The system shall return results grouped by type (Persons, Vehicles, Cases) with a maximum of 100 results per type. Results shall be returned within 3 seconds for a corpus of up to 5000 FIRs.

**Rationale:** Officers spend hours manually cross-referencing; fast search is critical to the investigation workflow.
**User role:** INVESTIGATOR (jurisdiction-scoped), SCRB_ANALYST (all)
**Related feature:** FEAT-014
**Inputs:** Search query string (minimum 3 characters)
**Error behavior:** Query less than 3 characters → HTTP 422; no results → HTTP 200 with empty result set and message "No results found"
**Audit behavior:** `SEARCH.QUERY` event with query string and result count (not individual results, to avoid logging sensitive data)
**Priority:** P0
**Verification method:** Integration test — search for planted person by exact name, by alias, and by vehicle registration; verify correct results; verify cross-district results excluded for INVESTIGATOR

---

## Group RPT — Analytics and Reporting

### FR-RPT-001 — Geospatial Hotspot Heatmap

**Requirement:** The system shall render a heatmap overlay on a MapLibre GL map centred on Karnataka showing crime density by district. Density shall be computed from the count of CaseMaster records grouped by DistrictRef. SCRB_ANALYST and ADMIN users shall see all districts. INVESTIGATOR users shall see only their assigned district. The heatmap shall update when the user applies a crime-type or date-range filter.

**User role:** INVESTIGATOR (own district), SCRB_ANALYST (all)
**Related feature:** FEAT-040
**Priority:** P0
**Verification method:** UI test — verify heatmap renders; apply crime-type filter; verify density updates

---

### FR-RPT-002 — District-to-Station Drill-Down

**Requirement:** The authorized user shall be able to click a district on the hotspot map and see a station-level breakdown of case counts within that district. The system shall display a side panel listing police stations in the selected district, each with a case count. Clicking a station shall filter the case list to cases from that station in the current time period and crime-type filter.

**User role:** INVESTIGATOR (own district), SCRB_ANALYST (all)
**Related feature:** FEAT-041
**Priority:** P0
**Verification method:** UI test — click planted district; verify station list; click station; verify case list

---

### FR-RPT-003 — Crime Type and Date Range Filter

**Requirement:** The authorized user shall be able to apply the following filters to the hotspot map and analytics views: crime head (searchable dropdown from the CrimeHead lookup table) and date range (preset options: Last 7 days, Last 30 days, Last 90 days; plus a custom date picker). The system shall update the heatmap, anomaly alerts, and trend charts when filters change.

**User role:** INVESTIGATOR (own district), SCRB_ANALYST (all)
**Related feature:** FEAT-042
**Priority:** P0
**Verification method:** UI test — apply crime-type filter; verify map updates; apply date filter; verify trend chart updates

---

### FR-RPT-004 — Anomaly Detection and Alerts

**Requirement:** The system shall compute a z-score for each district and crime-head combination by comparing the current week's case count to the rolling 12-week baseline. The system shall create an AnomalyAlert record when z-score > 2.0 (LOW), > 3.0 (MEDIUM), or > 4.0 (HIGH). The system shall display anomaly badges on the hotspot map at affected districts. The badge shall show the severity level and crime type. Clicking the badge shall display the alert detail and link to the contributing cases.

**User role:** INVESTIGATOR (own district), SCRB_ANALYST (all)
**Related feature:** FEAT-043
**Priority:** P0
**Verification method:** Integration test — load synthetic data with planted 5× spike in one district for one week; verify AnomalyAlert record created with z-score > 4.0; verify badge appears on map

---

## Group AUD — Audit Logging

### FR-AUD-001 — Audit Event Recording

**Requirement:** The system shall record an audit event in `gov_AuditLog` for every action listed in the Phase 1 audit event register (see `02-STAKEHOLDERS-AND-USER-ROLES.md` Section 12). Each audit record shall contain: event ID, event type, user ID, resource type, resource ID, timestamp (ISO 8601 UTC), district, and a JSON details field. The system shall write the audit record before returning the API response. If the audit write fails, the system shall log the failure to a local error log but shall still return the original API response (audit failure shall not block user operations).

**Rationale:** Auditability of every sensitive action is a core governance requirement.
**User role:** System
**Related feature:** FEAT-004
**Priority:** P0
**Verification method:** Integration test — perform a sequence of actions; verify audit log contains a record for each action with correct fields

---

### FR-AUD-002 — Audit Log View

**Requirement:** The authorized COMPLIANCE and ADMIN users shall be able to query the audit log with the following filter combinations: date range, user ID, event type, resource type. INVESTIGATOR and SCRB_ANALYST users shall be able to query only their own audit entries. The system shall apply row-level security at the query level — non-COMPLIANCE users shall not be able to retrieve audit entries from other users by manipulating query parameters. The audit log shall be read-only — no user, including ADMIN, shall be able to delete or modify audit records via the API.

**User role:** COMPLIANCE (all entries), ADMIN (all entries), INVESTIGATOR (own only), SCRB_ANALYST (own only)
**Related feature:** FEAT-080
**Priority:** P0
**Verification method:** Integration test — query as COMPLIANCE; verify all entries; query as INVESTIGATOR with another user's ID; verify empty result; attempt DELETE on audit log; verify 405

---

*End of 05-FUNCTIONAL-REQUIREMENTS.md*
