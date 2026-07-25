# Catalyst Data Store Schema Mapping

*Note: Every table automatically gets a Catalyst `ROWID` (BigInt) primary key. All Catalyst `Foreign Key` columns map implicitly to the target table's `ROWID`.*

## Phase A: Independent Master Tables

| ER Table | Catalyst Table | ER Field / New Field | Catalyst Field | Type | Parent Table | Constraints / Settings | On Delete | Reason / Note |
|---|---|---|---|---|---|---|---|---|
| State | State | StateID | StateID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | StateName | StateName | Var Char | - | Mandatory | - | |
| UnitType | UnitType | UnitTypeID | UnitTypeID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | UnitTypeName | UnitTypeName | Var Char | - | Mandatory | - | |
| Rank | Rank | RankID | RankID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | RankName | RankName | Var Char | - | Mandatory | - | |
| Designation | Designation | DesignationID | DesignationID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | DesignationName | DesignationName | Var Char | - | Mandatory | - | |
| CaseCategory | CaseCategory | CaseCategoryID | CaseCategoryID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | CategoryName | CategoryName | Var Char | - | Mandatory | - | |
| GravityOffence | GravityOffence | GravityOffenceID | GravityOffenceID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | GravityName | GravityName | Var Char | - | Mandatory | - | |
| CaseStatusMaster | CaseStatusMaster | CaseStatusID | CaseStatusID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | StatusName | StatusName | Var Char | - | Mandatory | - | |
| CrimeHead | CrimeHead | CrimeHeadID | CrimeHeadID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | HeadName | HeadName | Var Char | - | Mandatory | - | |
| Act | Act | ActCode | ActCode | Var Char | - | Unique, Mandatory, Search Index | - | ER VARCHAR -> Var Char |
| | | ActName | ActName | Var Char | - | Mandatory | - | |
| OccupationMaster | OccupationMaster | OccupationID | OccupationID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | OccupationName | OccupationName | Var Char | - | Mandatory | - | |
| ReligionMaster | ReligionMaster | ReligionID | ReligionID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | ReligionName | ReligionName | Var Char | - | Mandatory | - | |
| CasteMaster | CasteMaster | CasteID | CasteID | Int | - | Unique, Mandatory, Search Index | - | ER INT -> Int |
| | | CasteName | CasteName | Var Char | - | Mandatory | - | |
| GenderMaster | GenderMaster | GenderID | GenderID | Int | - | Unique, Mandatory, Search Index | - | Added per prompt |
| | | GenderName | GenderName | Var Char | - | Mandatory | - | |
| BloodGroupMaster | BloodGroupMaster | BloodGroupID | BloodGroupID | Int | - | Unique, Mandatory, Search Index | - | Added per prompt |
| | | BloodGroupName | BloodGroupName | Var Char | - | Mandatory | - | |
| NationalityMaster | NationalityMaster | NationalityID | NationalityID | Int | - | Unique, Mandatory, Search Index | - | Added per prompt |
| | | NationalityName | NationalityName | Var Char | - | Mandatory | - | |
| ArrestSurrenderTypeMaster | ArrestSurrenderTypeMaster | TypeID | TypeID | Int | - | Unique, Mandatory, Search Index | - | Added per prompt |
| | | TypeName | TypeName | Var Char | - | Mandatory | - | |

## Phase B: Dependent Master Tables

| ER Table | Catalyst Table | ER Field / New Field | Catalyst Field | Type | Parent Table | Constraints / Settings | On Delete | Reason / Note |
|---|---|---|---|---|---|---|---|---|
| District | District | DistrictID | DistrictID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | DistrictName | DistrictName | Var Char | - | Mandatory | - | |
| | | StateID | StateRef | Foreign Key | State | Mandatory | Restrict | Catalyst FK requirement |
| Unit | Unit | UnitID | UnitID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | UnitName | UnitName | Var Char | - | Mandatory | - | |
| | | DistrictID | DistrictRef | Foreign Key | District | Mandatory | Restrict | Catalyst FK requirement |
| | | UnitTypeID | UnitTypeRef | Foreign Key | UnitType | Mandatory | Restrict | Catalyst FK requirement |
| | | ParentUnit | ParentUnitRef | Foreign Key | Unit | - | Set Null | Explicitly added self-ref |
| Court | Court | CourtID | CourtID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | CourtName | CourtName | Var Char | - | Mandatory | - | |
| | | DistrictID | DistrictRef | Foreign Key | District | Mandatory | Restrict | Catalyst FK requirement |
| CrimeSubHead | CrimeSubHead | CrimeSubHeadID | CrimeSubHeadID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | SubHeadName | SubHeadName | Var Char | - | Mandatory | - | |
| | | CrimeHeadID | CrimeHeadRef | Foreign Key | CrimeHead | Mandatory | Restrict | Catalyst FK requirement |
| Section | Section | SectionCode | SectionCode | Var Char | - | Mandatory, Search Index | - | ER VARCHAR -> Var Char |
| | | SectionName | SectionName | Var Char | - | Mandatory | - | |
| | | ActID (INT) | ActRef | Foreign Key | Act | Mandatory | Restrict | Fixed INT-to-VARCHAR issue |
| | | [NEW] | SectionKey | Var Char | - | Unique, Mandatory, Search Index | - | Format: `ActCode:SectionCode` |
| Employee | Employee | EmployeeID | EmployeeID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | EmployeeName | EmployeeName | Var Char | - | Mandatory, PII enabled | - | |
| | | RankID | RankRef | Foreign Key | Rank | Mandatory | Restrict | Catalyst FK requirement |
| | | DesignationID | DesignationRef | Foreign Key | Designation | Mandatory | Restrict | Catalyst FK requirement |
| | | UnitID | UnitRef | Foreign Key | Unit | Mandatory | Restrict | Catalyst FK requirement |

