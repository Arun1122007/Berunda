import os
import pandas as pd
import uuid

def generate_missing_entities():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/synthetic'))
    
    # 1. Police Stations
    stations = [
        {"station_id": str(uuid.uuid4()), "station_name": "Koramangala PS", "district": "Bengaluru", "active": True, "synthetic": True},
        {"station_id": str(uuid.uuid4()), "station_name": "Indiranagar PS", "district": "Bengaluru", "active": True, "synthetic": True},
        {"station_id": str(uuid.uuid4()), "station_name": "Ulsoor PS", "district": "Bengaluru", "active": True, "synthetic": True},
        {"station_id": str(uuid.uuid4()), "station_name": "JP Nagar PS", "district": "Bengaluru", "active": True, "synthetic": True},
    ]
    pd.DataFrame(stations).to_csv(os.path.join(data_dir, "SYNTHETIC_PoliceStations_demo_42.csv"), index=False)
    
    # 2. Users
    users = [
        {"user_id": str(uuid.uuid4()), "name": "Demo_Officer_1", "role": "Investigating Officer", "station_id": stations[0]["station_id"], "synthetic": True},
        {"user_id": str(uuid.uuid4()), "name": "Demo_Supervisor_1", "role": "Supervisor", "station_id": stations[0]["station_id"], "synthetic": True},
        {"user_id": str(uuid.uuid4()), "name": "Demo_Analyst_1", "role": "Analyst", "station_id": "HQ", "synthetic": True},
    ]
    pd.DataFrame(users).to_csv(os.path.join(data_dir, "SYNTHETIC_Users_demo_42.csv"), index=False)
    
    # 3. Crime Categories
    categories = [
        {"category_id": "CAT-001", "name": "vehicle_theft", "description": "Theft of motor vehicles", "synthetic": True},
        {"category_id": "CAT-002", "name": "burglary", "description": "Breaking and entering", "synthetic": True},
        {"category_id": "CAT-003", "name": "assault", "description": "Physical altercation", "synthetic": True},
        {"category_id": "CAT-004", "name": "fraud", "description": "Financial deception", "synthetic": True},
    ]
    pd.DataFrame(categories).to_csv(os.path.join(data_dir, "SYNTHETIC_CrimeCategories_demo_42.csv"), index=False)
    
    # 4. Audit Events
    audit = [
        {"event_id": str(uuid.uuid4()), "user_id": users[0]["user_id"], "action": "FIR_CREATED", "target_id": "FIR-001", "synthetic": True},
        {"event_id": str(uuid.uuid4()), "user_id": users[0]["user_id"], "action": "AI_EXTRACTION_PERFORMED", "target_id": "FIR-001", "synthetic": True},
        {"event_id": str(uuid.uuid4()), "user_id": users[0]["user_id"], "action": "HUMAN_REVIEW_ACCEPTED", "target_id": "FIR-001", "synthetic": True},
        {"event_id": str(uuid.uuid4()), "user_id": users[2]["user_id"], "action": "SEARCH_QUERY_BLOCKED", "target_id": "N/A", "synthetic": True},
    ]
    pd.DataFrame(audit).to_csv(os.path.join(data_dir, "SYNTHETIC_AuditEvents_demo_42.csv"), index=False)
    
    print("Generated missing synthetic entities.")

if __name__ == "__main__":
    generate_missing_entities()
