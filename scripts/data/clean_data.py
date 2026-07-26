import os
import pandas as pd

def normalize_and_clean():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/synthetic'))
    
    print(f"Normalizing and cleaning files in {data_dir}...")
    
    for filename in os.listdir(data_dir):
        if not filename.endswith('.csv'):
            continue
            
        filepath = os.path.join(data_dir, filename)
        df = pd.read_csv(filepath)
        
        # Add synthetic marker if missing
        if 'synthetic' not in df.columns:
            df['synthetic'] = True
            print(f"Added 'synthetic' marker to {filename}")
            
        # Basic cleaning: strip whitespace from object columns
        df_obj = df.select_dtypes(['object'])
        df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
        
        # Save back
        df.to_csv(filepath, index=False)
        print(f"Cleaned {filename}")

if __name__ == "__main__":
    normalize_and_clean()
