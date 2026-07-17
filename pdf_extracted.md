Police FIR System ΓÇö ER Diagram
DB schema
Entity Relationship Diagram ΓÇö Database Design Document
Karnataka Police Department
Color Legend
PK ΓÇö Primary Key Uniquely identifies each record in the table
FK ΓÇö Foreign Key References the Primary Key of another table
Alternate row Alternating row shading for readability
Normal column Regular data column with no key constraint
Table Definitions
CaseMaster
Column Name Type Key Description
CaseMasterID INT PK Primary key ΓÇö unique identifier for each FIR/case
Crime Number is assigned at the police station level and is
linked to the corresponding PoliceStationID. The Crime
Number follows a structured format consisting of:
1 digit Case Category Code + 4 digit District ID + 4 digit
Police Station ID (Unit ID) + 4 digit Year + 5 digit Running
Serial Number
CrimeNo VARCHAR A separate running serial number is maintained for each
police station, case category, and year.
Examples:
∩é╖ FIR: 104430006202600001
∩é╖ UDR: 304430006202600001
∩é╖ Zero FIR: 804430006202600001
∩é╖ PAR: 404430006202600001
The Case Number is generated at the police station level and
is associated with the corresponding PoliceStationID. For
each case category, a unique serial number is maintained per
CaseNo VARCHAR
police station and per year. The format is YYYY + 5-digit
running serial number (e.g., 202600001). (Last 9 digits
from CrimeNo)
CrimeRegisteredDate DATE Date when the FIR was registered
PolicePersonID INT FK FK ΓåÆ Employee.EmployeeID ΓÇö officer who registered the FIR
PoliceStationID INT FK FK ΓåÆ Unit.UnitID ΓÇö police station where FIR is registered
CaseCategoryID INT FK FK ΓåÆ CaseCategory.CaseCategoryID ΓÇö category
FK ΓåÆ GravityOffence.GravityOffenceID ΓÇö gravity level of the
GravityOffenceID INT FK
offence
FK ΓåÆ CrimeHead.CrimeHeadID ΓÇö major crime head
CrimeMajorHeadID INT FK
classification
FK ΓåÆ CrimeSubHead.CrimeSubHeadID ΓÇö minor crime sub-head
CrimeMinorHeadID INT FK
classification
FK ΓåÆ CaseStatusMaster.CaseStatusID ΓÇö current status of the
CaseStatusID INT FK
case
CourtID INT FK FK ΓåÆ Court.CourtID ΓÇö court where the case is being heard
Karnataka Police Department | Confidential

Police FIR System ΓÇö ER Diagram
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
IncidentFromDate  DATETIME    Start date and time of the incident
| IncidentToDate  | DATETIME  |   End date and time of the incident  |
| --------------- | --------- | ------------------------------------ |
Date and time when police station received information about the
| InfoReceivedPSDate  | DATETIME  |     |
| ------------------- | --------- | --- |
incident
latitude  DECIMAL    GPS latitude coordinate of the incident location
longitude  DECIMAL    GPS longitude coordinate of the incident location
| BriefFacts  | Nvarchar(Max)  |   Summary of the case  |
| ----------- | -------------- | ---------------------- |
ComplainantDetails
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
ComplainantID  INT  PK  Primary key ΓÇö unique identifier for the complainant
FK ΓåÆ CaseMaster.CaseMasterID ΓÇö FIR/case filed by this
| CaseMasterID  | INT  | FK  |
| ------------- | ---- | --- |
complainant
| ComplainantName  | VARCHAR  |   Full name of the complainant  |
| ---------------- | -------- | ------------------------------- |
| AgeYear          | INT      |   Age of the complainant        |
FK ΓåÆ OccupationMaster.OccupationID ΓÇö occupation of the
| OccupationID  | INT  | FK  |
| ------------- | ---- | --- |
complainant
ReligionID  INT  FK  FK ΓåÆ ReligionMaster.ReligionID ΓÇö religion of the complainant
CasteID  INT  FK  FK ΓåÆ CasteMaster.caste_master_id ΓÇö caste of the complainant
| GenderID  | INT  |   Gender of the complainant (lookup value)  |
| --------- | ---- | ------------------------------------------- |
ActSectionAssociation
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
FK ΓåÆ CaseMaster.CaseMasterID ΓÇö FIR/case this act-section
| CaseMasterID  | INT  | FK  |
| ------------- | ---- | --- |
applies to
ActID  INT  FK  FK ΓåÆ Act.ActCode ΓÇö legal act under which charges are framed
SectionID  INT  FK  FK ΓåÆ Section.SectionCode ΓÇö specific section of the act invoked
ActOrderID  INT  Display/print order of the act within the case

