# Data Dictionary

[//]: # (Document ID: BERUNDA-DATA-004 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Source Tables (`src_`)

### 1.1 CaseMaster — Central FIR Record

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| CaseMasterID | INT | Unique identifier for each FIR/case | Auto-increment PK |
| CrimeNo | VARCHAR(50) | Structured crime number | Format: 1+4+4+4+5 digits: [CategoryCode][DistrictID][StationID][Year][Serial] |
| CaseNo | VARCHAR(50) | Case number | YYYY + 5-digit serial, last 9 digits of CrimeNo |
| CrimeRegisteredDate | DATE | Date FIR was registered | |
| PolicePersonID | INT | Officer who registered FIR | FK → Employee.EmployeeID |
| PoliceStationID | INT | Station where FIR registered | FK → Unit.UnitID |
| CaseCategoryID | INT | Case category | FK → CaseCategory.CaseCategoryID (FIR/UDR/PAR/Zero FIR) |
| GravityOffenceID | INT | Gravity of offence | FK → GravityOffence.GravityOffenceID |
| CrimeMajorHeadID | INT | Major crime head | FK → CrimeHead.CrimeHeadID |
| CrimeMinorHeadID | INT | Minor crime sub-head | FK → CrimeSubHead.CrimeSubHeadID |
| CaseStatusID | INT | Current case status | FK → CaseStatusMaster.CaseStatusID |
| CourtID | INT | Court hearing the case | FK → Court.CourtID, nullable |
| IncidentFromDate | DATETIME | Incident start (also in Inv_OccuranceTime) | |
| IncidentToDate | DATETIME | Incident end (also in Inv_OccuranceTime) | |

### 1.2 Inv_OccuranceTime — Incident Occurrence Details

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| CaseMasterID | INT | FK to CaseMaster | PK, 1:1 relationship |
| IncidentFromDate | DATETIME | Start date/time of incident | Mandatory |
| IncidentToDate | DATETIME | End date/time of incident | Nullable if single event |
| InfoReceivedPSDate | DATETIME | When police received info | Mandatory |
| Latitude | DECIMAL(10,7) | GPS latitude of incident location | |
| Longitude | DECIMAL(10,7) | GPS longitude of incident location | |
| BriefFacts | NVARCHAR(MAX) | Summary/narrative of the case | Free text; input for NER |

### 1.3 ComplainantDetails — Complainant Information

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| ComplainantID | INT | Unique complainant identifier | PK |
| CaseMasterID | INT | Associated FIR | FK → CaseMaster.CaseMasterID |
| ComplainantName | VARCHAR(200) | Full name of complainant | |
| AgeYear | INT | Age in years | |
| OccupationID | INT | Occupation | FK → OccupationMaster.OccupationID |
| ReligionID | INT | Religion | FK → ReligionMaster.ReligionID, RESTRICTED |
| CasteID | INT | Caste | FK → CasteMaster.caste_master_id, RESTRICTED |
| GenderID | INT | Gender | Lookup value |

### 1.4 Victim — Victim Information

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| VictimMasterID | INT | Unique victim identifier | PK |
| CaseMasterID | INT | Associated FIR | FK → CaseMaster.CaseMasterID |
| VictimName | VARCHAR(200) | Full name of victim | |
| AgeYear | INT | Age in years | |
| GenderID | INT | Gender | M, F, T lookup |
| VictimPolice | VARCHAR(1) | Is victim a police officer? | 1=Yes, 0=No |

### 1.5 Accused — Accused Information

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| AccusedMasterID | INT | Unique accused identifier | PK |
| CaseMasterID | INT | Associated FIR | FK → CaseMaster.CaseMasterID |
| AccusedName | VARCHAR(200) | Full name of accused | |
| AgeYear | INT | Age in years | |
| GenderID | INT | Gender | M/F/T lookup |
| PersonID | VARCHAR(10) | Accused sorting label | A1, A2, A3... |

### 1.6 ArrestSurrender — Arrest/Voluntary Surrender Events

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| ArrestSurrenderID | INT | Unique event identifier | PK |
| CaseMasterID | INT | Associated FIR | FK → CaseMaster.CaseMasterID |
| ArrestSurrenderTypeID | INT | Event type | Arrest or surrender (lookup) |
| ArrestSurrenderDate | DATE | Date of event | |
| ArrestSurrenderStateId | INT | State of event | FK → State.StateID |
| ArrestSurrenderDistrictId | INT | District of event | FK → District.DistrictID |
| PoliceStationID | INT | Handling station | FK → Unit.UnitID |
| IOID | INT | Investigating Officer | FK → Employee.EmployeeID |
| CourtID | INT | Court where produced | FK → Court.CourtID, nullable |
| AccusedMasterID | INT | Accused person | FK → Accused.AccusedMasterID |
| IsAccused | BIT | Primary accused? | 1=Yes |
| IsComplainantAccused | BIT | Complainant also accused? | 1=Yes |

### 1.7 ActSectionAssociation — Case Act-Section Links

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| CaseMasterID | INT | Associated FIR | FK → CaseMaster.CaseMasterID, PK (composite) |
| ActID | VARCHAR(10) | Legal act code | FK → Act.ActCode, PK (composite) |
| SectionID | VARCHAR(10) | Section code | FK → Section.SectionCode, PK (composite) |
| ActOrderID | INT | Display order for act | |
| SectionOrderID | INT | Display order for section | |

### 1.8 Act — Legal Act Reference

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| ActCode | VARCHAR(10) | Act unique code | PK, e.g., IPC, NDPS, CrPC |
| ActDescription | VARCHAR(500) | Full official name | |
| ShortName | VARCHAR(100) | Common abbreviation | |
| Active | BIT | Is active? | 1=Active, 0=Inactive |

### 1.9 Section — Legal Section Reference

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| ActCode | VARCHAR(10) | Parent act | FK → Act.ActCode, PK (composite) |
| SectionCode | VARCHAR(10) | Section number | e.g., 302, 307, 376, PK (composite) |
| SectionDescription | VARCHAR(500) | Full description | |
| Active | BIT | Is active? | 1=Active, 0=Inactive |

### 1.10-1.27 Lookup Tables

All lookup tables (CrimeHead, CrimeSubHead, CrimeHeadActSection, CasteMaster, ReligionMaster, OccupationMaster, CaseStatusMaster, Court, District, State, Unit, UnitType, Rank, Designation, Employee, CaseCategory, GravityOffence, ChargesheetDetails) follow a consistent pattern:

| Field | Type | Description |
|-------|------|-------------|
| {Table}ID | INT | PK (except Act: ActCode VARCHAR, Section: composite VARCHAR) |
| {Name} | VARCHAR(100-200) | Display name/description |
| Active | BIT | Soft-delete/status flag |

Special notes:
- **CasteMaster/R**eligionMaster: Access restricted to Compliance role only (ADR-007)
- **Unit**: Has `ParentUnit` (INT) for hierarchy self-reference
- **Employee**: Contains KGID (Karnataka Government ID), RankID, DesignationID

## 2. Intelligence Tables (`int_`)

### 2.1 PersonEntity — Deduplicated Person Identity

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| PersonEntityID | INT | Unique entity identifier | PK, auto-increment |
| CanonicalName | VARCHAR(200) | Best-guess canonical name | Chosen from most-frequent variant |
| DOB | DATE | Derived date of birth | Nullable; approximated from age |
| Gender | VARCHAR(1) | Derived gender | M/F/T; most-frequent from sources |
| PrimaryDistrictID | INT | Most associated district | FK → District.DistrictID |
| RiskScoreID | INT | Latest risk score | FK → RiskScore.RiskScoreID, nullable |
| CreatedAt | DATETIME | Record created | |
| UpdatedAt | DATETIME | Record updated | |

### 2.2 PersonEntityLink — Source Record to Entity Link

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| PersonEntityLinkID | INT | Unique link identifier | PK, auto-increment |
| PersonEntityID | INT | Target entity | FK → PersonEntity.PersonEntityID |
| SourceTable | VARCHAR(50) | Source table name | "ComplainantDetails", "Victim", "Accused" |
| SourceRecordID | INT | PK in source table | |
| CaseMasterID | INT | Associated case | FK → CaseMaster.CaseMasterID |
| Confidence | DECIMAL(5,4) | Match confidence | 0.0000-1.0000 |
| IsReviewed | BIT | Human reviewed? | 0=No, 1=Yes |
| ReviewedBy | INT | Reviewer employee ID | FK → Employee.EmployeeID, nullable |
| ReviewedAt | DATETIME | Review timestamp | Nullable |
| CreatedAt | DATETIME | Record created | |

### 2.3 RelationshipEdge — Person-to-Person Relationship

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| RelationshipEdgeID | INT | Unique edge identifier | PK, auto-increment |
| PersonEntityA | INT | First person | FK → PersonEntity.PersonEntityID |
| PersonEntityB | INT | Second person | FK → PersonEntity.PersonEntityID |
| RelationshipType | VARCHAR(50) | Type of relationship | co-accused, accused-victim, family, etc. |
| SourceCaseID | INT | Case revealing this edge | FK → CaseMaster.CaseMasterID |
| Confidence | DECIMAL(5,4) | Edge confidence | 0.0000-1.0000 |
| DiscoveredAt | DATETIME | When discovered | |
| CreatedAt | DATETIME | Record created | |

### 2.4 VehicleLink — Vehicle-to-Case Link

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| VehicleLinkID | INT | Unique link identifier | PK, auto-increment |
| VehicleNumber | VARCHAR(50) | Registration number | e.g., KA-01-AB-1234 |
| CaseMasterID | INT | Associated case | FK → CaseMaster.CaseMasterID |
| Confidence | DECIMAL(5,4) | Extraction confidence | 0.0000-1.0000 |
| Source | VARCHAR(50) | How extracted | NER, manual, extracted |
| CreatedAt | DATETIME | Record created | |

### 2.5 RiskScore — Person Risk Assessment

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| RiskScoreID | INT | Unique score identifier | PK, auto-increment |
| PersonEntityID | INT | Scored person | FK → PersonEntity.PersonEntityID |
| Score | DECIMAL(6,5) | Risk probability | 0.00000-1.00000 |
| ModelVersion | VARCHAR(20) | Model identifier | e.g., quickml-auto-v1 |
| FeaturesJSON | JSON | Input feature snapshot | Includes all features used |
| ComputedAt | DATETIME | Computation timestamp | |
| CreatedAt | DATETIME | Record created | |

### 2.6 RiskScoreFeatureImportance — Feature Explanation

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| RiskScoreImportanceID | INT | Unique importance identifier | PK, auto-increment |
| RiskScoreID | INT | Parent score | FK → RiskScore.RiskScoreID |
| FeatureName | VARCHAR(100) | Feature name | e.g., num_prior_cases, age_group |
| ImportanceValue | DECIMAL(10,8) | Normalized importance | |

### 2.7 MoPattern — Modus Operandi Pattern

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| MoPatternID | INT | Unique pattern identifier | PK, auto-increment |
| PatternName | VARCHAR(200) | Human-readable label | |
| Embedding | BLOB/VECTOR | Pattern embedding vector | |
| CreatedAt | DATETIME | Record created | |

### 2.8 MoPatternLink — Case-to-Pattern Link

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| MoPatternLinkID | INT | Unique link identifier | PK, auto-increment |
| MoPatternID | INT | Pattern | FK → MoPattern.MoPatternID |
| CaseMasterID | INT | Case | FK → CaseMaster.CaseMasterID |
| SimilarityScore | DECIMAL(5,4) | Pattern match score | 0.0000-1.0000 |
| CreatedAt | DATETIME | Record created | |

### 2.9 AnomalyAlert — Detected Anomaly Record

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| AnomalyAlertID | INT | Unique alert identifier | PK, auto-increment |
| DistrictID | INT | District | FK → District.DistrictID |
| CrimeHeadID | INT | Crime head | FK → CrimeHead.CrimeHeadID |
| WeekStart | DATE | Start of observation week | |
| ObservedCount | INT | Actual count | |
| BaselineMean | DECIMAL(10,4) | Historical mean | |
| StdDev | DECIMAL(10,4) | Standard deviation | |
| ZScore | DECIMAL(10,4) | Computed z-score | |
| AlertLevel | BIT | Is alert triggered? | 1=Alert, 0=Normal |
| CreatedAt | DATETIME | Record created | |

### 2.10 HotspotLayer — Geospatial Density Tile

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| HotspotLayerID | INT | Unique tile identifier | PK, auto-increment |
| DistrictID | INT | District | FK → District.DistrictID |
| TileX | INT | Grid X coordinate | |
| TileY | INT | Grid Y coordinate | |
| DensityScore | DECIMAL(10,4) | KDE density value | |
| WeekStart | DATE | Start of period | |
| WeekEnd | DATE | End of period | |
| CreatedAt | DATETIME | Record created | |

### 2.11 RAGCorpusChunk — Retrieved Augmented Generation Corpus

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| ChunkID | INT | Unique chunk identifier | PK, auto-increment |
| CaseMasterID | INT | Source case | FK → CaseMaster.CaseMasterID |
| ChunkIndex | INT | Chunk sequence number | Within case |
| ChunkText | NVARCHAR(MAX) | Text content | Chunked from BriefFacts |
| Embedding | BLOB/VECTOR | Vector embedding | |
| CreatedAt | DATETIME | Record created | |

## 3. Governance Tables (`gov_`)

### 3.1 AuditLog — Append-Only Audit Trail

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| AuditLogID | BIGINT | Unique audit identifier | PK, auto-increment (BIGINT for volume) |
| UserID | INT | Acting user | FK → Employee.EmployeeID |
| Action | VARCHAR(50) | Action performed | READ, CREATE, UPDATE, MERGE_CONFIRM, RAG_QUERY, etc. |
| EntityType | VARCHAR(50) | Entity affected | PersonEntity, RiskScore, CaseMaster, etc. |
| EntityID | INT | Entity PK | |
| OldValue | JSON | Pre-change state | Nullable for CREATE actions |
| NewValue | JSON | Post-change state | Nullable for READ/DELETE actions |
| Timestamp | DATETIME | Action timestamp | |
| IPAddress | VARCHAR(45) | Client IP | IPv4 or IPv6 |

### 3.2 FairnessCheckResult — Automated Fairness Verification

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| FairnessCheckID | INT | Unique check identifier | PK, auto-increment |
| CheckType | VARCHAR(50) | Type of check | model_exclusion, access_control |
| Timestamp | DATETIME | Check timestamp | |
| Passed | BIT | Check outcome | 1=Passed, 0=Failed |
| Details | JSON | Full check output | |
| CheckedBy | VARCHAR(100) | Check executor | System or username |

### 3.3 DataProvenanceRecord — Data Lineage Tracking

| Field | Type | Description | Values/Rules |
|-------|------|-------------|--------------|
| ProvenanceID | BIGINT | Unique provenance identifier | PK, auto-increment |
| TargetTable | VARCHAR(50) | Destination table | |
| TargetRecordID | INT | Destination record PK | |
| SourceTable | VARCHAR(50) | Source table | |
| SourceRecordID | INT | Source record PK | |
| TransformationDescription | VARCHAR(500) | What was done | e.g., "NER extraction from BriefFacts" |
| CreatedAt | DATETIME | Record created | |

## 4. Data Type Mapping (PDF → Catalyst Data Store)

| PDF Type | Catalyst Data Store (MySQL) |
|----------|---------------------------|
| INT | INT |
| VARCHAR | VARCHAR |
| NVARCHAR(MAX) | TEXT / LONGTEXT |
| DECIMAL | DECIMAL(p,s) |
| DATE | DATE |
| DATETIME | DATETIME |
| BIT | TINYINT(1) |
| JSON | JSON (MySQL 8+) |
| BLOB | BLOB / LONGBLOB |
