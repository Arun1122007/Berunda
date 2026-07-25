import json
import os

tables = []

def create_table(name, columns):
    tables.append({
        "tableName": name,
        "columns": columns,
        "permissions": {
            "insert": ["App Administrator", "Investigating Officer"],
            "select": ["App Administrator", "Investigating Officer", "Police Analyst", "Read Only Auditor", "Demo User"],
            "update": ["App Administrator", "Investigating Officer"],
            "delete": ["App Administrator"]
        }
    })

# Phase A
create_table("State", [
    {"columnName": "StateID", "dataType": "bigint", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "StateName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False}
])
create_table("UnitType", [
    {"columnName": "UnitTypeID", "dataType": "int", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "UnitTypeName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False}
])
create_table("CaseCategory", [
    {"columnName": "CaseCategoryID", "dataType": "int", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "CategoryName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False}
])
create_table("GravityOffence", [
    {"columnName": "GravityOffenceID", "dataType": "int", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "GravityName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False}
])
create_table("CaseStatusMaster", [
    {"columnName": "CaseStatusID", "dataType": "int", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "StatusName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False}
])
create_table("CrimeHead", [
    {"columnName": "CrimeHeadID", "dataType": "bigint", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "HeadName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False}
])
create_table("Act", [
    {"columnName": "ActCode", "dataType": "varchar", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "ActName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False}
])

# Just representative subset of master tables for brevity, plus core tables

create_table("District", [
    {"columnName": "DistrictID", "dataType": "bigint", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "DistrictName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False},
    {"columnName": "StateRef", "dataType": "foreign key", "parentTable": "State", "isMandatory": True, "onDelete": "restrict"}
])

create_table("Unit", [
    {"columnName": "UnitID", "dataType": "bigint", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "UnitName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False},
    {"columnName": "DistrictRef", "dataType": "foreign key", "parentTable": "District", "isMandatory": True, "onDelete": "restrict"},
    {"columnName": "UnitTypeRef", "dataType": "foreign key", "parentTable": "UnitType", "isMandatory": True, "onDelete": "restrict"},
    {"columnName": "ParentUnitRef", "dataType": "foreign key", "parentTable": "Unit", "isMandatory": False, "onDelete": "set null"}
])

create_table("Employee", [
    {"columnName": "EmployeeID", "dataType": "bigint", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "EmployeeName", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False, "isPII": True},
    {"columnName": "UnitRef", "dataType": "foreign key", "parentTable": "Unit", "isMandatory": True, "onDelete": "restrict"}
])

create_table("CaseMaster", [
    {"columnName": "CaseMasterID", "dataType": "bigint", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "CrimeNo", "dataType": "varchar", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "CaseNo", "dataType": "varchar", "isMandatory": True, "isUnique": False, "isSearchIndex": False},
    {"columnName": "CrimeRegisteredDate", "dataType": "date", "isMandatory": True, "isUnique": False, "isSearchIndex": False},
    {"columnName": "PolicePersonRef", "dataType": "foreign key", "parentTable": "Employee", "isMandatory": True, "onDelete": "restrict"},
    {"columnName": "PoliceStationRef", "dataType": "foreign key", "parentTable": "Unit", "isMandatory": True, "onDelete": "restrict"}
])

create_table("Inv_OccurrenceTime", [
    {"columnName": "CaseMasterRef", "dataType": "foreign key", "parentTable": "CaseMaster", "isMandatory": True, "isUnique": True, "onDelete": "cascade"},
    {"columnName": "IncidentFromDate", "dataType": "datetime", "isMandatory": False, "isUnique": False, "isSearchIndex": False},
    {"columnName": "IncidentToDate", "dataType": "datetime", "isMandatory": False, "isUnique": False, "isSearchIndex": False},
    {"columnName": "BriefFacts", "dataType": "encrypted text", "isMandatory": False, "isUnique": False, "isSearchIndex": False, "isPII": True}
])

create_table("Accused", [
    {"columnName": "AccusedID", "dataType": "bigint", "isMandatory": True, "isUnique": True, "isSearchIndex": True},
    {"columnName": "CaseMasterRef", "dataType": "foreign key", "parentTable": "CaseMaster", "isMandatory": True, "onDelete": "cascade"},
    {"columnName": "Name", "dataType": "varchar", "isMandatory": True, "isPII": True},
    {"columnName": "Age", "dataType": "int", "isPII": True}
])

template = {
    "datastore": tables
}

output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "infra", "catalyst", "project-template.json")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(template, f, indent=4)

print(f"Generated Catalyst IaC template at {output_path}")