SectionOrderID  INT    Display/print order of the section under the act
Victim
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
VictimMasterID  INT  PK  Primary key ΓÇö unique identifier for each victim
CaseMasterID  INT  FK  FK ΓåÆ CaseMaster.CaseMasterID ΓÇö FIR/case this victim belongs to
| VictimName  | VARCHAR  |   Full name of the victim     |
| ----------- | -------- | ----------------------------- |
| AgeYear     | INT      |   Age of the victim in years  |
GenderID  INT    Gender of the victim (lookup value) like m, f, t
| VictimPolice  | VARCHAR  |   If Victim is police then 1else 0   |
| ------------- | -------- | ------------------------------------ |
Accused
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
AccusedMasterID  INT  PK  Primary key ΓÇö unique identifier for each accused person
CaseMasterID  INT  FK  FK ΓåÆ CaseMaster.CaseMasterID ΓÇö FIR/case this accused is linked
Karnataka Police Department | Confidential

Police FIR System ΓÇö ER Diagram
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
to
| AccusedName  | VARCHAR  |   Full name of the accused                |
| ------------ | -------- | ----------------------------------------- |
| AgeYear      | INT      |   Age of the accused                      |
| GenderID     | INT      | Gender of the accused mentioned as M/F/T  |

| PersonID  | VARCHAR  |   Accused Sorting like A1, A2, A3ΓÇª.  |
| --------- | -------- | ------------------------------------ |
ArrestSurrender
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
ArrestSurrenderID  INT  PK  Primary key ΓÇö unique identifier for each arrest/surrender event
FK ΓåÆ CaseMaster.CaseMasterID ΓÇö FIR/case linked to this
| CaseMasterID  | INT  | FK  |
| ------------- | ---- | --- |
arrest/surrender
ArrestSurrenderTypeID  INT  Type of event: arrest or voluntary surrender (lookup value)

| ArrestSurrenderDate  | DATE  |   Date of arrest or surrender  |
| -------------------- | ----- | ------------------------------ |
ArrestSurrenderStateId  INT  FK  FK ΓåÆ State.StateID ΓÇö state where arrest/surrender occurred
ArrestSurrenderDistrictId  INT  FK  FK ΓåÆ District.DistrictID ΓÇö district where arrest/surrender occurred
PoliceStationID  INT  FK  FK ΓåÆ Unit.UnitID ΓÇö police station handling the arrest
FK ΓåÆ Employee.EmployeeID ΓÇö Investigating Officer who made the
| IOID  | INT  | FK  |
| ----- | ---- | --- |
arrest
CourtID  INT  FK  FK ΓåÆ Court.CourtID ΓÇö court before which accused was produced
FK ΓåÆ Accused.AccusedMasterID ΓÇö accused person linked to this
| AccusedMasterID  | INT  | FK  |
| ---------------- | ---- | --- |
arrest/surrender
IsAccused  BIT  Flag (0/1): whether the person is the primary accused in the case

IsComplainantAccused  BIT    Flag (0/1): whether the complainant is also listed as accused
Act
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
ActCode  VARCHAR  PK  Primary key ΓÇö unique code for the legal act (e.g. IPC, NDPS)
ActDescription  VARCHAR    Full official name/description of the act
| ShortName  | VARCHAR  |   Abbreviated/common name of the act  |
| ---------- | -------- | ------------------------------------- |
Active  BIT    Whether the act is currently active and usable (1=Active, 0=Inactive)
Section
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
ActCode  VARCHAR  FK  FK ΓåÆ Act.ActCode ΓÇö parent act this section belongs to
| SectionCode         | VARCHAR  |   Section number/code (e.g. 302, 307)  |
| ------------------- | -------- | -------------------------------------- |
| SectionDescription  | VARCHAR  |   Full description of the section      |
Active  BIT    Whether the section is currently active (1=Active, 0=Inactive)
CrimeHeadActSection
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
FK ΓåÆ CrimeHead.CrimeHeadID ΓÇö crime head this act-section
| CrimeHeadID  | INT  | FK  |
| ------------ | ---- | --- |
combination maps to
Karnataka Police Department | Confidential

Police FIR System ΓÇö ER Diagram
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
ActCode  VARCHAR  FK  FK ΓåÆ Act.ActCode ΓÇö legal act linked to this crime head
SectionCode  VARCHAR    Section code from the act applicable to this crime head

