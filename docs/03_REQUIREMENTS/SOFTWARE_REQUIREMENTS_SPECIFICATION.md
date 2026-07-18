# Software Requirements Specification

[//]: # (Document ID: BERUNDA-SRS-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Architects, QA | Source: 01_Enterprise_Blueprint + SRS references | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Functional Requirements

### 1.1 Data Ingestion

#### FR-001: FIR Structured Import

**Description:** System shall ingest FIR/incident records from structured Excel/CSV files into the Data Store schema
**Rationale:** Investigators need to bulk-import legacy FIR records into the system efficiently without manual re-entry, enabling downstream analytics and entity resolution at scale.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** DR-001 (Source Schema Migration), DR-005 (CrimeNo Parsing)
**Security/Privacy Implications:** Imported FIRs may contain sensitive PII; file upload handling must be secured against malicious file injection.
**Source:** 01_Blueprint §4.1
**Acceptance Criteria:**
- Given an authorized Investigator uploads a valid Excel/CSV FIR file, when the system processes the file, then all records are ingested into the Data Store schema with correct field mapping and no data loss.
**Verification Method:** Test
**Demo Evidence:** Imported case list visible in dashboard

#### FR-002: FIR Manual Entry

**Description:** System shall provide a manual entry form for FIR data input
**Rationale:** Not all FIR records are available in digital structured format; officers in the field need a form-based interface to enter individual cases directly.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** DR-001
**Security/Privacy Implications:** Form submission must validate and sanitize all inputs to prevent XSS and injection attacks.
**Source:** 01_Blueprint §4.1
**Acceptance Criteria:**
- Given an Investigator opens the manual entry form, when they fill all required fields and submit, then the FIR record is persisted in the Data Store and visible in the case list.
**Verification Method:** Test
**Demo Evidence:** Imported case list visible in dashboard

#### FR-003: Data Validation

**Description:** System shall validate imported data for required fields, referential integrity, and type correctness
**Rationale:** Invalid or incomplete data corrupts downstream analytics and entity resolution; upfront validation ensures data quality at the point of ingestion.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-001, FR-002
**Security/Privacy Implications:** Validation logic must not leak internal schema details in error messages.
**Source:** 01_Blueprint §6.7
**Acceptance Criteria:**
- Given an imported record with missing required fields or invalid types, when validation runs, then the record is rejected with a specific error message identifying the issue.
**Verification Method:** Test
**Demo Evidence:** Imported case list visible in dashboard

#### FR-004: Duplicate Detection

**Description:** System shall detect and flag potential duplicate FIR records based on CrimeNo
**Rationale:** Duplicate case entries distort crime statistics and waste investigative effort; automated flagging alerts the user to possible duplicates before they proliferate.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** SHOULD
**Scope:** MVP
**Dependencies:** FR-001, FR-003
**Security/Privacy Implications:** N/A
**Source:** 01_Blueprint §6.8
**Acceptance Criteria:**
- Given a CrimeNo already exists in the database, when an import or entry uses the same CrimeNo, then the system flags the duplicate and prompts the user to review.
**Verification Method:** Test
**Demo Evidence:** Imported case list visible in dashboard

### 1.2 Entity Extraction

#### FR-005: English NER

**Description:** System shall extract person names, locations, vehicles, and organizations from English FIR narrative text
**Rationale:** FIR narratives contain rich unstructured details about involved entities; automated extraction surfaces these for linking and analysis without manual reading.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** AIR-001
**Security/Privacy Implications:** Extracted entities may include sensitive personal data; extraction pipeline must operate within access controls.
**Source:** 01_Blueprint §8.1
**Acceptance Criteria:**
- Given an English FIR narrative, when the NER pipeline processes it, then all person names, locations, vehicles, and organizations are extracted with entity type labels and confidence scores.
**Verification Method:** Test
**Demo Evidence:** Extracted entities highlighted in the FIR narrative view

#### FR-006: Kannada NER

**Description:** System shall extract entities from Kannada FIR narrative text
**Rationale:** A significant portion of FIRs in Karnataka are filed in Kannada; supporting Kannada NER ensures inclusive coverage across the state's linguistic landscape.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** SHOULD
**Scope:** STRETCH
**Dependencies:** AIR-008
**Security/Privacy Implications:** Same as FR-005.
**Source:** 01_Blueprint §8.1
**Acceptance Criteria:**
- Given a Kannada FIR narrative, when the Kannada NER pipeline processes it, then named entities are extracted with type labels and confidence scores.
**Verification Method:** Test
**Demo Evidence:** Extracted entities highlighted in a Kannada FIR narrative view

#### FR-007: Confidence Scoring

**Description:** Every extracted entity shall include a confidence score
**Rationale:** NER predictions vary in reliability; confidence scores allow investigators to prioritize high-certainty links and flag uncertain ones for manual review.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-005, FR-006
**Security/Privacy Implications:** N/A
**Source:** 01_Blueprint §8.1
**Acceptance Criteria:**
- Given an entity extracted from any narrative, when the extraction result is returned, then a confidence score between 0.0 and 1.0 is included for that entity.
**Verification Method:** Test
**Demo Evidence:** Entity list panel showing confidence bars per extracted entity

#### FR-008: Entity Linking

**Description:** Extracted entities shall be linked to the originating CaseMaster record
**Rationale:** Entities have no investigative value in isolation; linking them to cases enables cross-case analysis and relationship discovery.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-005, FR-007, DR-002
**Security/Privacy Implications:** N/A
**Source:** 01_Blueprint §8.1
**Acceptance Criteria:**
- Given an extracted entity, when the extraction pipeline completes, then the entity record includes a foreign key reference to the source CaseMaster record.
**Verification Method:** Test
**Demo Evidence:** Entity detail page showing source case reference

### 1.3 Entity Resolution

#### FR-009: PersonEntity Identity

**Description:** System shall maintain a PersonEntity table as a deduplicated cross-case identity store
**Rationale:** A single person may appear across multiple FIRs; a unified identity store prevents duplicate person records and enables accurate cross-case linkage.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** DR-002
**Security/Privacy Implications:** PersonEntity consolidates sensitive PII; access must be tightly controlled and audited.
**Source:** 01_Blueprint §6.3
**Acceptance Criteria:**
- Given extracted person references from multiple cases, when entity resolution runs, then matching references are consolidated into a single PersonEntity record.
**Verification Method:** Test
**Demo Evidence:** PersonEntity list showing merged identities with source case references

#### FR-010: Blocking Strategy

**Description:** System shall use blocking (name similarity + age band + address/locality overlap) for candidate generation
**Rationale:** Pairwise comparison of all person references is computationally infeasible; blocking reduces the candidate space to likely matches for efficient scoring.
**Stakeholder:** STK-001:Investigating Officer / STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-009
**Security/Privacy Implications:** Blocking criteria must not use protected attributes (caste, religion) as blocking keys.
**Source:** 01_Blueprint §6.3
**Acceptance Criteria:**
- Given a new person reference, when the blocking strategy executes, then only candidates sharing similar name, age band, or locality are generated for scoring.
**Verification Method:** Test
**Demo Evidence:** Processing log showing candidate pair count reduction

#### FR-011: Similarity Scoring

**Description:** System shall compute weighted similarity score for candidate record pairs
**Rationale:** Objective similarity scores provide a consistent, quantitative basis for match decisions rather than subjective judgment.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-010
**Security/Privacy Implications:** N/A
**Source:** 01_Blueprint §6.3
**Acceptance Criteria:**
- Given a candidate pair of person references, when similarity scoring runs, then a weighted composite score between 0.0 and 1.0 is produced.
**Verification Method:** Test
**Demo Evidence:** Resolution UI showing similarity scores per candidate pair

#### FR-012: Match Thresholds

**Description:** System shall support configurable match/possible/no-match thresholds with a grey zone requiring manual review
**Rationale:** Strict binary matching is brittle; configurable thresholds and a grey zone allow organizations to calibrate sensitivity and ensure human judgment for borderline cases.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-011
**Security/Privacy Implications:** N/A
**Source:** 01_Blueprint §6.3
**Acceptance Criteria:**
- Given configured thresholds (match ≥ 0.85, possible 0.70–0.84, no-match < 0.70), when a candidate pair scores 0.78, then it is classified as "possible" and queued for manual review.
**Verification Method:** Test
**Demo Evidence:** Admin settings page showing configurable threshold sliders

#### FR-013: Manual Review

**Description:** System shall present possible matches to an Investigator for manual confirmation
**Rationale:** Automated matching can produce false positives in the grey zone; human review ensures accuracy and accountability for identity merges.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-012
**Security/Privacy Implications:** Review UI must hide sensitive data (caste/religion) from non-Compliance roles.
**Source:** 01_Blueprint §6.3
**Acceptance Criteria:**
- Given a possible match in the grey zone, when an Investigator opens the review queue, then the candidate pair is displayed with similarity details and the option to confirm or reject.
**Verification Method:** Test
**Demo Evidence:** Manual review screen showing candidate pair with confirm/reject buttons

#### FR-014: Merge Approval

**Description:** Only a human reviewer may confirm a merge; no auto-merges
**Rationale:** Automated identity merging carries significant privacy and accuracy risks; requiring human approval ensures accountability and prevents erroneous consolidation.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-013
**Security/Privacy Implications:** Merge actions must be logged to AuditLog with reviewer identity.
**Source:** 01_Blueprint §7.1
**Acceptance Criteria:**
- Given a candidate pair scored above the match threshold, when the resolution process completes, then no automatic merge occurs; the merge only happens after explicit human approval.
**Verification Method:** Test
**Demo Evidence:** Audit log showing merge approval event with reviewer ID

#### FR-015: Provenance Tracking

**Description:** Every PersonEntityLink shall record source table, source record ID, and match confidence
**Rationale:** Traceability is essential for auditing entity resolution decisions and for reversing erroneous merges when discovered.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-009, FR-014
**Security/Privacy Implications:** Provenance metadata supports audit investigations but must not expose full source record contents.
**Source:** 01_Blueprint §6.3
**Acceptance Criteria:**
- Given a confirmed PersonEntityLink, when the link record is created, then it includes source_table, source_record_id, and match_confidence fields.
**Verification Method:** Test
**Demo Evidence:** Entity link detail view showing provenance fields

### 1.4 Relationship Graph

#### FR-016: RelationshipEdge Table

**Description:** System shall maintain a RelationshipEdge table with person_entity_a, person_entity_b, relationship_type, source_case, confidence
**Rationale:** A dedicated edge table enables graph analytics and visualization of connections between persons across different cases.
**Stakeholder:** STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-009, DR-002
**Security/Privacy Implications:** Relationship data can reveal sensitive associations; access must be role-controlled.
**Source:** 01_Blueprint §6.4
**Acceptance Criteria:**
- Given two PersonEntity records identified as connected, when the relationship is recorded, then a RelationshipEdge row is created with both entities, relationship type, source case, and confidence.
**Verification Method:** Test
**Demo Evidence:** Relationship edge table viewer showing connections

#### FR-017: Graph Traversal

**Description:** System shall support degree centrality and shortest-path traversal over RelationshipEdge
**Rationale:** Analysts need to identify highly connected individuals (degree centrality) and connection paths between persons for investigative leads.
**Stakeholder:** STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-016
**Security/Privacy Implications:** Graph traversal results may reveal unexpected connections; results must respect role-based access.
**Source:** 01_Blueprint §8.3
**Acceptance Criteria:**
- Given a populated RelationshipEdge graph, when an analyst queries degree centrality for a person, then the system returns the count of direct connections; when querying shortest path between two persons, then the system returns the minimal connection chain.
**Verification Method:** Test
**Demo Evidence:** Graph analytics panel showing centrality scores and path visualization

#### FR-018: Graph Visualization

**Description:** System shall render a force-directed node-link graph in the browser
**Rationale:** Visual graph representation is more intuitive than tabular data for understanding complex relationship networks.
**Stakeholder:** STK-001:Investigating Officer / STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-017
**Security/Privacy Implications:** Visualization must not display protected attributes; node labels must respect access controls.
**Source:** 01_Blueprint §11
**Acceptance Criteria:**
- Given a set of related PersonEntity records, when an analyst opens the graph view, then a force-directed node-link diagram is rendered with interactive pan, zoom, and node selection.
**Verification Method:** Demonstration
**Demo Evidence:** Interactive graph visualization in browser with clickable nodes

#### FR-019: Vehicle Linking

**Description:** System shall maintain vehicle-to-case links via VehicleLink table
**Rationale:** Vehicles are key entities in many crimes; tracking vehicle involvement across cases enables identification of repeat vehicle usage patterns.
**Stakeholder:** STK-001:Investigating Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-005, DR-002
**Security/Privacy Implications:** Vehicle registration data may contain owner PII; access must be scoped.
**Source:** 01_Blueprint §6.4
**Acceptance Criteria:**
- Given a vehicle registration number extracted from a case, when the system processes it, then a VehicleLink record associates the vehicle with the case in the VehicleLink table.
**Verification Method:** Test
**Demo Evidence:** Vehicle detail page showing linked cases timeline

#### FR-020: MO Pattern Matching

**Description:** System shall flag incidents sharing similar modus operandi via embedding similarity
**Rationale:** Recognizing MO patterns across cases helps identify serial offenders and connect seemingly unrelated incidents.
**Stakeholder:** STK-003:SCRB Analyst
**Priority:** SHOULD
**Scope:** STRETCH
**Dependencies:** AIR-009
**Security/Privacy Implications:** MO embeddings derived from narrative text may inadvertently encode sensitive information.
**Source:** 01_Blueprint §8.4
**Acceptance Criteria:**
- Given a set of incident narratives encoded as embeddings, when the MO matching algorithm runs, then incidents with cosine similarity above a threshold are flagged as related.
**Verification Method:** Test
**Demo Evidence:** MO pattern view showing clustered incidents with similarity scores

### 1.5 Geospatial Analytics

#### FR-021: Hotspot Map

**Description:** System shall render a hexbin/heatmap layer from Incident latitude/longitude
**Rationale:** Visual hotspot identification enables rapid understanding of crime concentration areas for resource deployment and preventive patrol.
**Stakeholder:** STK-003:SCRB Analyst / STK-004:Senior Police Official
**Priority:** MUST
**Scope:** MVP
**Dependencies:** DR-005
**Security/Privacy Implications:** Hotspot maps display aggregate data only; no individual incident locations should be identifiable at low zoom levels.
**Source:** 01_Blueprint §8.6
**Acceptance Criteria:**
- Given incident data with valid lat/lng coordinates, when an analyst loads the geospatial view, then a hexbin/heatmap overlay is rendered on the map showing crime density.
**Verification Method:** Demonstration
**Demo Evidence:** Map view with hexbin overlay colored by incident density

#### FR-022: District Drill-Down

**Description:** System shall support drill-down from state → district → station jurisdiction
**Rationale:** Analysts need to navigate geographic hierarchies to compare crime patterns at different administrative levels.
**Stakeholder:** STK-003:SCRB Analyst / STK-004:Senior Police Official
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-021
**Security/Privacy Implications:** Drill-down to station level may reveal sensitive local crime data; access must respect jurisdiction scoping.
**Source:** 01_Blueprint §8.6
**Acceptance Criteria:**
- Given the geospatial view at state level, when the analyst clicks on a district, then the map zooms to show district-level data; subsequent click on a station shows station-jurisdiction data.
**Verification Method:** Demonstration
**Demo Evidence:** Map demonstrating click-through from state to district to station

#### FR-023: Temporal Filter

**Description:** System shall support filtering by date range, crime type, and jurisdiction
**Rationale:** Crime patterns vary by time, type, and location; interactive filters let analysts isolate specific subsets for targeted analysis.
**Stakeholder:** STK-001:Investigating Officer / STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-021, FR-022
**Security/Privacy Implications:** Filter controls must respect user role permissions; jurisdiction filter should only show authorized areas.
**Source:** 01_Blueprint §4.1
**Acceptance Criteria:**
- Given the geospatial view with filters visible, when the analyst selects a date range, crime type, and jurisdiction, then the map and charts update to show only matching incidents.
**Verification Method:** Demonstration
**Demo Evidence:** Map view with filter controls demonstrating real-time data filtering

#### FR-024: Anomaly Detection

**Description:** System shall detect z-score deviations in rolling (district, crime_type, week) counts vs. historical baseline
**Rationale:** Automated anomaly detection alerts analysts to statistically significant crime spikes without manual monitoring of every metric.
**Stakeholder:** STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** AIR-004
**Security/Privacy Implications:** Anomaly alerts may trigger investigative actions; false positive rates must be monitored to avoid alert fatigue.
**Source:** 01_Blueprint §8.7
**Acceptance Criteria:**
- Given a rolling 4-week window of crime counts by district and crime type, when the current week's count exceeds the baseline mean by 2+ standard deviations, then the system flags it as an anomaly.
**Verification Method:** Test
**Demo Evidence:** Anomaly alert list showing flagged deviations with z-score magnitude

#### FR-025: Anomaly Alert

**Description:** System shall create alert records for detected anomalies with deviation magnitude
**Rationale:** Persistent alert records enable tracking of anomaly history, trend analysis, and accountability for follow-up actions.
**Stakeholder:** STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-024
**Security/Privacy Implications:** Alert data may trigger operational decisions; alert creation must be audited.
**Source:** 01_Blueprint §8.7
**Acceptance Criteria:**
- Given a detected anomaly, when the alert creation process runs, then an alert record is persisted with district, crime type, week, deviation magnitude, and timestamp.
**Verification Method:** Test
**Demo Evidence:** Alert history table showing recorded anomalies with deviation values

### 1.6 Risk Scoring

#### FR-026: Risk Score Computation

**Description:** System shall compute a repeat-offender risk score per PersonEntity using QuickML AutoML
**Rationale:** Objective risk scores help analysts prioritize high-risk individuals for attention, replacing subjective judgment with data-driven assessment.
**Stakeholder:** STK-003:SCRB Analyst / STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** AIR-002, FR-009
**Security/Privacy Implications:** Risk scores must not use protected attributes (caste, religion); scores should be presented with uncertainty bounds.
**Source:** 01_Blueprint §8.5
**Acceptance Criteria:**
- Given a PersonEntity with associated case history, when the risk scoring pipeline runs, then a risk score (0–100) is computed and stored in the RiskScore table.
**Verification Method:** Test
**Demo Evidence:** PersonEntity detail page showing computed risk score with trend

#### FR-027: Feature Importance

**Description:** Every risk score shall include a JSON feature-importance breakdown
**Rationale:** Transparency into which features drive a risk score is required for fairness auditing and for investigators to understand score rationale.
**Stakeholder:** STK-003:SCRB Analyst / STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-026, AIR-006
**Security/Privacy Implications:** Feature importance may reveal proxy variables for protected attributes; must be reviewed in fairness checks.
**Source:** 01_Blueprint §8.5
**Acceptance Criteria:**
- Given a computed risk score, when the score record is retrieved, then it includes a JSON feature_importance map listing each feature and its contribution.
**Verification Method:** Test
**Demo Evidence:** Risk score detail view showing feature importance bar chart

#### FR-028: Feature Exclusion

**Description:** CasteID, ReligionID, and any identity-proxy variables shall be hard-excluded from the feature set
**Rationale:** Using caste or religion in risk scoring is legally and ethically prohibited in Indian law; hard exclusion prevents inadvertent inclusion.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-026, AIR-007
**Security/Privacy Implications:** Direct implementation of ethical AI requirements; exclusion must be verified by automated fairness checks.
**Source:** 01_Blueprint §6.2
**Acceptance Criteria:**
- Given the feature set configured for the risk model, when the model is trained, then CasteID, ReligionID, and any configured proxy variables are absent from the feature set.
**Verification Method:** Review
**Demo Evidence:** Fairness dashboard showing excluded variable verification

#### FR-029: Score Explainability

**Description:** Feature-importance breakdown shall be visible in the Investigator Console
**Rationale:** Front-line investigators need to understand why a score was assigned so they can make informed decisions about investigative priority.
**Stakeholder:** STK-001:Investigating Officer / STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-027
**Security/Privacy Implications:** N/A
**Source:** 01_Blueprint §8.5
**Acceptance Criteria:**
- Given a PersonEntity with a risk score, when an Investigator views the person detail in the console, then a feature importance breakdown is displayed alongside the score.
**Verification Method:** Demonstration
**Demo Evidence:** Investigator Console showing risk score card with feature importance bars

### 1.7 Natural Language Query

#### FR-030: RAG Query

**Description:** System shall accept plain-English questions and return grounded, cited answers over the case corpus
**Rationale:** Investigators and analysts may not be proficient in query languages; natural language access to case data lowers the barrier to information retrieval.
**Stakeholder:** STK-001:Investigating Officer / STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** AIR-005
**Security/Privacy Implications:** RAG pipeline must respect RBAC; answers must not include data the user is not authorized to see.
**Source:** 01_Blueprint §8.9
**Acceptance Criteria:**
- Given an authorized user submits a plain-English question about case data, when the RAG pipeline processes it, then the system returns a natural-language answer with citations to source documents.
**Verification Method:** Demonstration
**Demo Evidence:** NLQ interface showing question input and cited answer output

#### FR-031: Source Citations

**Description:** Every answer shall cite the source document(s) it was derived from
**Rationale:** Citations enable verification and build trust in AI-generated answers; uncited answers cannot be validated.
**Stakeholder:** STK-001:Investigating Officer / STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-030
**Security/Privacy Implications:** Citations must respect RBAC; restricted documents must not be cited to unauthorized users.
**Source:** 01_Blueprint §8.9
**Acceptance Criteria:**
- Given a RAG-generated answer, when the answer is displayed, then each claim in the answer includes a reference to the source CaseMaster ID or document.
**Verification Method:** Demonstration
**Demo Evidence:** Answer panel showing clickable citation links to source cases

#### FR-032: Role-Based Filtering

**Description:** RAG retrieval shall respect role-based access controls (do not return restricted data)
**Rationale:** Preventing unauthorized data exposure is a legal requirement; RAG must not bypass existing access controls.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-030, FR-036
**Security/Privacy Implications:** Core security control; failure could result in PII exposure to unauthorized roles.
**Source:** 01_Blueprint §8.9
**Acceptance Criteria:**
- Given a user with Investigator role, when they query for data restricted to Compliance role only, then the RAG system returns "Insufficient evidence" without exposing restricted data.
**Verification Method:** Test
**Demo Evidence:** Role-switching test showing different query results per role

#### FR-033: Insufficient Evidence Response

**Description:** When evidence is insufficient, the system shall state "Insufficient evidence" rather than hallucinate
**Rationale:** Hallucinated answers in law enforcement contexts could lead to wrongful investigative actions; strict refusal to answer without evidence prevents harm.
**Stakeholder:** STK-001:Investigating Officer / STK-003:SCRB Analyst
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-030
**Security/Privacy Implications:** Prevention of AI hallucination is a safety requirement in the criminal justice context.
**Source:** 01_Blueprint §8.9
**Acceptance Criteria:**
- Given a user query for which the case corpus contains no relevant evidence, when the RAG pipeline processes it, then the response states "Insufficient evidence" without fabricating information.
**Verification Method:** Test
**Demo Evidence:** NLQ interface showing "Insufficient evidence" response for out-of-scope query

#### FR-034: Query Audit

**Description:** Every RAG query and answer shall be logged in the AuditLog
**Rationale:** Auditability of AI queries is required for accountability, misuse detection, and compliance with data governance policies.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-030, FR-042
**Security/Privacy Implications:** Audit logs themselves contain query text which may include sensitive information; logs must be append-only and access-controlled.
**Source:** 01_Blueprint §8.9
**Acceptance Criteria:**
- Given a user submits a RAG query and receives an answer, when the AuditLog is queried, then an entry exists with the query text, answer summary, user ID, and timestamp.
**Verification Method:** Test
**Demo Evidence:** AuditLog search showing RAG query entries with user and timestamp

### 1.8 Authentication & Authorization

#### FR-035: User Authentication

**Description:** System shall authenticate users via Catalyst Authentication
**Rationale:** Catalyst Authentication provides a managed, enterprise-grade identity service that integrates with existing Zoho ecosystem credentials.
**Stakeholder:** STK-013:System Admin
**Priority:** MUST
**Scope:** MVP
**Dependencies:** Catalyst platform configuration
**Security/Privacy Implications:** Primary authentication gateway; must enforce password policies, session management, and MFA integration.
**Source:** 01_Blueprint §12.1
**Acceptance Criteria:**
- Given a registered user with valid credentials, when they attempt to log in, then they are authenticated via Catalyst and granted a session token.
**Verification Method:** Test
**Demo Evidence:** Login page showing Catalyst authentication flow

#### FR-036: Role-Based Access

**Description:** System shall enforce RBAC with at least 3 roles: Investigator, SCRB Analyst, Compliance Officer
**Rationale:** Different users require different data access levels; RBAC ensures least-privilege access and supports audit accountability.
**Stakeholder:** STK-012:Compliance Officer / STK-013:System Admin
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-035
**Security/Privacy Implications:** Core authorization control; all data access decisions must route through RBAC enforcement.
**Source:** 01_Blueprint §12.1
**Acceptance Criteria:**
- Given a user with Investigator role, when they attempt to access Compliance-only data, then the system denies access with an authorization error.
**Verification Method:** Test
**Demo Evidence:** User management screen showing role assignment and permission matrix

#### FR-037: Jurisdiction Scoping

**Description:** Investigator role shall be scoped to their assigned district/station records
**Rationale:** Investigators should only access cases within their jurisdiction to maintain data separation and operational boundaries.
**Stakeholder:** STK-001:Investigating Officer / STK-013:System Admin
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-036
**Security/Privacy Implications:** Prevents unauthorized cross-jurisdiction data access; critical for data privacy compliance.
**Source:** 01_Blueprint §12.1
**Acceptance Criteria:**
- Given an Investigator assigned to District A, when they search for cases, then only cases from District A are returned; cases from District B are invisible.
**Verification Method:** Test
**Demo Evidence:** Two Investigator logins showing different case lists based on jurisdiction

#### FR-038: MFA Support

**Description:** MFA shall be required for accounts accessing person-level records
**Rationale:** Person-level records contain sensitive PII requiring elevated authentication assurance to prevent unauthorized access.
**Stakeholder:** STK-012:Compliance Officer / STK-013:System Admin
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-035
**Security/Privacy Implications:** MFA provides defense against credential compromise for sensitive data access.
**Source:** 01_Blueprint §12.1
**Acceptance Criteria:**
- Given a user with access to person-level records, when they attempt to view a person record, then they are prompted for MFA if not already authenticated with MFA in the current session.
**Verification Method:** Test
**Demo Evidence:** MFA challenge screen appearing when accessing person record detail

### 1.9 Audit Logging

#### FR-039: Person-Level Read Audit

**Description:** Every read of a person-level record shall write to AuditLog
**Rationale:** Tracking who accessed personal data is a legal requirement under Indian privacy frameworks and essential for misuse investigation.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-042, DR-002
**Security/Privacy Implications:** Core privacy control; enables detection of unauthorized data access patterns.
**Source:** 01_Blueprint §12.3
**Acceptance Criteria:**
- Given a user views a person-level record, when the record is displayed, then an AuditLog entry is created with user ID, record ID, action type "READ", and timestamp.
**Verification Method:** Test
**Demo Evidence:** Audit log viewer showing person-level read events with user details

#### FR-040: AI Output Audit

**Description:** Every AI-assisted recommendation surfaced to a human shall write to AuditLog
**Rationale:** AI recommendations influence investigative decisions; full audit trail is required for accountability and bias detection.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-042
**Security/Privacy Implications:** Enables post-hoc review of AI-driven decisions for fairness and correctness.
**Source:** 01_Blueprint §12.3
**Acceptance Criteria:**
- Given an AI recommendation (risk score, entity match, anomaly alert) is displayed to a user, when the display occurs, then an AuditLog entry records the recommendation type, content summary, and user context.
**Verification Method:** Test
**Demo Evidence:** Audit log entries showing AI recommendation events with details

#### FR-041: Append-Only Log

**Description:** AuditLog shall be append-only at the application layer
**Rationale:** Tamper-proof audit trails are required for evidentiary integrity and regulatory compliance; logs must not be modifiable or deletable.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-039, DR-002
**Security/Privacy Implications:** Foundational security control; prevents evidence tampering and supports forensic investigation.
**Source:** 01_Blueprint §12.3
**Acceptance Criteria:**
- Given an AuditLog entry exists, when any user attempts to modify or delete the entry through the application, then the operation is rejected with an error.
**Verification Method:** Test
**Demo Evidence:** AuditLog showing error when attempting to delete or edit an entry

#### FR-042: Audit Queryability

**Description:** Governance Officer shall be able to search and filter AuditLog
**Rationale:** Audit logs are only useful if they can be efficiently searched; governance officers need filtering by user, date range, action type, and target record.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-041, DR-003
**Security/Privacy Implications:** Audit log search must itself be audited and restricted to authorized roles.
**Source:** 01_Blueprint §12.3
**Acceptance Criteria:**
- Given a populated AuditLog, when a Governance Officer searches by user ID and date range, then matching audit entries are returned with pagination.
**Verification Method:** Demonstration
**Demo Evidence:** Audit search interface showing filters and results table

### 1.10 Governance

#### FR-043: Fairness Check

**Description:** System shall verify that CasteID/ReligionID do not appear in any RiskScore.feature_importance
**Rationale:** Proactive fairness verification ensures that protected attributes have not inadvertently influenced risk scores due to data leakage or proxy variables.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-027, FR-028
**Security/Privacy Implications:** Direct compliance with ethical AI requirements; results feed into governance reporting.
**Source:** 01_Blueprint §8.13
**Acceptance Criteria:**
- Given a computed RiskScore with feature_importance JSON, when the fairness check runs, then it asserts that neither CasteID, ReligionID, nor any proxy variable appears in the feature_importance keys.
**Verification Method:** Test
**Demo Evidence:** Fairness dashboard showing pass/fail status for each risk score

#### FR-044: Role Restriction Check

**Description:** System shall verify that general dashboard roles cannot query CasteID/ReligionID columns
**Rationale:** Caste and religion data require elevated handling; access must be restricted to Compliance role per governance policy.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-036
**Security/Privacy Implications:** Enforces data minimization and access control for sensitive demographic attributes.
**Source:** 01_Blueprint §6.2
**Acceptance Criteria:**
- Given a user with Investigator or SCRB Analyst role, when they attempt to query CasteID or ReligionID columns, then the system returns a column-access-denied error.
**Verification Method:** Test
**Demo Evidence:** Role-switching demonstration showing blocked access vs. permitted access

#### FR-045: Fairness Dashboard

**Description:** Governance Officer shall have a dashboard showing fairness check results
**Rationale:** A dedicated dashboard gives compliance officers visibility into ongoing fairness metrics, enabling timely intervention if issues arise.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-043, FR-044
**Security/Privacy Implications:** Dashboard itself must only be accessible to Compliance role.
**Source:** 01_Blueprint §11.1
**Acceptance Criteria:**
- Given fairness check results exist, when a Governance Officer opens the Fairness Dashboard, then it displays pass/fail status, recent check history, and any violations detected.
**Verification Method:** Demonstration
**Demo Evidence:** Fairness Dashboard view with charts and pass/fail indicators

### 1.11 Synthetic Data

#### FR-046: Synthetic Data Generation

**Description:** System shall support generating 2000+ synthetic FIR records using Faker (en_IN)
**Rationale:** Synthetic data enables development, testing, and demo without exposing real PII; 2000+ records provide sufficient volume for meaningful analytics testing.
**Stakeholder:** STK-013:System Admin
**Priority:** MUST
**Scope:** MVP
**Dependencies:** Python Faker library (en_IN locale)
**Security/Privacy Implications:** Synthetic data must be clearly distinguishable from real data to prevent confusion in production environments.
**Source:** 01_Blueprint §6.7
**Acceptance Criteria:**
- Given the synthetic data generator is invoked with a seed, when generation completes, then at least 2000 FIR records are created with realistic Indian names, addresses, and crime types.
**Verification Method:** Test
**Demo Evidence:** Synthetic data generation script output showing record count

#### FR-047: Planted Patterns

**Description:** Synthetic data shall include deliberately planted patterns: repeat-offender, shared-vehicle, hotspot week
**Rationale:** Planted patterns allow test scenarios to verify that analytics features (entity resolution, vehicle linking, hotspot detection) produce correct results against known ground truth.
**Stakeholder:** STK-013:System Admin
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-046
**Security/Privacy Implications:** N/A
**Source:** 01_Blueprint §6.7
**Acceptance Criteria:**
- Given the synthetic dataset, when analyzed for repeat offenders, then pre-configured repeat-offender patterns are detectable; when analyzed for shared vehicles, then pre-configured vehicle-sharing patterns are present.
**Verification Method:** Test
**Demo Evidence:** Pattern detection results matching planted ground truth

#### FR-048: Seeded Reproducibility

**Description:** Synthetic data generation shall use a seeded RNG for reproducibility
**Rationale:** Reproducible synthetic datasets are essential for regression testing, debugging, and comparing results across development iterations.
**Stakeholder:** STK-013:System Admin
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-046
**Security/Privacy Implications:** N/A
**Source:** 01_Blueprint §6.7
**Acceptance Criteria:**
- Given the generator is run twice with the same seed, when both runs complete, then the resulting datasets are identical.
**Verification Method:** Test
**Demo Evidence:** Diff comparison showing identical outputs from two seeded runs

#### FR-049: Synthetic Labeling

**Description:** Every synthetic record shall be clearly labeled as synthetic
**Rationale:** Unlabeled synthetic data could be mistaken for real records, leading to erroneous analysis conclusions or privacy concerns.
**Stakeholder:** STK-012:Compliance Officer
**Priority:** MUST
**Scope:** MVP
**Dependencies:** FR-046
**Security/Privacy Implications:** Critical for preventing confusion between synthetic and real PII; supports demo environments.
**Source:** 01_Blueprint §6.7
**Acceptance Criteria:**
- Given a synthetic record in any query result or view, when the record is displayed, then it includes a visible "SYNTHETIC" label or badge.
**Verification Method:** Review
**Demo Evidence:** Synthetic record card showing "SYNTHETIC" badge in UI

---

## 2. Data Requirements

| ID | Title | Description | Priority | Scope | Rationale | Stakeholder | Demo Evidence |
|----|-------|-------------|----------|-------|-----------|-------------|--------------|
| DR-001 | Source Schema Migration | All 27+ source tables from the FIR ERD shall be migrated to Catalyst Data Store | MUST | MVP | All 27+ source tables must be migrated to enable querying and analytics on the Catalyst platform | STK-013:System Admin | Catalyst Data Store browser showing all 27+ tables |
| DR-002 | Berunda Extension Tables | PersonEntity, PersonEntityLink, RelationshipEdge, RiskScore, AuditLog tables shall be created | MUST | MVP | Core analytics tables (PersonEntity, RelationshipEdge, etc.) are foundational for entity resolution and graph features | STK-013:System Admin | Schema viewer showing extension tables with indexes |
| DR-003 | Indexes | Composite indexes shall be created on CaseMaster(CrimeMajorHeadID, CrimeRegisteredDate, PoliceStationID) | MUST | MVP | Composite indexes on frequently queried columns are essential for query performance at scale | STK-013:System Admin | Query execution plan showing index usage |
| DR-004 | CasteID Not Indexed | ComplainantDetails.CasteID and ReligionID shall NOT be indexed for general search | MUST | MVP | Preventing indexing on caste/religion columns reduces the risk of these attributes being used in searches or model features | STK-012:Compliance Officer | Index list confirming CasteID/ReligionID are not indexed |
| DR-005 | CrimeNo Parsing | District/station/year components embedded in CrimeNo shall be parsed at ingestion time | MUST | MVP | CrimeNo encodes district/station/year; parsing these components at ingestion enables geospatial and temporal aggregation without additional lookups | STK-001:Investigating Officer | Parsed CrimeNo components visible in case detail |
| DR-006 | Full-Text Index | Full-text index on Inv_OccuranceTime.BriefFacts | MUST | MVP | BriefFacts contains the narrative; full-text indexing enables keyword search across case narratives | STK-001:Investigating Officer | Full-text search results across narratives |
| DR-007 | Schema Separation | Source tables and Berunda extension tables shall be in separate logical schemas/namespaces | MUST | MVP | Logical separation of source tables from Berunda extension tables prevents accidental cross-schema dependencies and simplifies data lifecycle management | STK-013:System Admin | Schema browser showing two separate namespaces |

## 3. AI Requirements

| ID | Title | Description | Priority | Scope | Rationale | Stakeholder | Demo Evidence |
|----|-------|-------------|----------|-------|-----------|-------------|--------------|
| AIR-001 | NER Pipeline | English NER using spaCy pipeline deployed as a Catalyst Function | MUST | MVP | spaCy provides production-grade NER suitable for English FIR narratives | STK-001:Investigating Officer | NER pipeline invocation showing extracted entities |
| AIR-002 | Risk Scoring Model | Gradient-boosted trees via QuickML AutoML for risk scoring | MUST | MVP | Gradient-boosted trees offer state-of-the-art tabular data performance with built-in feature importance | STK-003:SCRB Analyst | Model training run showing feature importance chart |
| AIR-003 | Hotspot Detection | KDE/hexbin aggregation for hotspot detection | MUST | MVP | KDE/hexbin aggregation is a standard, interpretable method for crime hotspot identification | STK-003:SCRB Analyst | Map rendering with hexbin overlay |
| AIR-004 | Anomaly Detection | Z-score deviation from rolling baseline for anomaly detection | MUST | MVP | Z-score deviation is a simple yet effective statistical method for detecting crime count anomalies | STK-003:SCRB Analyst | Anomaly detection results with deviation values |
| AIR-005 | RAG Foundation | QuickML LLM serving + RAG over curated case corpus | MUST | MVP | RAG with curated corpus enables grounded question answering over case data without model hallucination | STK-001:Investigating Officer | RAG query returning cited answer |
| AIR-006 | Feature Importance | All model outputs include feature-importance via QuickML native capability | MUST | MVP | QuickML native feature importance provides model transparency without custom implementation | STK-012:Compliance Officer | Feature importance bar chart per model output |
| AIR-007 | Fairness Auditing | Rule-based parity check for feature exclusion | MUST | MVP | Rule-based parity check ensures protected attribute exclusion is enforced | STK-012:Compliance Officer | Fairness check report showing pass status |
| AIR-008 | Kannada NER | AI4Bharat/IndicNLP model for Kannada NER | SHOULD | STRETCH | AI4Bharat/IndicNLP provides pre-trained Indic language models suitable for Kannada | STK-001:Investigating Officer | Kannada FIR narrative with extracted entities |
| AIR-009 | MO Embeddings | Sentence-transformer embedding similarity for MO matching | SHOULD | STRETCH | Sentence-transformer embeddings capture semantic similarity between narrative texts for MO matching | STK-003:SCRB Analyst | MO similarity scores between case pairs |
| AIR-010 | Drift Monitoring | Scheduled re-evaluation of model performance against held-out window | SHOULD | STRETCH | Model performance degrades over time; scheduled re-evaluation against held-out data detects drift early | STK-013:System Admin | Drift monitoring dashboard showing performance trends |
| AIR-011 | Bias Proxy Check | Automated check that no excluded variable proxies appear in feature sets | SHOULD | STRETCH | Automated proxy detection prevents indirect use of protected attributes via correlated features | STK-012:Compliance Officer | Proxy check report listing detected and cleared features |
| AIR-012 | No Criminality Prediction | System shall NOT predict individual criminality or likelihood of future offending | MUST | MVP | Predicting individual criminality is ethically prohibited and legally risky; the system limits itself to repeat-offender risk assessment | STK-012:Compliance Officer | Model card documentation confirming no criminality prediction |
| AIR-013 | Advisory Only | Every AI output shall be labeled as advisory, not automated | MUST | MVP | AI outputs must not be presented as automated decisions; advisory labeling maintains human accountability | STK-012:Compliance Officer | UI screenshot with "Advisory" label on AI output |
| AIR-014 | Human-in-the-Loop | No AI output shall trigger an automatic enforcement action | MUST | MVP | Preventing automatic enforcement actions from AI outputs preserves human oversight and legal accountability | STK-012:Compliance Officer | Process flow diagram showing human approval step |
| AIR-015 | Confidence Display | Every AI output shall display confidence or uncertainty | MUST | MVP | Displaying uncertainty prevents over-reliance on AI outputs and supports informed decision-making | STK-001:Investigating Officer | AI output with confidence indicator visible |

## 4. Security Requirements

| ID | Title | Description | Priority | Scope | Rationale | Stakeholder | Demo Evidence |
|----|-------|-------------|----------|-------|-----------|-------------|--------------|
| SEC-001 | Encryption at Rest | All data in Data Store, NoSQL, and Stratus shall be encrypted at rest | MUST | MVP | Data at rest encryption is a baseline security requirement for any system handling sensitive law enforcement data | STK-013:System Admin | Catalyst console showing encryption-enabled status |
| SEC-002 | Encryption in Transit | All communication shall use TLS, enforced at API Gateway | MUST | MVP | TLS ensures data confidentiality and integrity during transmission, preventing interception | STK-013:System Admin | Network traffic capture showing TLS handshake |
| SEC-003 | API Gateway | All API calls shall route through Catalyst API Gateway for auth and throttling | MUST | MVP | Centralized API gateway provides consistent authentication, authorization, and throttling for all service endpoints | STK-013:System Admin | API Gateway dashboard showing routing and throttling rules |
| SEC-004 | Input Validation | All user inputs shall be validated and sanitized against injection attacks | MUST | MVP | Input validation is the primary defense against injection attacks that could compromise data integrity | STK-013:System Admin | Penetration test report showing validation effectiveness |
| SEC-005 | Parameterized Queries | All database queries shall use parameterized bindings (no string concatenation) | MUST | MVP | Parameterized queries prevent SQL injection by separating query structure from data | STK-013:System Admin | Code review showing parameterized query usage |
| SEC-006 | Secrets Management | API keys and credentials shall be stored in Catalyst secrets management, not code | MUST | MVP | Hardcoded credentials are a common vulnerability; Catalyst secrets management provides secure, auditable credential storage | STK-013:System Admin | Secrets management console showing stored keys (masked) |
| SEC-007 | CasteID Role Restriction | CasteID/ReligionID columns accessible only to Compliance role | MUST | MVP | Caste/religion data access must be restricted to Compliance role to prevent misuse | STK-012:Compliance Officer | Access test showing Compliance-only access |
| SEC-008 | Rate Limiting | API Gateway rate limiting to prevent abuse | MUST | MVP | Rate limiting prevents API abuse, brute-force attacks, and resource exhaustion | STK-013:System Admin | Rate limit configuration in API Gateway |
| SEC-009 | Session Management | Authenticated sessions with timeout and secure cookie handling | MUST | MVP | Secure session handling prevents session hijacking and unauthorized access | STK-013:System Admin | Session timeout test showing automatic logout |

## 5. Privacy Requirements

| ID | Title | Description | Priority | Scope | Rationale | Stakeholder | Demo Evidence |
|----|-------|-------------|----------|-------|-----------|-------------|--------------|
| PRIV-001 | No Real PII in Demo | Only synthetic person-level data in demo; no real victim/accused/witness data | MUST | MVP | Using real victim/accused/witness data in demos would violate privacy; synthetic-only demos prevent any PII exposure | STK-012:Compliance Officer | Demo environment data audit confirming zero real PII |
| PRIV-002 | Synthetic Labeling | All synthetic person records shall be clearly and persistently labeled | MUST | MVP | Clear labeling prevents any person from being mistaken for a real individual with legal consequences | STK-012:Compliance Officer | Synthetic record showing persistent "SYNTHETIC" label |
| PRIV-003 | Data Minimization | Only data required for named features shall be collected | MUST | MVP | Collecting only necessary data reduces privacy risk and simplifies compliance with data protection principles | STK-012:Compliance Officer | Data dictionary showing purpose for each collected field |
| PRIV-004 | Caste/Religion Governance | CasteID/ReligionID never in model features; aggregate reporting only | MUST | MVP | Caste and religion data require special governance; the system ensures they are never used in models and only appear in aggregate reports | STK-012:Compliance Officer | Aggregate report showing caste/religion stats without individual identification |
| PRIV-005 | Audit Proportionality | Audit logs capture who/what/when/why, not full record contents | MUST | MVP | Logging full record contents would itself create privacy risk; logs capture metadata sufficient for investigation without exposing data | STK-012:Compliance Officer | Sample audit log entry showing metadata pattern without full record content |
