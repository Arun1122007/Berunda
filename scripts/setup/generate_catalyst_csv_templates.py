import csv
import os

# Define all 27 tables and their exact columns from the official PDF
schema = {
    "CaseMaster": ["CaseMasterID", "CrimeNo", "CaseNo", "CrimeRegisteredDate", "PolicePersonID", "PoliceStationID", "CaseCategoryID", "GravityOffenceID", "CrimeMajorHeadID", "CrimeMinorHeadID", "CaseStatusID", "CourtID"],
    "ComplainantDetails": ["ComplainantID", "CaseMasterID", "ComplainantName", "AgeYear", "OccupationID", "ReligionID", "CasteID", "GenderID"],
    "ActSectionAssociation": ["CaseMasterID", "ActID", "SectionID", "ActOrderID", "SectionOrderID"],
    "Victim": ["VictimMasterID", "CaseMasterID", "VictimName", "AgeYear", "GenderID", "VictimPolice"],
    "Accused": ["AccusedMasterID", "CaseMasterID", "AccusedName", "AgeYear", "GenderID", "PersonID"],
    "ArrestSurrender": ["ArrestSurrenderID", "CaseMasterID", "ArrestSurrenderTypeID", "ArrestSurrenderDate", "ArrestSurrenderStateId", "ArrestSurrenderDistrictId", "PoliceStationID", "IOID", "CourtID", "AccusedMasterID", "IsAccused", "IsComplainantAccused"],
    "Act": ["ActCode", "ActDescription", "ShortName", "Active"],
    "Section": ["ActCode", "SectionCode", "SectionDescription", "Active"],
    "CrimeHeadActSection": ["CrimeHeadID", "ActCode", "SectionCode"],
    "CrimeHead": ["CrimeHeadID", "CrimeGroupName", "Active"],
    "CrimeSubHead": ["CrimeSubHeadID", "CrimeHeadID", "CrimeHeadName", "SeqID"],
    "CasteMaster": ["caste_master_id", "caste_master_name"],
    "ReligionMaster": ["ReligionID", "ReligionName"],
    "OccupationMaster": ["OccupationID", "OccupationName"],
    "CaseStatusMaster": ["CaseStatusID", "CaseStatusName"],
    "Court": ["CourtID", "CourtName", "DistrictID", "StateID", "Active"],
    "District": ["DistrictID", "DistrictName", "StateID", "Active"],
    "State": ["StateID", "StateName", "NationalityID", "Active"],
    "Unit": ["UnitID", "UnitName", "TypeID", "ParentUnit", "NationalityID", "StateID", "DistrictID", "Active"],
    "UnitType": ["UnitTypeID", "UnitTypeName", "CityDistState"],
    "Rank": ["RankID", "RankName", "Hierarchy", "Active"],
    "Designation": ["DesignationID", "DesignationName", "Active", "SortOrder"],
    "Employee": ["EmployeeID", "DistrictID", "UnitID", "RankID", "DesignationID", "KGID", "FirstName", "EmployeeDOB", "GenderID", "BloodGroupID", "PhysicallyChallenged", "AppointmentDate"],
    "CaseCategory": ["CaseCategoryID", "LookupValue"],
    "GravityOffence": ["GravityOffenceID", "LookupValue"],
    "ChargesheetDetails": ["CSID", "CaseMasterID", "csdate", "cstype", "PolicePersonID"],
    "Inv_OccuranceTime": ["CaseMasterID", "IncidentFromDate", "IncidentToDate", "InfoReceivedPSDate", "latitude", "longitude", "BriefFacts"]
}

output_dir = os.path.join("data", "catalyst_csvs")
os.makedirs(output_dir, exist_ok=True)

print("Generating 27 CSV templates for Zoho Catalyst Data Store...")

for table_name, columns in schema.items():
    file_path = os.path.join(output_dir, f"{table_name}.csv")
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)

        # Catalyst requires at least 1 row of dummy data to infer types during bulk import.
        # We will write an empty row so it doesn't fail parsing.
        writer.writerow([""] * len(columns))

print(f"Successfully generated 27 CSV templates in '{output_dir}'.")