CrimeHead
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
CrimeHeadID  INT  PK  Primary key ΓÇö unique identifier for the major crime head
CrimeGroupName  VARCHAR    Name of the crime group/major head (e.g. Crimes Against Body)
Active  BIT    Whether this crime head is active (1=Active, 0=Inactive)
CrimeSubHead
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
CrimeSubHeadID  INT  PK  Primary key ΓÇö unique identifier for the crime sub-head
FK ΓåÆ CrimeHead.CrimeHeadID ΓÇö parent major crime head this
| CrimeHeadID  | INT  | FK  |
| ------------ | ---- | --- |
belongs to
CrimeHeadName  VARCHAR    Name of this crime sub-head (e.g. Murder, Robbery)
SeqID  INT    Display/sort sequence number for ordering sub-heads
CasteMaster
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for each caste. Referenced by
| caste_master_id  | INT  | PK  |
| ---------------- | ---- | --- |
ComplainantDetails.CasteID
| caste_master_name  | VARCHAR  |   Name of the caste  |
| ------------------ | -------- | -------------------- |
ReligionMaster
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for each religion. Referenced by
| ReligionID  | INT  | PK  |
| ----------- | ---- | --- |
ComplainantDetails.ReligionID
ReligionName  VARCHAR    Name of the religion (e.g. Hindu, Muslim, Christian)
OccupationMaster
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
OccupationID  Primary key ΓÇö unique identifier for each occupation. Referenced by
|     | INT  | PK  |
| --- | ---- | --- |
ComplainantDetails.OccupationID
OccupationName  VARCHAR    Name of the occupation (e.g. Farmer, Government Employee)
CaseStatusMaster
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for each case status. Referenced by
| CaseStatusID  | INT  | PK  |
| ------------- | ---- | --- |
CaseMaster.CaseStatusID
Name of the status (e.g. Under Investigation, Charge Sheeted,
| CaseStatusName  | VARCHAR  |     |
| --------------- | -------- | --- |
Closed)
Karnataka Police Department | Confidential

Police FIR System ΓÇö ER Diagram
Court
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the court. Referenced by
| CourtID  | INT  | PK  |
| -------- | ---- | --- |
CaseMaster.CourtID, ArrestSurrender.CourtID
| CourtName  | VARCHAR  |   Full name of the court  |
| ---------- | -------- | ------------------------- |
DistrictID  INT  FK  FK ΓåÆ District.DistrictID ΓÇö district where the court is located
StateID  INT  FK  FK ΓåÆ State.StateID ΓÇö state where the court is located
Active  BIT    Whether the court is active (1=Active, 0=Inactive)
District
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the district. Referenced by Court,
| DistrictID  | INT  | PK  |
| ----------- | ---- | --- |
Unit, Employee, ArrestSurrender
| DistrictName  | VARCHAR  |   Name of the district  |
| ------------- | -------- | ----------------------- |
StateID  INT  FK  FK ΓåÆ State.StateID ΓÇö state this district belongs to
Active  BIT    Whether the district record is active (1=Active, 0=Inactive)
State
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the state. Referenced by Court,
| StateID  | INT  | PK  |
| -------- | ---- | --- |
District, Unit, ArrestSurrender
| StateName      | VARCHAR  |   Name of the state         |
| -------------- | -------- | --------------------------- |
| NationalityID  | INT      |   Nationality reference ID  |
Active  BIT    Whether the state record is active (1=Active, 0=Inactive)
Unit
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the police unit. Referenced by
UnitID  INT  PK  CaseMaster.PoliceStationID, Employee.UnitID,
ArrestSurrender.PoliceStationID
| UnitName  | VARCHAR  | Name of the unit or police station  |
| --------- | -------- | ----------------------------------- |

TypeID  INT  FK  FK ΓåÆ UnitType.UnitTypeID ΓÇö type/category of the unit
ParentUnit  INT    Parent unit ID for hierarchy (self-reference to UnitID)
| NationalityID  | INT  |   Nationality reference ID  |
| -------------- | ---- | --------------------------- |
StateID  INT  FK  FK ΓåÆ State.StateID ΓÇö state the unit belongs to
DistrictID  INT  FK  FK ΓåÆ District.DistrictID ΓÇö district the unit belongs to
Active  BIT    Whether the unit is active (1=Active, 0=Inactive)
UnitType
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the unit type. Referenced by
| UnitTypeID  | INT  | PK  |
| ----------- | ---- | --- |
Unit.TypeID
UnitTypeName  VARCHAR    Name of the unit type (e.g. Police Station, Circle Office)
CityDistState  VARCHAR    Operational level: City / District / State
Karnataka Police Department | Confidential

