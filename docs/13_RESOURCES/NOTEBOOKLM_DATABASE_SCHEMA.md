Here is the complete Database Schema and data modeling details for Project Berunda (CaseGraph), extracted from the Karnataka State Police FIR ER diagrams and the project's enterprise architecture blueprints. 

The schema is divided into the core governmental System-of-Record tables and the Berunda-specific analytical extensions designed to solve data silos and deduplication.

### 1. Core Transactional Tables (System of Record)
These tables mirror the official Karnataka Police FIR schema. They capture the raw incident data but natively lack cross-case entity linkage [1, 2].

```sql
-- MAIN FIR/CASE RECORD
CREATE TABLE CaseMaster (
    CaseMasterID INT PRIMARY KEY,
    CrimeNo VARCHAR, -- Format: 1-digit Category + 4-digit Dist ID + 4-digit Station ID + 4-digit Year + 5-digit Serial
    CaseNo VARCHAR, -- Format: YYYY + 5-digit running serial (last 9 digits of CrimeNo)
    CrimeRegisteredDate DATE,
    PolicePersonID INT, -- FK -> Employee.EmployeeID
    PoliceStationID INT, -- FK -> Unit.UnitID
    CaseCategoryID INT, -- FK -> CaseCategory.CaseCategoryID
    GravityOffenceID INT, -- FK -> GravityOffence.GravityOffenceID
    CrimeMajorHeadID INT, -- FK -> CrimeHead.CrimeHeadID
    CrimeMinorHeadID INT, -- FK -> CrimeSubHead.CrimeSubHeadID
    CaseStatusID INT, -- FK -> CaseStatusMaster.CaseStatusID
    CourtID INT -- FK -> Court.CourtID
);

-- INCIDENT TIME, LOCATION & NARRATIVE (1:1 with CaseMaster)
CREATE TABLE Inv_OccuranceTime (
    CaseMasterID INT PRIMARY KEY, -- FK -> CaseMaster.CaseMasterID
    IncidentFromDate DATETIME,
    IncidentToDate DATETIME,
    InfoReceivedPSDate DATETIME,
    latitude DECIMAL,
    longitude DECIMAL,
    BriefFacts NVARCHAR(MAX) -- Free-text summary feeding the NLP/NER Agents
);

-- COMPLAINANT DETAILS
CREATE TABLE ComplainantDetails (
    ComplainantID INT PRIMARY KEY,
    CaseMasterID INT, -- FK -> CaseMaster.CaseMasterID
    ComplainantName VARCHAR,
    AgeYear INT,
    GenderID INT,
    OccupationID INT, -- FK -> OccupationMaster.OccupationID
    ReligionID INT, -- FK -> ReligionMaster.ReligionID
    CasteID INT -- FK -> CasteMaster.caste_master_id
);

-- ACCUSED DETAILS (Scoped per-case, not globally)
CREATE TABLE Accused (
    AccusedMasterID INT PRIMARY KEY,
    CaseMasterID INT, -- FK -> CaseMaster.CaseMasterID
    AccusedName VARCHAR,
    AgeYear INT,
    GenderID INT,
    PersonID VARCHAR -- Display label (e.g., A1, A2)
);

-- VICTIM DETAILS
CREATE TABLE Victim (
    VictimMasterID INT PRIMARY KEY,
    CaseMasterID INT, -- FK -> CaseMaster.CaseMasterID
    VictimName VARCHAR,
    AgeYear INT,
    GenderID INT,
    VictimPolice VARCHAR -- Flags if victim is a police officer (1 or 0)
);

-- ARREST & SURRENDER LOGS
CREATE TABLE ArrestSurrender (
    ArrestSurrenderID INT PRIMARY KEY,
    CaseMasterID INT, -- FK -> CaseMaster.CaseMasterID
    ArrestSurrenderTypeID INT,
    ArrestSurrenderDate DATE,
    ArrestSurrenderStateId INT, -- FK -> State.StateID
    ArrestSurrenderDistrictId INT, -- FK -> District.DistrictID
    PoliceStationID INT, -- FK -> Unit.UnitID
    IOID INT, -- FK -> Employee.EmployeeID
    CourtID INT, -- FK -> Court.CourtID
    AccusedMasterID INT, -- FK -> Accused.AccusedMasterID
    IsAccused BIT,
    IsComplainantAccused BIT
);

-- CHARGESHEET DETAILS
CREATE TABLE ChargesheetDetails (
    CSID INT PRIMARY KEY,
    CaseMasterID INT, -- FK -> CaseMaster.CaseMasterID
    csdate DATETIME,
    cstype CHAR, -- A->Chargesheet, B->False Case, C->Undetected
    PolicePersonID INT -- FK -> Employee.EmployeeID
);

-- APPLIED ACTS & SECTIONS
CREATE TABLE ActSectionAssociation (
    CaseMasterID INT, -- FK -> CaseMaster.CaseMasterID
    ActID INT, -- FK -> Act.ActCode
    SectionID INT, -- FK -> Section.SectionCode
    ActOrderID INT,
    SectionOrderID INT
);
```