## Phase C: Core Case Tables

| ER Table | Catalyst Table | ER Field / New Field | Catalyst Field | Type | Parent Table | Constraints / Settings | On Delete | Reason / Note |
|---|---|---|---|---|---|---|---|---|
| CaseMaster | CaseMaster | CaseMasterID | CaseMasterID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | CrimeNo | CrimeNo | Var Char | - | Unique, Mandatory, Search Index | - | ER VARCHAR |
| | | CaseNo | CaseNo | Var Char | - | Mandatory | - | |
| | | CrimeRegisteredDate | CrimeRegisteredDate | Date | - | Mandatory | - | ER DATE -> Date |
| | | PolicePersonRef | PolicePersonRef | Foreign Key | Employee | Mandatory | Restrict | Catalyst FK requirement |
| | | PoliceStationRef | PoliceStationRef | Foreign Key | Unit | Mandatory | Restrict | Catalyst FK requirement |
| | | CaseCategoryRef | CaseCategoryRef | Foreign Key | CaseCategory | Mandatory | Restrict | Catalyst FK requirement |
| | | GravityOffenceRef | GravityOffenceRef | Foreign Key | GravityOffence | Mandatory | Restrict | Catalyst FK requirement |
| | | CrimeMajorHeadRef | CrimeMajorHeadRef | Foreign Key | CrimeHead | Mandatory | Restrict | Catalyst FK requirement |
| | | CrimeMinorHeadRef | CrimeMinorHeadRef | Foreign Key | CrimeSubHead | Mandatory | Restrict | Catalyst FK requirement |
| | | CaseStatusRef | CaseStatusRef | Foreign Key | CaseStatusMaster | Mandatory | Restrict | Catalyst FK requirement |
| | | CourtRef | CourtRef | Foreign Key | Court | - | Restrict | Catalyst FK requirement |
| Inv_OccuranceTime | Inv_OccurrenceTime | CaseMasterID | CaseMasterRef | Foreign Key | CaseMaster | Unique, Mandatory | Cascade | Corrected spelling |
| | | IncidentFromDate | IncidentFromDate | DateTime | - | - | - | ER DATETIME -> DateTime |
| | | IncidentToDate | IncidentToDate | DateTime | - | - | - | ER DATETIME -> DateTime |
| | | InfoReceivedPSDate | InfoReceivedPSDate | DateTime | - | - | - | ER DATETIME -> DateTime |
| | | Latitude | Latitude | Double | - | - | - | ER DECIMAL -> Double |
| | | Longitude | Longitude | Double | - | - | - | ER DECIMAL -> Double |
| | | BriefFacts | BriefFacts | Encrypted Text | - | PII enabled | - | ER NVARCHAR(MAX) -> Encrypted Text |
| ComplainantDetails | ComplainantDetails | ComplainantID | ComplainantID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | CaseMasterID | CaseMasterRef | Foreign Key | CaseMaster | Mandatory | Cascade | Catalyst FK requirement |
| | | Name | Name | Var Char | - | Mandatory, PII enabled | - | |
| | | Age | Age | Int | - | PII enabled | - | |
| | | Gender | GenderRef | Foreign Key | GenderMaster | - | Restrict | FK link to new GenderMaster |
| | | Nationality | NationalityRef | Foreign Key | NationalityMaster | - | Restrict | FK link to new NationalityMaster |
| | | Religion | ReligionRef | Foreign Key | ReligionMaster | - | Restrict | Catalyst FK requirement |
| | | Caste | CasteRef | Foreign Key | CasteMaster | - | Restrict | Catalyst FK requirement |
| | | Occupation | OccupationRef | Foreign Key | OccupationMaster | - | Restrict | Catalyst FK requirement |
| Victim | Victim | VictimID | VictimID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | CaseMasterID | CaseMasterRef | Foreign Key | CaseMaster | Mandatory | Cascade | Catalyst FK requirement |
| | | Name | Name | Var Char | - | Mandatory, PII enabled | - | |
| | | Age | Age | Int | - | PII enabled | - | |
| | | Gender | GenderRef | Foreign Key | GenderMaster | - | Restrict | FK link to new GenderMaster |
| | | Nationality | NationalityRef | Foreign Key | NationalityMaster | - | Restrict | FK link to new NationalityMaster |
| | | Religion | ReligionRef | Foreign Key | ReligionMaster | - | Restrict | Catalyst FK requirement |
| | | Caste | CasteRef | Foreign Key | CasteMaster | - | Restrict | Catalyst FK requirement |
| | | Occupation | OccupationRef | Foreign Key | OccupationMaster | - | Restrict | Catalyst FK requirement |
| Accused | Accused | AccusedID | AccusedID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | CaseMasterID | CaseMasterRef | Foreign Key | CaseMaster | Mandatory | Cascade | Catalyst FK requirement |
| | | Name | Name | Var Char | - | Mandatory, PII enabled | - | |
| | | Age | Age | Int | - | PII enabled | - | |
| | | Gender | GenderRef | Foreign Key | GenderMaster | - | Restrict | FK link to new GenderMaster |
| | | Nationality | NationalityRef | Foreign Key | NationalityMaster | - | Restrict | FK link to new NationalityMaster |
| | | Religion | ReligionRef | Foreign Key | ReligionMaster | - | Restrict | Catalyst FK requirement |
| | | Caste | CasteRef | Foreign Key | CasteMaster | - | Restrict | Catalyst FK requirement |
| | | Occupation | OccupationRef | Foreign Key | OccupationMaster | - | Restrict | Catalyst FK requirement |
| ArrestSurrender | ArrestSurrender | ArrestSurrenderID | ArrestSurrenderID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | CaseMasterID | CaseMasterRef | Foreign Key | CaseMaster | Mandatory | Cascade | Catalyst FK requirement |
| | | TypeID | TypeRef | Foreign Key | ArrestSurrenderTypeMaster | Mandatory | Restrict | FK link to new master |
| | | DateOfArrest | DateOfArrest | DateTime | - | Mandatory | - | ER DATETIME -> DateTime |
| | | EmployeeID | PolicePersonRef | Foreign Key | Employee | Mandatory | Restrict | Catalyst FK requirement |
| | | AccusedMasterID | [REMOVED] | - | - | - | - | Replaced by Junction Table |
| ChargesheetDetails | ChargesheetDetails | ChargesheetID | ChargesheetID | BigInt | - | Unique, Mandatory, Search Index | - | ER INT -> BigInt |
| | | CaseMasterID | CaseMasterRef | Foreign Key | CaseMaster | Mandatory | Cascade | Catalyst FK requirement |
| | | ChargesheetDate | ChargesheetDate | Date | - | Mandatory | - | ER DATE -> Date |
| | | PolicePersonID | PolicePersonRef | Foreign Key | Employee | Mandatory | Restrict | Fixed naming to Employee ref |

