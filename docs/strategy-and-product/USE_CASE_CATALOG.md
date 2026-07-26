# Use Case Catalog

[//]: # (Document ID: BERUNDA-UC-001 | Version: 1.0 | Status: DRAFT | Classification: PUBLIC | Owner: Berunda Team | Audience: Team | Source: 01_Enterprise_Blueprint | Last Verified: 2026-07-17 | Review: Monthly)

---

## Use Case Index

| UC-ID | Use Case | Primary Actor | Priority | Scope |
|-------|----------|--------------|----------|-------|
| UC-001 | Ingest FIR from structured source | System (batch) | MUST | MVP |
| UC-002 | Extract entities from FIR narrative | System (NER) | MUST | MVP |
| UC-003 | Resolve person identity across cases | System (entity resolution) | MUST | MVP |
| UC-004 | View relationship graph for a person | IO | MUST | MVP |
| UC-005 | Discover hidden links between cases | IO | MUST | MVP |
| UC-006 | View geospatial hotspot map | SHO / SCRB | MUST | MVP |
| UC-007 | Analyze temporal crime patterns | SCRB | MUST | MVP |
| UC-008 | Compute explainable risk score | System (AutoML) | MUST | MVP |
| UC-009 | Detect anomalous crime spikes | System (statistical) | MUST | MVP |
| UC-010 | Ask natural-language investigation question | IO / SHO | MUST | MVP |
| UC-011 | Authenticate and authorize user | All users | MUST | MVP |
| UC-012 | Audit sensitive data access | System | MUST | MVP |
| UC-013 | Verify fairness and bias controls | Governance Officer | MUST | MVP |
| UC-014 | Generate statutory SC/ST aggregate report | Governance Officer | SHOULD | STRETCH |
| UC-015 | View state-level command dashboard | SCRB / DGP | MUST | MVP |
| UC-016 | Review and Approve AI Suggestions | IO / SHO | MUST | MVP |

## Detailed Use Cases

### UC-001: Ingest FIR from Structured Source

| Field | Value |
|-------|-------|
| **Primary Actor** | System (batch ingestion pipeline) |
| **Description** | Import FIR/incident records from structured Excel/CSV into the Data Store schema |
| **Trigger** | Upload event or scheduled import |
| **Preconditions** | Catalyst Data Store schema is migrated; source file passes validation |
| **Postconditions** | FIR record exists in CaseMaster with linked Accused/Victim/Complainant records |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-002: Extract Entities from FIR Narrative

| Field | Value |
|-------|-------|
| **Primary Actor** | System (NER pipeline) |
| **Description** | Automatically extract person names, locations, vehicle references, and organizations from English FIR narrative text |
| **Trigger** | New FIR ingested; BriefFacts text available |
| **Preconditions** | English NER model (spaCy) deployed as Catalyst Function |
| **Postconditions** | Extracted entities scored, linked to case, written to PersonEntityLink and VehicleLink |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-003: Resolve Person Identity Across Cases

| Field | Value |
|-------|-------|
| **Primary Actor** | System (entity resolution engine) |
| **Description** | Match newly extracted or imported person records against existing PersonEntity table using name similarity, age band, and address overlap |
| **Trigger** | New person record arrives (via NER, import, or manual entry) |
| **Preconditions** | PersonEntity and PersonEntityLink tables exist; blocking + similarity function deployed |
| **Postconditions** | Record linked to existing PersonEntity or creates new entity; confidence score recorded |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-004: View Relationship Graph for a Person

| Field | Value |
|-------|-------|
| **Primary Actor** | Investigating Officer |
| **Description** | Click on a person entity to see a force-directed graph showing linked cases, co-accused, victims, vehicles, and locations |
| **Preconditions** | RelationshipEdge and VehicleLink tables populated; PersonEntity exists |
| **Postconditions** | Graph rendered with edge thickness proportional to confidence |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-005: Discover Hidden Links Between Cases

| Field | Value |
|-------|-------|
| **Primary Actor** | Investigating Officer |
| **Description** | Traverse graph from a seed entity to surface connections across cases that would not be visible in isolated record views |
| **Preconditions** | Link analysis agent populated with entity-resolution output |
| **Postconditions** | Path between two entities displayed with intermediate hops and case references |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-006: View Geospatial Hotspot Map

| Field | Value |
|-------|-------|
| **Primary Actor** | SHO / SCRB Analyst |
| **Description** | View a heatmap/hexbin layer over Karnataka showing incident density, with drill-down from state → district → station jurisdiction |
| **Preconditions** | Inv_OccuranceTime latitude/longitude populated; KDE or hexbin aggregation computed |
| **Postconditions** | Hotspot layer rendered with time-of-day and crime-type filters |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-007: Analyze Temporal Crime Patterns

| Field | Value |
|-------|-------|
| **Primary Actor** | SCRB Analyst |
| **Description** | Filter crime incidents by date range, crime type, district, and station; view trend charts and distribution breakdowns |
| **Preconditions** | CaseMaster and CrimeHead/CrimeSubHead tables populated |
| **Postconditions** | Dashboard shows filtered results with visualizations |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-008: Compute Explainable Risk Score

| Field | Value |
|-------|-------|
| **Primary Actor** | System (QuickML AutoML) |
| **Description** | Compute a repeat-offender risk score per PersonEntity based on prior case count, recency, offense-type diversity, resolution outcomes. Score ships with feature-importance breakdown. |
| **Preconditions** | PersonEntity linked to case history; QuickML AutoML model trained on synthetic data |
| **Hard Constraint** | CasteID/ReligionID and any proxy variables EXCLUDED from feature set |
| **Postconditions** | RiskScore record created with value, computed_at, feature_importance JSON |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-009: Detect Anomalous Crime Spikes

| Field | Value |
|-------|-------|
| **Primary Actor** | System (statistical detection) |
| **Description** | Monitor rolling crime counts per (district, crime_type, week) and alert when current count exceeds historical baseline by a threshold (z-score) |
| **Preconditions** | Historical crime data loaded; baseline computed |
| **Postconditions** | Alert record created with deviation magnitude |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-010: Ask Natural-Language Investigation Question

| Field | Value |
|-------|-------|
| **Primary Actor** | IO / SHO |
| **Description** | Type a plain-English question about cases, persons, or vehicles. System retrieves relevant documents and returns a grounded, cited answer. |
| **Preconditions** | QuickML LLM serving + RAG configured; curated case corpus indexed |
| **Postconditions** | Answer displayed with source citations |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-011: Authenticate and Authorize User

| Field | Value |
|-------|-------|
| **Primary Actor** | All users |
| **Description** | User logs in via Catalyst Authentication. System verifies credentials and enforces RBAC permissions for the user's role (Investigator, SCRB, Compliance) |
| **Preconditions** | Catalyst Authentication configured; role definitions created |
| **Postconditions** | User session established; role-appropriate UI rendered |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-012: Audit Sensitive Data Access

| Field | Value |
|-------|-------|
| **Primary Actor** | System (audit logger) |
| **Description** | Every read of a person-level record and every AI-recommendation view writes an AuditLog entry: actor, action, entity, timestamp, justification |
| **Preconditions** | AuditLog table exists; audit hooks wired into data access layer |
| **Postconditions** | Audit audit trail is queryable |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-013: Verify Fairness and Bias Controls

| Field | Value |
|-------|-------|
| **Primary Actor** | Governance Officer |
| **Description** | Run fairness checks confirming that (a) CasteID/ReligionID never appear in RiskScore.feature_importance, and (b) general dashboard roles cannot query those two columns |
| **Preconditions** | Risk scores computed; RBAC configured |
| **Postconditions** | Fairness report displayed showing check results |
| **Priority** | MUST |
| **Scope** | MVP |

### UC-014: Generate Statutory SC/ST Aggregate Report

| Field | Value |
|-------|-------|
| **Primary Actor** | Governance Officer (Compliance role) |
| **Description** | Generate aggregate district-wise counts of crimes against SC/ST communities from ComplainantDetails.CasteID/ReligionID, for statutory reporting purposes only |
| **Preconditions** | Compliance role has access to CasteID/ReligionID columns; data present |
| **Postconditions** | Aggregate report generated (no individual-level data exposed) |
| **Priority** | SHOULD |
| **Scope** | STRETCH |

### UC-015: View State-Level Command Dashboard

| Field | Value |
|-------|-------|
| **Primary Actor** | SCRB / DGP Office |
| **Description** | State-wide KPI view: total cases by district, trend lines, cross-district comparison, hotspot overview |
| **Preconditions** | Data aggregated across all districts |
| **Postconditions** | Dashboard displays actionable state-level metrics |
| **Priority** | MUST |
| **Scope** | MVP |


### UC-016: Review and Approve AI Suggestions

| Field | Value |
|-------|-------|
| **Primary Actor** | IO / SHO |
| **Description** | Human review of AI generated suggestions before making them official. AI output is marked as a suggestion. |
| **Priority** | MUST |
| **Scope** | MVP |