### 2. Master / Lookup Tables
The database utilizes a strict reference hierarchy mapped via Foreign Keys to the transaction tables above [3-12].
*   **Legal Catalog:** `Act`, `Section`, and `CrimeHeadActSection` link crime heads to specific IPC/BNS/NDPS statutes [3, 4].
*   **Crime Taxonomy:** `CrimeHead` (Major Head) and `CrimeSubHead` (Minor Head) [5].
*   **Jurisdiction & Hierarchy:** `State`, `District`, `Unit` (Police Station), `UnitType`, and `Court` [8-10].
*   **Officer Roster:** `Employee` (referenced by KGID), `Rank`, `Designation` [12, 13].
*   **Demographics:** `CasteMaster`, `ReligionMaster`, `OccupationMaster` [6, 7].

### 3. Berunda Data Modeling Extensions (The Deduplication Layer)
A major challenge identified in the KSP schema is that **Accused and Victim records are scoped strictly per-FIR** [2]. If an individual is accused in three separate FIRs, they generate three unconnected `AccusedMasterID` rows [2]. 

Project Berunda addresses this by introducing a secondary analytics schema inside the Catalyst Data Store to build a cross-case intelligence graph [14, 15].

```sql
-- DEDUPLICATED MASTER IDENTITY (Created by AI Entity Resolution)
CREATE TABLE PersonEntity (
    PersonEntityID INT PRIMARY KEY,
    ResolvedName VARCHAR,
    ResolvedAgeBand VARCHAR,
    ResolvedAddress VARCHAR,
    RiskScore DECIMAL,
    CreatedByAgent VARCHAR -- Tracks the AI agent that merged the record
);

-- IDENTITY LINKAGE (Maps native FIR entities to the deduplicated Master Identity)
CREATE TABLE PersonEntityLink (
    LinkID INT PRIMARY KEY,
    PersonEntityID INT, -- FK -> PersonEntity.PersonEntityID
    SourceTable VARCHAR, -- e.g., 'Accused', 'Victim', 'Complainant'
    SourceRecordID INT, -- FK -> AccusedMasterID / VictimMasterID
    MatchConfidenceScore DECIMAL -- Accuracy of the phonetic/fuzzy match
);

-- NETWORK GRAPH EDGES
CREATE TABLE RelationshipEdge (
    EdgeID INT PRIMARY KEY,
    SourceEntityID INT, -- FK -> PersonEntity.PersonEntityID
    TargetEntityID INT, -- FK -> PersonEntity.PersonEntityID / Vehicle.VehicleID / Location
    RelationshipType VARCHAR, -- e.g., 'CO_ACCUSED', 'SHARED_VEHICLE', 'SHARED_ADDRESS'
    ConfidenceScore DECIMAL
);

-- AI REPEAT-OFFENDER RISK SCORES
CREATE TABLE RiskScore (
    RiskScoreID INT PRIMARY KEY,
    PersonEntityID INT,
    ScoreValue DECIMAL,
    FeatureImportance JSON -- Explainability layer: why the score was assigned
);

-- IMMUTABLE AUDIT LOG
CREATE TABLE AuditLog (
    AuditID INT PRIMARY KEY,
    ActorID INT, -- Investigating Officer
    ActionType VARCHAR, -- 'VIEW_PROFILE', 'DOWNLOAD_REPORT', 'MERGE_ENTITY'
    TargetEntityID INT,
    JustificationReason VARCHAR,
    Timestamp DATETIME
);
```

### 4. Core Constraints and Business Logic
*   **`CrimeNo` Smart Key:** The `CrimeNo` in `CaseMaster` is not a random string. It is a strictly formatted payload: **1-digit Case-Category code + 4-digit District ID + 4-digit Police-Station ID + 4-digit Year + 5-digit running serial** (e.g., `104430006202600001`). Project Berunda parses this field at ingestion to create instant spatial/temporal indexes [16, 17].
*   **PersonEntity Deduplication Logic:** The Entity Resolution Agent deduplicates `Accused` and `Victim` rows by applying phonetic name similarity blocks (to handle English/Kannada transliteration variations), matching age bands, and identifying spatial overlap. It assigns a confidence score before linking records in `PersonEntityLink` [14, 18].
*   **Strict Caste and Religion Governance:** `CasteID` and `ReligionID` are recorded in `ComplainantDetails` purely for statutory compliance (e.g., SC/ST Prevention of Atrocities Act reporting) [19, 20]. **Hard Constraint:** These fields are explicitly masked and banned from being used as features in the `RiskScore` models to prevent demographic profiling [21, 22].
*   **Graph Processing Query Optimization:** The `RelationshipEdge` and `PersonEntityLink` tables carry the link-analysis load. They are indexed to enable real-time network graph traversal without hitting the heavier `CaseMaster` tables [23, 24].

### 5. Storage Tiering & Architecture
To handle processing efficiency across Catalyst by Zoho, the data model is explicitly tiered [15, 25]:
1.  **Catalyst Data Store (Relational):** Hosts both the primary KSP Schema (`CaseMaster`, `Accused`, etc.) and the Berunda graph extensions (`PersonEntity`, `RelationshipEdge`) [15, 25].
2.  **Catalyst NoSQL:** Stores unstructured intelligence, OSINT captures, and the full-text `BriefFacts` from `Inv_OccuranceTime` to allow dynamic searching without schema rigidity [15, 25].
3.  **Catalyst Stratus (Object Storage):** Stores heavy multimedia, evidence files, and the automatically generated PDF case briefs [15, 25].
4.  **Catalyst Cache:** Maintains the `District`, `Unit`, and `Court` jurisdiction tables as they rarely change but are read continuously for dashboard filtering [15, 25].