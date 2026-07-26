import argparse
import csv
from pathlib import Path
from typing import Any

import zcatalyst_sdk
from dotenv import load_dotenv

load_dotenv()

def init_catalyst():
    """Initializes the Catalyst SDK using local credentials."""
    # During local script execution outside an AppSail container, we need to mock the req
    # or ensure we have proper environment variables configured for CLI.
    # Catalyst usually requires init via catalyst serve or deployed container.
    return zcatalyst_sdk.initialize()

def get_row_data(row: dict[str, str]) -> dict[str, Any]:
    """Cleans empty strings from CSV and casts integers."""
    clean = {}
    for k, v in row.items():
        if v == "":
            continue
        if v.isdigit():
            clean[k] = int(v)
        elif v.replace(".", "", 1).isdigit() and v.count(".") == 1:
            clean[k] = float(v)
        else:
            clean[k] = v
    return clean

def import_table(datastore, table_name: str, csv_path: Path) -> None:
    print(f"Importing {table_name} from {csv_path}...")
    table = datastore.table(table_name)

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            batch.append(get_row_data(row))
            if len(batch) >= 50:
                print(f"Inserting batch of 50 into {table_name}...")
                table.insert_rows(batch)
                batch = []
        if batch:
            print(f"Inserting final batch of {len(batch)} into {table_name}...")
            table.insert_rows(batch)

def main():
    parser = argparse.ArgumentParser(description="Import synthetic data to Catalyst Data Store")
    parser.add_argument("--tier", type=str, default="smoke", choices=["smoke", "demo"], help="Data tier to import")
    parser.add_argument("--seed", type=str, default="42", help="Seed used for the generation")
    args = parser.parse_args()

    app = init_catalyst()
    datastore = app.datastore()

    data_dir = Path("data/synthetic")

    # Tables must be imported in correct parent-child order to satisfy foreign keys
    # But since Catalyst ROWIDs are generated on the server, our synthetic data currently
    # might have its own generated IDs or references. If they refer to Catalyst ROWIDs,
    # we would have a mismatch.
    # For now, we import them sequentially as a best effort. A full production import
    # script requires a mapping cache (Original ID -> Catalyst ROWID).

    tables_order = [
        "CaseMaster",
        "Inv_OccuranceTime",
        "ComplainantDetails",
        "VictimDetails",
        "AccusedDetails",
        "ChargesheetDetails",
        "EvidenceMaster"
    ]

    for table in tables_order:
        csv_file = data_dir / f"SYNTHETIC_{table}_{args.tier}_{args.seed}.csv"
        if csv_file.exists():
            import_table(datastore, table, csv_file)
        else:
            print(f"Warning: {csv_file} not found. Skipping {table}.")

if __name__ == "__main__":
    main()
