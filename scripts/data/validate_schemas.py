import os
import json
import pandas as pd

def validate_schemas():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/synthetic'))
    
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} not found.")
        return False
        
    print(f"Validating synthetic files in {data_dir}...")
    errors = 0
    total_records = 0
    
    for filename in os.listdir(data_dir):
        if not filename.endswith('.csv'):
            continue
            
        filepath = os.path.join(data_dir, filename)
        df = pd.read_csv(filepath)
        total_records += len(df)
        
        # Rule 1: Must contain synthetic flag
        if 'synthetic' not in df.columns:
            print(f"[ERROR] {filename} is missing 'synthetic' column!")
            errors += 1
        else:
            if not df['synthetic'].all():
                print(f"[ERROR] {filename} contains records where synthetic != true!")
                errors += 1
                
        # Rule 2: No obvious real PII fields
        prohibited = ['real_name', 'ssn', 'aadhar', 'real_phone']
        for p in prohibited:
            if p in df.columns:
                print(f"[ERROR] {filename} contains prohibited field: {p}")
                errors += 1

        print(f"[OK] {filename} - {len(df)} records validated.")

    print(f"\n--- VALIDATION SUMMARY ---")
    print(f"Total Records Validated: {total_records}")
    print(f"Total Errors: {errors}")
    
    if errors == 0:
        print("Verdict: PASS")
        return True
    else:
        print("Verdict: FAIL")
        return False

if __name__ == "__main__":
    validate_schemas()
