import csv
import json
import os


def generate_csvs():
    input_file = "synthetic_seed_data.json"
    output_dir = os.path.join("data", "seed")

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file) as f:
        data = json.load(f)

    for table_name, records in data.items():
        if not records:
            continue

        csv_file = os.path.join(output_dir, f"{table_name}.csv")
        fieldnames = list(records[0].keys())

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        print(f"Created {csv_file} with {len(records)} records.")

if __name__ == "__main__":
    generate_csvs()
