import argparse
import csv
import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import requests
from scripts.database.catalyst_client import BASE_URL, HEADERS, PROJECT_ID, get_tables


def insert_rows(table_id, rows):
    url = f"{BASE_URL}/baas/v1/project/{PROJECT_ID}/table/{table_id}/row"
    response = requests.post(url, headers=HEADERS, json=rows)
    try:
        response.raise_for_status()
        res_json = response.json()
        print(f"Successfully inserted {len(rows)} rows into table ID {table_id}")
        return res_json
    except Exception as e:
        print(f"Error inserting into {table_id}: {e}")
        if response.text:
            print("Response:", response.text[:500])
        return None

def import_table(table_id, table_name, csv_path):
    print(f"\n--- Importing {table_name} from {csv_path} ---")
    if not csv_path.exists():
        print(f"File {csv_path} does not exist. Skipping.")
        return

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        count = 0
        for row in reader:
            clean_row = {}
            for k, v in row.items():
                if v is not None and v != "":
                    if isinstance(v, str) and v.isdigit():
                        clean_row[k] = int(v)
                    else:
                        clean_row[k] = str(v)
            if clean_row:
                batch.append(clean_row)
                count += 1
            if len(batch) >= 20:
                insert_rows(table_id, batch)
                batch = []
        if batch:
            insert_rows(table_id, batch)
        print(f"Finished {table_name}: Total {count} rows processed.")

def main():
    parser = argparse.ArgumentParser(description="Import synthetic data to Catalyst Data Store")
    parser.add_argument("--tier", type=str, default="smoke", choices=["smoke", "demo"])
    parser.add_argument("--seed", type=str, default="42")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")
    args = parser.parse_args()

    # Fetch table IDs from Catalyst API
    remote_data = get_tables()
    remote_map = {t['table_name']: t['table_id'] for t in remote_data.get('data', [])}
    print(f"Connected to Catalyst API. Found {len(remote_map)} tables.")

    if args.dry_run:
        print("--- DRY RUN: No data will be inserted ---")
        return

    data_dir = Path("data/synthetic")
    table_mappings = [
        ("CaseMaster", f"SYNTHETIC_CaseMaster_{args.tier}_{args.seed}.csv"),
        ("Inv_OccurrenceTime", f"SYNTHETIC_Inv_OccuranceTime_{args.tier}_{args.seed}.csv"),
        ("ComplainantDetails", f"SYNTHETIC_ComplainantDetails_{args.tier}_{args.seed}.csv"),
        ("Victim", f"SYNTHETIC_VictimDetails_{args.tier}_{args.seed}.csv"),
        ("Accused", f"SYNTHETIC_AccusedDetails_{args.tier}_{args.seed}.csv"),
        ("ChargesheetDetails", f"SYNTHETIC_ChargesheetDetails_{args.tier}_{args.seed}.csv"),
        ("EvidenceMaster", f"SYNTHETIC_EvidenceMaster_{args.tier}_{args.seed}.csv"),
    ]

    for table_name, filename in table_mappings:
        csv_file = data_dir / filename
        t_id = remote_map.get(table_name)
        if t_id:
            import_table(t_id, table_name, csv_file)
        else:
            print(f"Warning: Table {table_name} not found in Catalyst Data Store. Skipping.")

if __name__ == "__main__":
    main()