Police FIR System ΓÇö ER Diagram
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Hierarchy  INT    Hierarchy level number (lower = higher authority)
Active  BIT    Whether the unit type is active (1=Active, 0=Inactive)
Rank
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the rank. Referenced by
| RankID  | INT  | PK  |
| ------- | ---- | --- |
Employee.RankID
RankName  VARCHAR    Name of the police rank (e.g. Constable, Inspector, DSP)
Hierarchy  INT    Rank hierarchy level (lower = higher rank)
Active  BIT    Whether the rank is active (1=Active, 0=Inactive)

Designation
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the designation. Referenced by
| DesignationID  | INT  | PK  |
| -------------- | ---- | --- |
Employee.DesignationID
DesignationName  VARCHAR    Name of the designation (e.g. Investigating Officer, SHO)
Active  BIT    Whether the designation is active (1=Active, 0=Inactive)
| SortOrder  | INT  |   Display sort order for dropdowns/reports  |
| ---------- | ---- | ------------------------------------------- |
Employee
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the police employee. Referenced
| EmployeeID  | INT  | PK  |
| ----------- | ---- | --- |
by CaseMaster.PolicePersonID, ArrestSurrender.IOID
FK ΓåÆ District.DistrictID ΓÇö district the employee is currently posted
| DistrictID  | INT  | FK  |
| ----------- | ---- | --- |
in
UnitID  INT  FK  FK ΓåÆ Unit.UnitID ΓÇö unit/police station the employee is assigned to
RankID  INT  FK ΓåÆ Rank.RankID ΓÇö current rank of the employee
FK
FK ΓåÆ Designation.DesignationID ΓÇö current designation of the
| DesignationID  | INT  | FK  |
| -------------- | ---- | --- |
employee
KGID  VARCHAR    Karnataka Government ID (unique government employee number)
| FirstName  | VARCHAR  | First name of the employee  |
| ---------- | -------- | --------------------------- |

| EmployeeDOB  | DATE  |   Date of birth of the employee          |
| ------------ | ----- | ---------------------------------------- |
| GenderID     | INT   |   Gender of the employee (lookup value)  |
BloodGroupID  INT    Blood group of the employee (lookup value)
PhysicallyChallenged  BIT    Flag: whether the employee is physically challenged (1=Yes, 0=No)
AppointmentDate  DATE    Date of appointment to government service
CaseCategory
| Column Name  | Type  | Key  Description  |
| ------------ | ----- | ----------------- |
Primary key ΓÇö unique identifier for the case category. Referenced
| CaseCategoryID  | INT  | PK  |
| --------------- | ---- | --- |
by CaseMaster.CaseCategoryID
Karnataka Police Department | Confidential

Police FIR System ΓÇö ER Diagram
Column Name Type Key Description
LookupValue VARCHAR Category name (FIR, UDR, PAR..)
GravityOffence
Column Name Type Key Description
Primary key ΓÇö unique identifier for the gravity level. Referenced by
GravityOffenceID INT PK
CaseMaster.GravityOffenceID
LookupValue VARCHAR Gravity description (e.g. Heinous, Non-Heinous)
ChargesheetDetails
Column Name Type Key Description
CSID INT PK Primary key ΓÇö unique identifier for the chargesheet
FK ΓåÆ CaseMaster.CaseMasterID ΓÇö FIR/case filed by this
CaseMasterID INT FK
complainant
csdate DATETIME Chargesheeted date
cstype CHAR Final report type A-> Chargesheet, B->False Case, C->Undetected
PolicePersonID INT FK FK ΓåÆ employeeMaster.employee ID
Relationship Matrix
Defines all foreign key relationships between tables, including cardinality and a brief description.
Relationshi
Parent Table Parent Column Child Table Child Column Description
p
One FIR can
CaseMaster CaseMasterID One to Many Victim CaseMasterID have multiple
victims
One FIR can
CaseMaster CaseMasterID One to Many Accused CaseMasterID
have multiple
accused
persons
One FIR can
CaseMaster CaseMasterID One to Many ArrestSurrender CaseMasterID
have multiple
arrest/surrend
er events
One FIR can
CaseMaster CaseMasterID One to Many ComplainantDetails CaseMasterID have multiple
complainants
One FIR can
CaseMaster CaseMasterID One to Many ActSectionAssociation CaseMasterID invoke multiple
act-sections
One FIR has
one
CaseMaster CaseMasterID One to One Inv_OccuranceTime CaseMasterID occurrence
time/location
record
Karnataka Police Department | Confidential