## Phase D: Association Tables

| ER Table | Catalyst Table | ER Field / New Field | Catalyst Field | Type | Parent Table | Constraints / Settings | On Delete | Reason / Note |
|---|---|---|---|---|---|---|---|---|
| ActSectionAssociation | ActSectionAssociation | CaseMasterID | CaseMasterRef | Foreign Key | CaseMaster | Mandatory | Cascade | Catalyst FK requirement |
| | | ActID (INT) | ActRef | Foreign Key | Act | Mandatory | Restrict | Fixed INT to Catalyst FK |
| | | SectionID (INT) | SectionRef | Foreign Key | Section | Mandatory | Restrict | Fixed INT to Catalyst FK |
| CrimeHeadActSection | CrimeHeadActSection | CrimeSubHeadID | CrimeSubHeadRef | Foreign Key | CrimeSubHead | Mandatory | Cascade | Catalyst FK requirement |
| | | ActID (INT) | ActRef | Foreign Key | Act | Mandatory | Restrict | Fixed INT to Catalyst FK |
| | | SectionID (INT) | SectionRef | Foreign Key | Section | Mandatory | Restrict | Fixed INT to Catalyst FK |
| ArrestSurrenderAccused | ArrestSurrenderAccused | [NEW] | ArrestSurrenderRef | Foreign Key | ArrestSurrender | Mandatory | Cascade | Created new junction table |
| | | [NEW] | AccusedRef | Foreign Key | Accused | Mandatory | Cascade | Created new junction table |
| | | [NEW] | IsPrimaryAccused | Boolean | - | - | - | Metadata flag |
| | | [NEW] | IsComplainantAccused| Boolean | - | - | - | Metadata flag |
