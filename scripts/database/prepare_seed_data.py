import json
import random
from datetime import datetime, timedelta

def generate_seed_data():
    random.seed(42)  # Deterministic random seed
    
    # Phase A
    states = [{"StateID": i+1, "StateName": f"State_{i+1}"} for i in range(2)]
    acts = [{"ActCode": f"ACT-{i+1}", "ActName": f"Act Name {i+1}"} for i in range(3)]
    
    # Phase B
    districts = []
    for i, state in enumerate(states):
        districts.append({"DistrictID": i+1, "DistrictName": f"District_{i+1}", "StateRef": state["StateID"]})
        
    sections = []
    for i, act in enumerate(acts):
        for j in range(2):
            sections.append({
                "SectionCode": f"SEC-{i+1}-{j+1}", 
                "SectionName": f"Section {j+1}",
                "ActRef": act["ActCode"],
                "SectionKey": f"{act['ActCode']}:SEC-{i+1}-{j+1}"
            })
            
    # Core Cases
    cases = []
    for i in range(5):
        cases.append({
            "CaseMasterID": i+1,
            "CrimeNo": f"CR-{2026}-{i+1}",
            "CaseNo": f"C{i+1}",
            "CrimeRegisteredDate": (datetime(2026, 1, 1) + timedelta(days=i)).strftime("%Y-%m-%d"),
            "BriefFacts": "Synthetic case generated for testing."
        })
        
    accused_list = []
    for i, case in enumerate(cases):
        accused_list.append({
            "AccusedID": i+1,
            "CaseMasterRef": case["CaseMasterID"],
            "Name": f"Synthetic Accused {i+1}",
            "Age": random.randint(18, 60)
        })

    seed_data = {
        "State": states,
        "Act": acts,
        "District": districts,
        "Section": sections,
        "CaseMaster": cases,
        "Accused": accused_list
    }
    
    with open("synthetic_seed_data.json", "w") as f:
        json.dump(seed_data, f, indent=4)
        
    print("Synthetic seed data generated successfully.")

if __name__ == "__main__":
    generate_seed_data()
