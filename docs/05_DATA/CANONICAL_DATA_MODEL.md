# Canonical Data Model

[//]: # (Document ID: BERUNDA-DATA-003 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Data Engineers, QA | Source: ERD PDF | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Source Schema Definitions (`src_`)

All tables from the Police FIR ER Diagram. Column types follow the PDF specification. Each table is prefixed with `src_` in the Catalyst Data Store.

### src_CaseMaster

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CaseMasterID | INT | PK | Auto-increment |
| CrimeNo | VARCHAR(50) | | Formatted: 1+4+4+4+5 digits |
| CaseNo | VARCHAR(50) | | YYYY + 5-digit serial |
| CrimeRegisteredDate | DATE | | |
| PolicePersonID | INT | FK → src_Employee.EmployeeID | |
| PoliceStationID | INT | FK → src_Unit.UnitID | |
| CaseCategoryID | INT | FK → src_CaseCategory.CaseCategoryID | |
| GravityOffenceID | INT | FK → src_GravityOffence.GravityOffenceID | |
| CrimeMajorHeadID | INT | FK → src_CrimeHead.CrimeHeadID | |
| CrimeMinorHeadID | INT | FK → src_CrimeSubHead.CrimeSubHeadID | |
| CaseStatusID | INT | FK → src_CaseStatusMaster.CaseStatusID | |
| CourtID | INT | FK → src_Court.CourtID | |
| IncidentFromDate | DATETIME | | (from Relationship Matrix — also in Inv_OccuranceTime) |
| IncidentToDate | DATETIME | | (from Relationship Matrix — also in Inv_OccuranceTime) |

### src_Inv_OccuranceTime

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CaseMasterID | INT | PK, FK → src_CaseMaster.CaseMasterID | 1:1 relationship |
| IncidentFromDate | DATETIME | | Start date/time of incident |
| IncidentToDate | DATETIME | | End date/time of incident |
| InfoReceivedPSDate | DATETIME | | When police station received info |
| Latitude | DECIMAL(10,7) | | GPS coordinate |
| Longitude | DECIMAL(10,7) | | GPS coordinate |
| BriefFacts | NVARCHAR(MAX) | | Full FIR narrative text |

### src_ComplainantDetails

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| ComplainantID | INT | PK | |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | |
| ComplainantName | VARCHAR(200) | | |
| AgeYear | INT | | |
| OccupationID | INT | FK → src_OccupationMaster.OccupationID | |
| ReligionID | INT | FK → src_ReligionMaster.ReligionID | RESTRICTED (ADR-007) |
| CasteID | INT | FK → src_CasteMaster.caste_master_id | RESTRICTED (ADR-007) |
| GenderID | INT | | Lookup value |

### src_Victim

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| VictimMasterID | INT | PK | |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | |
| VictimName | VARCHAR(200) | | |
| AgeYear | INT | | |
| GenderID | INT | | M/F/T lookup |
| VictimPolice | VARCHAR(1) | | "1" if police, "0" otherwise |

### src_Accused

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| AccusedMasterID | INT | PK | |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | |
| AccusedName | VARCHAR(200) | | |
| AgeYear | INT | | |
| GenderID | INT | | M/F/T lookup |
| PersonID | VARCHAR(10) | | e.g., A1, A2, A3 |

### src_ArrestSurrender

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| ArrestSurrenderID | INT | PK | |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | |
| ArrestSurrenderTypeID | INT | | Arrest or surrender (lookup) |
| ArrestSurrenderDate | DATE | | |
| ArrestSurrenderStateId | INT | FK → src_State.StateID | |
| ArrestSurrenderDistrictId | INT | FK → src_District.DistrictID | |
| PoliceStationID | INT | FK → src_Unit.UnitID | |
| IOID | INT | FK → src_Employee.EmployeeID | |
| CourtID | INT | FK → src_Court.CourtID | |
| AccusedMasterID | INT | FK → src_Accused.AccusedMasterID | |
| IsAccused | BIT | | Primary accused? |
| IsComplainantAccused | BIT | | Complainant also accused? |

### src_ActSectionAssociation

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | Composite PK |
| ActID | VARCHAR(10) | FK → src_Act.ActCode | Composite PK |
| SectionID | VARCHAR(10) | FK → src_Section.SectionCode | Composite PK |
| ActOrderID | INT | | Display order for act |
| SectionOrderID | INT | | Display order for section |

### src_Act

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| ActCode | VARCHAR(10) | PK | e.g., IPC, NDPS |
| ActDescription | VARCHAR(500) | | Full name |
| ShortName | VARCHAR(100) | | Abbreviation |
| Active | BIT | | |

### src_Section

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| ActCode | VARCHAR(10) | FK → src_Act.ActCode | Composite PK |
| SectionCode | VARCHAR(10) | | Composite PK, e.g., "302" |
| SectionDescription | VARCHAR(500) | | |
| Active | BIT | | |

### src_CrimeHeadActSection

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CrimeHeadID | INT | FK → src_CrimeHead.CrimeHeadID | Composite PK |
| ActCode | VARCHAR(10) | FK → src_Act.ActCode | Composite PK |
| SectionCode | VARCHAR(10) | | |

### src_CrimeHead

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CrimeHeadID | INT | PK | |
| CrimeGroupName | VARCHAR(200) | | e.g., Crimes Against Body |
| Active | BIT | | |

### src_CrimeSubHead

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CrimeSubHeadID | INT | PK | |
| CrimeHeadID | INT | FK → src_CrimeHead.CrimeHeadID | |
| CrimeHeadName | VARCHAR(200) | | e.g., Murder, Robbery |
| SeqID | INT | | Display sort order |
| Active | BIT | | |

### src_CasteMaster

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| caste_master_id | INT | PK | |
| caste_master_name | VARCHAR(100) | | RESTRICTED access |
| Active | BIT | | |

### src_ReligionMaster

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| ReligionID | INT | PK | |
| ReligionName | VARCHAR(100) | | RESTRICTED access |
| Active | BIT | | |

### src_OccupationMaster

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| OccupationID | INT | PK | |
| OccupationName | VARCHAR(100) | | |
| Active | BIT | | |

### src_CaseStatusMaster

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CaseStatusID | INT | PK | |
| CaseStatusName | VARCHAR(100) | | Under Investigation, Charge Sheeted, Closed |
| Active | BIT | | |

### src_Court

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CourtID | INT | PK | |
| CourtName | VARCHAR(200) | | |
| DistrictID | INT | FK → src_District.DistrictID | |
| StateID | INT | FK → src_State.StateID | |
| Active | BIT | | |

### src_District

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| DistrictID | INT | PK | |
| DistrictName | VARCHAR(100) | | |
| StateID | INT | FK → src_State.StateID | |
| Active | BIT | | |

### src_State

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| StateID | INT | PK | |
| StateName | VARCHAR(100) | | |
| NationalityID | INT | | |
| Active | BIT | | |

### src_Unit

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| UnitID | INT | PK | |
| UnitName | VARCHAR(200) | | Police station name |
| TypeID | INT | FK → src_UnitType.UnitTypeID | |
| ParentUnit | INT | | Self-reference FK |
| NationalityID | INT | | |
| StateID | INT | FK → src_State.StateID | |
| DistrictID | INT | FK → src_District.DistrictID | |
| Active | BIT | | |

### src_UnitType

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| UnitTypeID | INT | PK | |
| UnitTypeName | VARCHAR(100) | | Police Station, Circle Office |
| CityDistState | VARCHAR(50) | | City / District / State |
| Hierarchy | INT | | Lower = higher authority |
| Active | BIT | | |

### src_Rank

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| RankID | INT | PK | |
| RankName | VARCHAR(100) | | Constable, Inspector, DSP |
| Hierarchy | INT | | Lower = higher rank |
| Active | BIT | | |

### src_Designation

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| DesignationID | INT | PK | |
| DesignationName | VARCHAR(100) | | IO, SHO |
| Active | BIT | | |
| SortOrder | INT | | |

### src_Employee

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| EmployeeID | INT | PK | |
| DistrictID | INT | FK → src_District.DistrictID | Current posting district |
| UnitID | INT | FK → src_Unit.UnitID | Current unit |
| RankID | INT | FK → src_Rank.RankID | |
| DesignationID | INT | FK → src_Designation.DesignationID | |
| KGID | VARCHAR(50) | | Karnataka Government ID |
| FirstName | VARCHAR(100) | | |
| EmployeeDOB | DATE | | |
| GenderID | INT | | Lookup |
| BloodGroupID | INT | | Lookup |
| PhysicallyChallenged | BIT | | |
| AppointmentDate | DATE | | |

### src_CaseCategory

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CaseCategoryID | INT | PK | |
| LookupValue | VARCHAR(10) | | FIR, UDR, PAR, Zero FIR |
| Active | BIT | | |

### src_GravityOffence

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| GravityOffenceID | INT | PK | |
| LookupValue | VARCHAR(50) | | Heinous, Non-Heinous |
| Active | BIT | | |

### src_ChargesheetDetails

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| CSID | INT | PK | |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | |
| csdate | DATETIME | | Chargesheet date |
| cstype | CHAR(1) | | A=Chargesheet, B=False Case, C=Undetected |
| PolicePersonID | INT | FK → src_Employee.EmployeeID | |
| Active | BIT | | |

## 2. Intelligence Schema Definitions (`int_`)

### int_PersonEntity

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| PersonEntityID | INT | PK | Auto-increment |
| CanonicalName | VARCHAR(200) | | Best-guess canonical name |
| DOB | DATE | | Derived from age/dob info (nullable) |
| Gender | VARCHAR(1) | | M/F/T (derived from source records) |
| PrimaryDistrictID | INT | FK → src_District.DistrictID | Most commonly associated district |
| RiskScoreID | INT | FK → int_RiskScore.RiskScoreID | Nullable until computed |
| CreatedAt | DATETIME | | |
| UpdatedAt | DATETIME | | |

### int_PersonEntityLink

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| PersonEntityLinkID | INT | PK | Auto-increment |
| PersonEntityID | INT | FK → int_PersonEntity.PersonEntityID | |
| SourceTable | VARCHAR(50) | | "ComplainantDetails", "Victim", "Accused" |
| SourceRecordID | INT | | PK of the source table row |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | For quick case lookup |
| Confidence | DECIMAL(5,4) | | 0.0000 - 1.0000 |
| IsReviewed | BIT | | Has human reviewed? Default 0 |
| ReviewedBy | INT | FK → src_Employee.EmployeeID | Nullable |
| ReviewedAt | DATETIME | | Nullable |
| CreatedAt | DATETIME | | |

### int_RelationshipEdge

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| RelationshipEdgeID | INT | PK | Auto-increment |
| PersonEntityA | INT | FK → int_PersonEntity.PersonEntityID | |
| PersonEntityB | INT | FK → int_PersonEntity.PersonEntityID | |
| RelationshipType | VARCHAR(50) | | e.g., "co-accused", "accused-victim", "family" |
| SourceCaseID | INT | FK → src_CaseMaster.CaseMasterID | Case that revealed this relationship |
| Confidence | DECIMAL(5,4) | | 0.0000 - 1.0000 |
| DiscoveredAt | DATETIME | | |
| CreatedAt | DATETIME | | |

### int_VehicleLink

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| VehicleLinkID | INT | PK | Auto-increment |
| VehicleNumber | VARCHAR(50) | | e.g., KA-01-AB-1234 |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | |
| Confidence | DECIMAL(5,4) | | |
| Source | VARCHAR(50) | | "NER", "manual", "extracted" |
| CreatedAt | DATETIME | | |

### int_RiskScore

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| RiskScoreID | INT | PK | Auto-increment |
| PersonEntityID | INT | FK → int_PersonEntity.PersonEntityID | |
| Score | DECIMAL(6,5) | | 0.00000 - 1.00000 |
| ModelVersion | VARCHAR(20) | | e.g., "quickml-auto-v1" |
| FeaturesJSON | JSON | | Input feature snapshot |
| ComputedAt | DATETIME | | |
| CreatedAt | DATETIME | | |

### int_RiskScoreFeatureImportance

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| RiskScoreImportanceID | INT | PK | Auto-increment |
| RiskScoreID | INT | FK → int_RiskScore.RiskScoreID | |
| FeatureName | VARCHAR(100) | | |
| ImportanceValue | DECIMAL(10,8) | | Normalized importance |
| CreatedAt | DATETIME | | |

### int_MoPattern

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| MoPatternID | INT | PK | Auto-increment |
| PatternName | VARCHAR(200) | | Human-readable label |
| Embedding | BLOB/VECTOR | | Vector embedding of pattern |
| CreatedAt | DATETIME | | |

### int_MoPatternLink

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| MoPatternLinkID | INT | PK | Auto-increment |
| MoPatternID | INT | FK → int_MoPattern.MoPatternID | |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | |
| SimilarityScore | DECIMAL(5,4) | | 0.0000 - 1.0000 |
| CreatedAt | DATETIME | | |

### int_AnomalyAlert

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| AnomalyAlertID | INT | PK | Auto-increment |
| DistrictID | INT | FK → src_District.DistrictID | |
| CrimeHeadID | INT | FK → src_CrimeHead.CrimeHeadID | |
| WeekStart | DATE | | |
| ObservedCount | INT | | |
| BaselineMean | DECIMAL(10,4) | | |
| StdDev | DECIMAL(10,4) | | |
| ZScore | DECIMAL(10,4) | | |
| AlertLevel | BIT | | 1=alert, 0=normal |
| CreatedAt | DATETIME | | |

### int_HotspotLayer

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| HotspotLayerID | INT | PK | Auto-increment |
| DistrictID | INT | FK → src_District.DistrictID | |
| TileX | INT | | Grid X coordinate |
| TileY | INT | | Grid Y coordinate |
| DensityScore | DECIMAL(10,4) | | KDE/hexbin density |
| WeekStart | DATE | | |
| WeekEnd | DATE | | |
| CreatedAt | DATETIME | | |

### int_RAGCorpusChunk

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| ChunkID | INT | PK | Auto-increment |
| CaseMasterID | INT | FK → src_CaseMaster.CaseMasterID | |
| ChunkIndex | INT | | Sequential chunk number |
| ChunkText | NVARCHAR(MAX) | | |
| Embedding | BLOB/VECTOR | | Vector embedding for similarity search |
| CreatedAt | DATETIME | | |

## 3. Governance Schema Definitions (`gov_`)

### gov_AuditLog

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| AuditLogID | BIGINT | PK | Auto-increment; BIGINT for volume |
| UserID | INT | FK → src_Employee.EmployeeID | |
| Action | VARCHAR(50) | | e.g., "READ", "CREATE", "MERGE_CONFIRM", "RAG_QUERY" |
| EntityType | VARCHAR(50) | | e.g., "PersonEntity", "RiskScore" |
| EntityID | INT | | PK of the entity acted upon |
| OldValue | JSON | | Nullable; snapshot before change |
| NewValue | JSON | | Nullable; snapshot after change |
| Timestamp | DATETIME | | |
| IPAddress | VARCHAR(45) | | IPv4 or IPv6 |

### gov_FairnessCheckResult

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| FairnessCheckID | INT | PK | Auto-increment |
| CheckType | VARCHAR(50) | | "model_exclusion" or "access_control" |
| Timestamp | DATETIME | | |
| Passed | BIT | | 1=passed, 0=failed |
| Details | JSON | | Full check output |
| CheckedBy | VARCHAR(100) | | System or user identifier |

### gov_DataProvenanceRecord

| Column | Type | Key | Notes |
|--------|------|-----|-------|
| ProvenanceID | BIGINT | PK | Auto-increment |
| TargetTable | VARCHAR(50) | | e.g., "int_PersonEntity" |
| TargetRecordID | INT | | |
| SourceTable | VARCHAR(50) | | e.g., "Accused" |
| SourceRecordID | INT | | |
| TransformationDescription | VARCHAR(500) | | e.g., "NER extraction from BriefFacts" |
| CreatedAt | DATETIME | | |

## 4. Index Strategy

| Table | Index | Type | Justification |
|-------|-------|------|---------------|
| src_CaseMaster | CrimeNo | UNIQUE | Duplicate detection (FR-004) |
| src_CaseMaster | PoliceStationID, CrimeRegisteredDate | COMPOSITE | Investigator jurisdiction filter |
| src_CaseMaster | Latitude, Longitude | COMPOSITE | Geospatial hotspot queries |
| int_PersonEntity | CanonicalName | INDEX | Entity resolution lookup |
| int_PersonEntityLink | PersonEntityID | INDEX | Fast link traversal |
| int_PersonEntityLink | (SourceTable, SourceRecordID) | COMPOSITE | Reverse lookup: source → entity |
| int_RelationshipEdge | PersonEntityA, PersonEntityB | COMPOSITE | Graph traversal queries |
| int_AnomalyAlert | (DistrictID, WeekStart) | COMPOSITE | Temporal anomaly queries |
| int_RAGCorpusChunk | Embedding | VECTOR INDEX | Similarity search for RAG |
| gov_AuditLog | Timestamp | DESCENDING INDEX | Audit trail queries |
| gov_AuditLog | UserID | INDEX | User activity queries |