Police FIR System ΓÇö ER Diagram
Relationshi
Parent Table  Parent Column  Child Table  Child Column  Description
p
Many FIRs
CaseMaster  CaseCategoryID  Many to One  CaseCategory  CaseCategoryID  can share the
same category
Many FIRs
|             |                   |              |                 | GravityOffenceI | can have the  |
| ----------- | ----------------- | ------------ | --------------- | --------------- | ------------- |
| CaseMaster  | GravityOffenceID  | Many to One  | GravityOffence  |                 |               |
|             |                   |              |                 | D               | same gravity  |
level
Many FIRs
CaseMaster  CrimeMajorHeadID  Many to One  CrimeHead  CrimeHeadID  can share the
same major
crime head
Many FIRs
|             |                   |              |               | CrimeSubHeadI | can share the  |
| ----------- | ----------------- | ------------ | ------------- | ------------- | -------------- |
| CaseMaster  | CrimeMinorHeadID  | Many to One  | CrimeSubHead  |               |                |
|             |                   |              |               | D             | same crime     |
sub-head
Many FIRs
CaseMaster  CaseStatusID  Many to One  CaseStatusMaster  CaseStatusID
can have the
same status
Many FIRs
CaseMaster  CourtID  Many to One  Court  CourtID  can be tried in
the same court
Many FIRs
can be
CaseMaster  PolicePersonID  Many to One  Employee  EmployeeID  registered by
the same
employee
One arrest
AccusedMasterID(via  inv_arrestsurrenderaccus ArrestSurrenderI event can link
| ArrestSurrender  |            | One to Many  |     |     | multiple  |
| ---------------- | ---------- | ------------ | --- | --- | --------- |
|                  | junction)  |              | ed  | D   |           |
accused via
junction
Junction links
| i n v _arrestsurrenderaccus |                    |              |                  | A r restSurrenderI | t o   t h e          |
| --------------------------- | ------------------ | ------------ | ---------------- | ------------------ | -------------------- |
|                             | ArrestSurrenderID  | Many to One  | ArrestSurrender  |                    |                      |
| e d                         |                    |              |                  | D                  | a r r e s t /surrend |
er event
Many arrest
ArrestSurrender  ArrestSurrenderStateId  Many to One  State  StateID  events can
occur in the
same state
Many arrest
|                  | ArrestSurrenderDistrict |              |           |             | events can    |
| ---------------- | ----------------------- | ------------ | --------- | ----------- | ------------- |
| ArrestSurrender  |                         | Many to One  | District  | DistrictID  |               |
|                  | Id                      |              |           |             | occur in the  |
same district
Accused may
| ArrestSurrender  | CourtID  | Many to One  | Court  | CourtID  |     |
| ---------------- | -------- | ------------ | ------ | -------- | --- |
be produced
before a court
Many arrests
ArrestSurrender  IOID  Many to One  Employee  EmployeeID  can be made
by the same
IO
Many
complainants
ComplainantDetails  OccupationID  Many to One  OccupationMaster  OccupationID  can share the
same
occupation
Many
ComplainantDetails  ReligionID  Many to One  ReligionMaster  ReligionID  complainants
can share the
same religion
Many
ComplainantDetails  CasteID  Many to One  CasteMaster  caste_master_id  complainants
can belong to
Karnataka Police Department | Confidential

Police FIR System ΓÇö ER Diagram
Relationshi
Parent Table Parent Column Child Table Child Column Description
p
the same
caste
Many case-
ActSectionAssociation ActID Many to One Act ActCode
sections can
reference the
same act
Many cases
ActSectionAssociation SectionID Many to One Section SectionCode can use the
same section
Multiple sub-
heads fall
CrimeSubHead CrimeHeadID Many to One CrimeHead CrimeHeadID under one
major crime
head
One crime
CrimeHead CrimeHeadID One to Many CrimeHeadActSection CrimeHeadID
head can map
to multiple act-
sections
One act can
Act ActCode One to Many CrimeHeadActSection ActCode
be linked to
multiple crime
heads
One act
Act ActCode One to Many Section ActCode
contains
multiple
sections
Many courts
Court DistrictID Many to One District DistrictID can be in the
same district
Many districts
District StateID Many to One State StateID belong to one
state
Many units
Unit TypeID Many to One UnitType UnitTypeID share the
same unit type
Many units are
Unit StateID Many to One State StateID located in the
same state
Many units
Unit DistrictID Many to One District DistrictID belong to the
same district
Many
Employee DistrictID Many to One District DistrictID
employees
posted in the
same district
Many
Employee UnitID Many to One Unit UnitID
employees
assigned to
the same unit
Many
Employee RankID Many to One Rank RankID
employees
can hold the
same rank
Many
employees
Employee DesignationID Many to One Designation DesignationID can have the
same
designation
Karnataka Police Department | Confidential
