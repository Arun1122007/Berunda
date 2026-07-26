import argparse
import csv
import json
import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import requests
from scripts.database.catalyst_client import BASE_URL, PROJECT_ID, HEADERS, get_tables

def insert_rows(table_id, rows):
    url = f"{BASE_URL}/baas/v1/project/{PROJECT_ID}/table/{table_id}/row"
    response = requests.post(url, headers=HEADERS, json=rows)
    try:
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error inserting into {table_id}: {e}")
        if response.text:
            print("Response:", response.text)
        return None

def import_table(table_id, table_name, csv_path):
    print(f"Importing {table_name} from {csv_path}...")
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            clean_row = {k: (int(v) if v.isdigit() else v) for k, v in row.items() if v != ""}
            batch.append(clean_row)
            if len(batch) >= 50:
                print(f"Inserting batch of 50 into {table_name}...")
                insert_rows(table_id, batch)
                batch = []
        if batch:
            print(f"Inserting final batch of {len(batch)} into {table_name}...")
            insert_rows(table_id, batch)

def main():
    parser = argparse.ArgumentParser(description="Import synthetic data to Catalyst Data Store")
    parser.add_argument("--tier", type=str, default="smoke", choices=["smoke", "demo"])
    parser.add_argument("--seed", type=str, default="42")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")
    args = parser.parse_args()

    if args.dry_run:
        print("--- DRY RUN: No data will be inserted ---")
        return

    # Fetch table IDs
    remote_data = get_tables()
    remote_map = {t['table_name']: t['table_id'] for t in remote_data.get('data', [])}

    data_dir = Path("data/synthetic")
    tables_order = ["CaseMaster", "Inv_OccuranceTime", "ComplainantDetails", "VictimDetails", "AccusedDetails", "ChargesheetDetails", "EvidenceMaster"]

    for table in tables_order:
        csv_file = data_dir / f"SYNTHETIC_{table}_{args.tier}_{args.seed}.csv"
        t_id = remote_map.get(table)
        if csv_file.exists() and t_id:
            import_table(t_id, table, csv_file)
        else:
            print(f"Warning: {csv_file} or table {table} not found. Skipping.")

if __name__ == "__main__":
    main()
