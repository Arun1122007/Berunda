import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scripts.database.catalyst_client import get_tables, get_table_columns

def parse_markdown_schema():
    with open('docs/database/CATALYST_DATASTORE_SCHEMA_MAPPING.md', 'r') as f:
        lines = f.readlines()

    tables = []
    current_table = None

    for line in lines:
        if line.strip().startswith('|') and 'Catalyst Table' not in line and '---' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 8:
                continue

            cat_table = parts[2]
            cat_field = parts[4]
            col_type = parts[5].lower()
            parent_table = parts[6]
            constraints = parts[7].lower()
            on_delete = parts[8].lower()

            if cat_table:
                current_table = {'tableName': cat_table, 'columns': []}
                tables.append(current_table)

            if not cat_field or cat_field == '-':
                continue

            col = {
                'columnName': cat_field,
                'dataType': 'varchar'
            }
            if 'int' in col_type and 'bigint' not in col_type:
                col['dataType'] = 'int'
            elif 'bigint' in col_type:
                col['dataType'] = 'bigint'
            elif 'date' in col_type and 'datetime' not in col_type:
                col['dataType'] = 'date'
            elif 'datetime' in col_type:
                col['dataType'] = 'datetime'
            elif 'double' in col_type or 'decimal' in col_type:
                col['dataType'] = 'double'
            elif 'boolean' in col_type:
                col['dataType'] = 'boolean'
            elif 'encrypted text' in col_type:
                col['dataType'] = 'encrypted text'
            elif 'foreign key' in col_type:
                col['dataType'] = 'foreign key'

            current_table['columns'].append(col)

    return tables

def main():
    print("--- SCHEMA DIFF VALIDATION ---")
    expected_tables = parse_markdown_schema()
    
    # Fetch remote
    try:
        remote_data = get_tables()
        remote_tables = remote_data.get('data', [])
    except Exception as e:
        print(f"Failed to fetch remote tables: {e}")
        return

    remote_map = {t['table_name']: t['table_id'] for t in remote_tables}

    missing_tables = []
    mismatch_columns = []

    for exp_table in expected_tables:
        tName = exp_table['tableName']
        if tName not in remote_map:
            missing_tables.append(tName)
            continue
        
        # Check columns
        tId = remote_map[tName]
        details = get_table_columns(tId)
        remote_cols = details.get('data', [])
        remote_col_map = {c['column_name']: c['data_type'] for c in remote_cols}
        
        for exp_col in exp_table['columns']:
            cName = exp_col['columnName']
            if cName not in remote_col_map:
                mismatch_columns.append(f"[{tName}] Missing column: {cName}")
            else:
                rType = remote_col_map[cName]
                eType = exp_col['dataType']
                if rType != eType and not (eType == 'foreign key' and rType == 'bigint'):
                     mismatch_columns.append(f"[{tName}] Type mismatch for {cName}: Expected {eType}, Found {rType}")

    print(f"\nMissing Tables: {len(missing_tables)}")
    for mt in missing_tables:
        print(f" - {mt}")

    print(f"\nColumn Issues: {len(mismatch_columns)}")
    for mc in mismatch_columns:
        print(f" - {mc}")

    if not missing_tables and not mismatch_columns:
        print("\nSUCCESS: Remote schema matches expected manifest.")

if __name__ == "__main__":
    main()
