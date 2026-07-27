import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import requests
from scripts.database.catalyst_client import BASE_URL, PROJECT_ID, HEADERS

def insert(table_name, table_id, rows):
    url = f"{BASE_URL}/baas/v1/project/{PROJECT_ID}/table/{table_id}/row"
    resp = requests.post(url, headers=HEADERS, json=rows)
    try:
        data = resp.json()
        print(f"Table {table_name} ({table_id}): inserted {len(rows)} rows — Response: {data.get('status')}")
        if data.get('status') != 'success':
            print("  Details:", data)
        return data
    except Exception as e:
        print(f"Table {table_name} Error:", resp.text)
        return None

def main():
    print("Seeding Catalyst Data Store Master & Lookup Tables...\n")

    # 1. State (ID: 48591000000023001)
    state_rows = [
        {"StateID": 1, "StateName": "Karnataka"},
        {"StateID": 2, "StateName": "Maharashtra"},
        {"StateID": 3, "StateName": "Tamil Nadu"}
    ]
    insert("State", "48591000000023001", state_rows)

    # 2. CaseCategory (ID: 48591000000024084)
    cat_rows = [
        {"CaseCategoryID": 1, "CategoryName": "Property Offence"},
        {"CaseCategoryID": 2, "CategoryName": "Violent Crime"},
        {"CaseCategoryID": 3, "CategoryName": "Cybercrime"},
        {"CaseCategoryID": 4, "CategoryName": "Financial Fraud"},
        {"CaseCategoryID": 5, "CategoryName": "Narcotics"}
    ]
    insert("CaseCategory", "48591000000024084", cat_rows)

    # 3. GravityOffence (ID: 48591000000024443)
    gravity_rows = [
        {"GravityOffenceID": 1, "GravityName": "Heinous"},
        {"GravityOffenceID": 2, "GravityName": "Non-Heinous"},
        {"GravityOffenceID": 3, "GravityName": "Minor Offence"}
    ]
    insert("GravityOffence", "48591000000024443", gravity_rows)

    # 4. CaseStatusMaster (ID: 48591000000024802)
    status_rows = [
        {"CaseStatusID": 1, "StatusName": "Under Investigation"},
        {"CaseStatusID": 2, "StatusName": "Chargesheeted"},
        {"CaseStatusID": 3, "StatusName": "Pending Trial"},
        {"CaseStatusID": 4, "StatusName": "Closed"},
        {"CaseStatusID": 5, "StatusName": "Convicted"}
    ]
    insert("CaseStatusMaster", "48591000000024802", status_rows)

    # 5. CrimeHead (ID: 48591000000025161)
    head_rows = [
        {"CrimeHeadID": 1, "HeadName": "Robbery & Dacoity"},
        {"CrimeHeadID": 2, "HeadName": "Cyber Theft"},
        {"CrimeHeadID": 3, "HeadName": "Aggravated Assault"},
        {"CrimeHeadID": 4, "HeadName": "Vehicle Theft"},
        {"CrimeHeadID": 5, "HeadName": "Commercial Fraud"}
    ]
    insert("CrimeHead", "48591000000025161", head_rows)

    print("\nMaster tables seeding complete!")

if __name__ == "__main__":
    main()
