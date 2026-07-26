import json
import os

import pytest


def get_template():
    template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'infra', 'catalyst', 'project-template.json')
    if not os.path.exists(template_path):
        pytest.skip("project-template.json not found")
    with open(template_path) as f:
        return json.load(f)

def test_no_incompatible_int_to_varchar():
    template = get_template()
    tables = template.get("datastore", [])

    # Check that any ActRef or SectionRef is a foreign key, not an INT
    for table in tables:
        for col in table.get("columns", []):
            if col["columnName"] in ["ActRef", "SectionRef"]:
                assert col["dataType"] == "foreign key", f"Column {col['columnName']} in {table['tableName']} must be a foreign key"

def test_crime_no_uniqueness():
    template = get_template()
    tables = template.get("datastore", [])
    case_master = next((t for t in tables if t["tableName"] == "CaseMaster"), None)
    assert case_master is not None
    crime_no_col = next((c for c in case_master["columns"] if c["columnName"] == "CrimeNo"), None)
    assert crime_no_col is not None
    assert crime_no_col["isUnique"] is True

def test_foreign_keys_point_to_parent_rowids():
    template = get_template()
    tables = template.get("datastore", [])
    valid_tables = [t["tableName"] for t in tables]

    for table in tables:
        for col in table.get("columns", []):
            if col["dataType"] == "foreign key":
                assert col["parentTable"] in valid_tables, f"Foreign key {col['columnName']} in {table['tableName']} points to invalid parent table {col['parentTable']}"

def test_one_to_many_relationships():
    # Verify that child tables have foreign keys to CaseMaster without unique constraints
    template = get_template()
    tables = template.get("datastore", [])

    accused_table = next((t for t in tables if t["tableName"] == "Accused"), None)
    assert accused_table is not None
    fk_col = next((c for c in accused_table["columns"] if c["columnName"] == "CaseMasterRef"), None)
    assert fk_col is not None
    assert fk_col.get("isUnique", False) is False  # Must not be unique for 1:N

def test_inv_occurrence_one_to_one():
    # Verify that Inv_OccurrenceTime has a unique foreign key to CaseMaster
    template = get_template()
    tables = template.get("datastore", [])

    occ_table = next((t for t in tables if t["tableName"] == "Inv_OccurrenceTime"), None)
    assert occ_table is not None
    fk_col = next((c for c in occ_table["columns"] if c["columnName"] == "CaseMasterRef"), None)
    assert fk_col is not None
    assert fk_col.get("isUnique") is True  # Must be unique for 1:1
