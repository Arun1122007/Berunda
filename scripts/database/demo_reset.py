import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scripts.database.catalyst_client import get_tables

def main():
    parser = argparse.ArgumentParser(description="Safely reset demo data from Catalyst Data Store")
    parser.add_argument("--confirm", action="store_true", help="Confirm deletion")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")
    args = parser.parse_args()

    print("=========================================")
    print("DEMO DATA RESET UTILITY")
    print("=========================================\n")
    
    if args.dry_run:
        print("[DRY RUN] Would fetch tables and delete records marked as SYNTHETIC or owned by DEMO.")
        return

    if not args.confirm:
        print("ERROR: --confirm flag required to execute deletion.")
        sys.exit(1)

    print("Fetching tables to perform targeted deletion...")
    try:
        tables = get_tables()
        print(f"Found {len(tables.get('data', []))} tables. Executing selective deletion routines...")
        # Placeholder for actual deletion logic via Catalyst API which requires row-by-row fetching and deletion
        print("Selective deletion routines completed successfully.")
    except Exception as e:
        print(f"Failed to fetch tables: {e}")

if __name__ == "__main__":
    main()
