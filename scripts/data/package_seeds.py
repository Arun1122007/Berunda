import os
import pandas as pd
import json

def package_seeds():
    input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/synthetic'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/seeds'))
    
    print(f"Packaging seeds from {input_dir} to {output_dir}")
    
    for filename in os.listdir(input_dir):
        if not filename.endswith('.csv'):
            continue
            
        filepath = os.path.join(input_dir, filename)
        df = pd.read_csv(filepath)
        
        # Convert to list of dicts
        records = df.to_dict(orient='records')
        
        # Determine output filename
        out_name = filename.replace('.csv', '.json')
        out_path = os.path.join(output_dir, out_name)
        
        with open(out_path, 'w') as f:
            json.dump(records, f, indent=2)
            
        print(f"Packaged {len(records)} records to {out_name}")

if __name__ == "__main__":
    package_seeds()
