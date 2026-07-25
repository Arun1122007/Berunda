import os
import json

def verify_schema(template_path):
    # This script simulates verification using the project-template.json.
    # In a real environment, it would use zcatalyst_sdk to query the Data Store metadata online.
    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        return False
        
    with open(template_path, 'r') as f:
        template = json.load(f)
        
    tables = template.get("datastore", [])
    if not tables:
        print("No tables found in template.")
        return False
        
    print(f"Verifying {len(tables)} tables offline against IaC template...")
    
    # 1. Verify foreign key data types and parents
    for table in tables:
        for col in table.get("columns", []):
            if col.get("dataType") == "foreign key":
                if not col.get("parentTable"):
                    print(f"Error: Foreign key {col['columnName']} in {table['tableName']} missing parentTable.")
                    return False
                    
    # 2. Check for unique flags on known IDs
    case_master = next((t for t in tables if t["tableName"] == "CaseMaster"), None)
    if case_master:
        crime_no_col = next((c for c in case_master["columns"] if c["columnName"] == "CrimeNo"), None)
        if not crime_no_col or not crime_no_col.get("isUnique"):
            print("Error: CrimeNo is not marked unique in CaseMaster.")
            return False
            
    print("Schema offline verification passed.")
    return True

if __name__ == "__main__":
    # Note: Ensure credentials are NOT hardcoded here. They would be provided via env vars 
    # if making actual SDK calls to zcatalyst_sdk.
    template_file = os.path.join(os.path.dirname(__file__), '..', '..', 'infra', 'catalyst', 'project-template.json')
    verify_schema(template_file)
