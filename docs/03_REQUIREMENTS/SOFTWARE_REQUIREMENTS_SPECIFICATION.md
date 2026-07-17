# Software Requirements Specification

[//]: # (Document ID: BERUNDA-SRS-001 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Functional Requirements

### 1.1 Data Ingestion

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-001 | FIR Structured Import | System shall ingest FIR/incident records from structured Excel/CSV files into the Data Store schema | MUST | MVP | 01_Blueprint §4.1 |
| FR-002 | FIR Manual Entry | System shall provide a manual entry form for FIR data input | MUST | MVP | 01_Blueprint §4.1 |
| FR-003 | Data Validation | System shall validate imported data for required fields, referential integrity, and type correctness | MUST | MVP | 01_Blueprint §6.7 |
| FR-004 | Duplicate Detection | System shall detect and flag potential duplicate FIR records based on CrimeNo | SHOULD | MVP | 01_Blueprint §6.8 |

### 1.2 Entity Extraction

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-005 | English NER | System shall extract person names, locations, vehicles, and organizations from English FIR narrative text | MUST | MVP | 01_Blueprint §8.1 |
| FR-006 | Kannada NER | System shall extract entities from Kannada FIR narrative text | SHOULD | STRETCH | 01_Blueprint §8.1 |
| FR-007 | Confidence Scoring | Every extracted entity shall include a confidence score | MUST | MVP | 01_Blueprint §8.1 |
| FR-008 | Entity Linking | Extracted entities shall be linked to the originating CaseMaster record | MUST | MVP | 01_Blueprint §8.1 |

### 1.3 Entity Resolution

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-009 | PersonEntity Identity | System shall maintain a PersonEntity table as a deduplicated cross-case identity store | MUST | MVP | 01_Blueprint §6.3 |
| FR-010 | Blocking Strategy | System shall use blocking (name similarity + age band + address/locality overlap) for candidate generation | MUST | MVP | 01_Blueprint §6.3 |
| FR-011 | Similarity Scoring | System shall compute weighted similarity score for candidate record pairs | MUST | MVP | 01_Blueprint §6.3 |
| FR-012 | Match Thresholds | System shall support configurable match/possible/no-match thresholds with a grey zone requiring manual review | MUST | MVP | 01_Blueprint §6.3 |
| FR-013 | Manual Review | System shall present possible matches to an Investigator for manual confirmation | MUST | MVP | 01_Blueprint §6.3 |
| FR-014 | Merge Approval | Only a human reviewer may confirm a merge; no auto-merges | MUST | MVP | 01_Blueprint §7.1 |
| FR-015 | Provenance Tracking | Every PersonEntityLink shall record source table, source record ID, and match confidence | MUST | MVP | 01_Blueprint §6.3 |

### 1.4 Relationship Graph

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-016 | RelationshipEdge Table | System shall maintain a RelationshipEdge table with person_entity_a, person_entity_b, relationship_type, source_case, confidence | MUST | MVP | 01_Blueprint §6.4 |
| FR-017 | Graph Traversal | System shall support degree centrality and shortest-path traversal over RelationshipEdge | MUST | MVP | 01_Blueprint §8.3 |
| FR-018 | Graph Visualization | System shall render a force-directed node-link graph in the browser | MUST | MVP | 01_Blueprint §11 |
| FR-019 | Vehicle Linking | System shall maintain vehicle-to-case links via VehicleLink table | MUST | MVP | 01_Blueprint §6.4 |
| FR-020 | MO Pattern Matching | System shall flag incidents sharing similar modus operandi via embedding similarity | SHOULD | STRETCH | 01_Blueprint §8.4 |

### 1.5 Geospatial Analytics

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-021 | Hotspot Map | System shall render a hexbin/heatmap layer from Incident latitude/longitude | MUST | MVP | 01_Blueprint §8.6 |
| FR-022 | District Drill-Down | System shall support drill-down from state → district → station jurisdiction | MUST | MVP | 01_Blueprint §8.6 |
| FR-023 | Temporal Filter | System shall support filtering by date range, crime type, and jurisdiction | MUST | MVP | 01_Blueprint §4.1 |
| FR-024 | Anomaly Detection | System shall detect z-score deviations in rolling (district, crime_type, week) counts vs. historical baseline | MUST | MVP | 01_Blueprint §8.7 |
| FR-025 | Anomaly Alert | System shall create alert records for detected anomalies with deviation magnitude | MUST | MVP | 01_Blueprint §8.7 |

### 1.6 Risk Scoring

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-026 | Risk Score Computation | System shall compute a repeat-offender risk score per PersonEntity using QuickML AutoML | MUST | MVP | 01_Blueprint §8.5 |
| FR-027 | Feature Importance | Every risk score shall include a JSON feature-importance breakdown | MUST | MVP | 01_Blueprint §8.5 |
| FR-028 | Feature Exclusion | CasteID, ReligionID, and any identity-proxy variables shall be hard-excluded from the feature set | MUST | MVP | 01_Blueprint §6.2 |
| FR-029 | Score Explainability | Feature-importance breakdown shall be visible in the Investigator Console | MUST | MVP | 01_Blueprint §8.5 |

### 1.7 Natural Language Query

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-030 | RAG Query | System shall accept plain-English questions and return grounded, cited answers over the case corpus | MUST | MVP | 01_Blueprint §8.9 |
| FR-031 | Source Citations | Every answer shall cite the source document(s) it was derived from | MUST | MVP | 01_Blueprint §8.9 |
| FR-032 | Role-Based Filtering | RAG retrieval shall respect role-based access controls (do not return restricted data) | MUST | MVP | 01_Blueprint §8.9 |
| FR-033 | Insufficient Evidence Response | When evidence is insufficient, the system shall state "Insufficient evidence" rather than hallucinate | MUST | MVP | 01_Blueprint §8.9 |
| FR-034 | Query Audit | Every RAG query and answer shall be logged in the AuditLog | MUST | MVP | 01_Blueprint §8.9 |

### 1.8 Authentication & Authorization

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-035 | User Authentication | System shall authenticate users via Catalyst Authentication | MUST | MVP | 01_Blueprint §12.1 |
| FR-036 | Role-Based Access | System shall enforce RBAC with at least 3 roles: Investigator, SCRB Analyst, Compliance Officer | MUST | MVP | 01_Blueprint §12.1 |
| FR-037 | Jurisdiction Scoping | Investigator role shall be scoped to their assigned district/station records | MUST | MVP | 01_Blueprint §12.1 |
| FR-038 | MFA Support | MFA shall be required for accounts accessing person-level records | MUST | MVP | 01_Blueprint §12.1 |

### 1.9 Audit Logging

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-039 | Person-Level Read Audit | Every read of a person-level record shall write to AuditLog | MUST | MVP | 01_Blueprint §12.3 |
| FR-040 | AI Output Audit | Every AI-assisted recommendation surfaced to a human shall write to AuditLog | MUST | MVP | 01_Blueprint §12.3 |
| FR-041 | Append-Only Log | AuditLog shall be append-only at the application layer | MUST | MVP | 01_Blueprint §12.3 |
| FR-042 | Audit Queryability | Governance Officer shall be able to search and filter AuditLog | MUST | MVP | 01_Blueprint §12.3 |

### 1.10 Governance

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-043 | Fairness Check | System shall verify that CasteID/ReligionID do not appear in any RiskScore.feature_importance | MUST | MVP | 01_Blueprint §8.13 |
| FR-044 | Role Restriction Check | System shall verify that general dashboard roles cannot query CasteID/ReligionID columns | MUST | MVP | 01_Blueprint §6.2 |
| FR-045 | Fairness Dashboard | Governance Officer shall have a dashboard showing fairness check results | MUST | MVP | 01_Blueprint §11.1 |

### 1.11 Synthetic Data

| ID | Title | Description | Priority | Scope | Source |
|----|-------|-------------|----------|-------|--------|
| FR-046 | Synthetic Data Generation | System shall support generating 2000+ synthetic FIR records using Faker (en_IN) | MUST | MVP | 01_Blueprint §6.7 |
| FR-047 | Planted Patterns | Synthetic data shall include deliberately planted patterns: repeat-offender, shared-vehicle, hotspot week | MUST | MVP | 01_Blueprint §6.7 |
| FR-048 | Seeded Reproducibility | Synthetic data generation shall use a seeded RNG for reproducibility | MUST | MVP | 01_Blueprint §6.7 |
| FR-049 | Synthetic Labeling | Every synthetic record shall be clearly labeled as synthetic | MUST | MVP | 01_Blueprint §6.7 |

## 2. Data Requirements

| ID | Title | Description | Priority | Scope |
|----|-------|-------------|----------|-------|
| DR-001 | Source Schema Migration | All 27+ source tables from the FIR ERD shall be migrated to Catalyst Data Store | MUST | MVP |
| DR-002 | Berunda Extension Tables | PersonEntity, PersonEntityLink, RelationshipEdge, RiskScore, AuditLog tables shall be created | MUST | MVP |
| DR-003 | Indexes | Composite indexes shall be created on CaseMaster(CrimeMajorHeadID, CrimeRegisteredDate, PoliceStationID) | MUST | MVP |
| DR-004 | CasteID Not Indexed | ComplainantDetails.CasteID and ReligionID shall NOT be indexed for general search | MUST | MVP |
| DR-005 | CrimeNo Parsing | District/station/year components embedded in CrimeNo shall be parsed at ingestion time | MUST | MVP |
| DR-006 | Full-Text Index | Full-text index on Inv_OccuranceTime.BriefFacts | MUST | MVP |
| DR-007 | Schema Separation | Source tables and Berunda extension tables shall be in separate logical schemas/namespaces | MUST | MVP |

## 3. AI Requirements

| ID | Title | Description | Priority | Scope |
|----|-------|-------------|----------|-------|
| AIR-001 | NER Pipeline | English NER using spaCy pipeline deployed as a Catalyst Function | MUST | MVP |
| AIR-002 | Risk Scoring Model | Gradient-boosted trees via QuickML AutoML for risk scoring | MUST | MVP |
| AIR-003 | Hotspot Detection | KDE/hexbin aggregation for hotspot detection | MUST | MVP |
| AIR-004 | Anomaly Detection | Z-score deviation from rolling baseline for anomaly detection | MUST | MVP |
| AIR-005 | RAG Foundation | QuickML LLM serving + RAG over curated case corpus | MUST | MVP |
| AIR-006 | Feature Importance | All model outputs include feature-importance via QuickML native capability | MUST | MVP |
| AIR-007 | Fairness Auditing | Rule-based parity check for feature exclusion | MUST | MVP |
| AIR-008 | Kannada NER | AI4Bharat/IndicNLP model for Kannada NER | SHOULD | STRETCH |
| AIR-009 | MO Embeddings | Sentence-transformer embedding similarity for MO matching | SHOULD | STRETCH |
| AIR-010 | Drift Monitoring | Scheduled re-evaluation of model performance against held-out window | SHOULD | STRETCH |
| AIR-011 | Bias Proxy Check | Automated check that no excluded variable proxies appear in feature sets | SHOULD | STRETCH |
| AIR-012 | No Criminality Prediction | System shall NOT predict individual criminality or likelihood of future offending | MUST | MVP |
| AIR-013 | Advisory Only | Every AI output shall be labeled as advisory, not automated | MUST | MVP |
| AIR-014 | Human-in-the-Loop | No AI output shall trigger an automatic enforcement action | MUST | MVP |
| AIR-015 | Confidence Display | Every AI output shall display confidence or uncertainty | MUST | MVP |

## 4. Security Requirements

| ID | Title | Description | Priority | Scope |
|----|-------|-------------|----------|-------|
| SEC-001 | Encryption at Rest | All data in Data Store, NoSQL, and Stratus shall be encrypted at rest | MUST | MVP |
| SEC-002 | Encryption in Transit | All communication shall use TLS, enforced at API Gateway | MUST | MVP |
| SEC-003 | API Gateway | All API calls shall route through Catalyst API Gateway for auth and throttling | MUST | MVP |
| SEC-004 | Input Validation | All user inputs shall be validated and sanitized against injection attacks | MUST | MVP |
| SEC-005 | Parameterized Queries | All database queries shall use parameterized bindings (no string concatenation) | MUST | MVP |
| SEC-006 | Secrets Management | API keys and credentials shall be stored in Catalyst secrets management, not code | MUST | MVP |
| SEC-007 | CasteID Role Restriction | CasteID/ReligionID columns accessible only to Compliance role | MUST | MVP |
| SEC-008 | Rate Limiting | API Gateway rate limiting to prevent abuse | MUST | MVP |
| SEC-009 | Session Management | Authenticated sessions with timeout and secure cookie handling | MUST | MVP |

## 5. Privacy Requirements

| ID | Title | Description | Priority | Scope |
|----|-------|-------------|----------|-------|
| PRIV-001 | No Real PII in Demo | Only synthetic person-level data in demo; no real victim/accused/witness data | MUST | MVP |
| PRIV-002 | Synthetic Labeling | All synthetic person records shall be clearly and persistently labeled | MUST | MVP |
| PRIV-003 | Data Minimization | Only data required for named features shall be collected | MUST | MVP |
| PRIV-004 | Caste/Religion Governance | CasteID/ReligionID never in model features; aggregate reporting only | MUST | MVP |
| PRIV-005 | Audit Proportionality | Audit logs capture who/what/when/why, not full record contents | MUST | MVP |
