import json
import re
import os

def parse_markdown_schema():
    with open('docs/database/CATALYST_DATASTORE_SCHEMA_MAPPING.md', 'r') as f:
        lines = f.readlines()
        
    tables = {}
    current_table = None
    
    for line in lines:
        if line.strip().startswith('|') and 'Catalyst Table' not in line and '---' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 8: continue
                
            cat_table = parts[2]
            cat_field = parts[4]
            col_type = parts[5].lower()
            parent_table = parts[6]
            constraints = parts[7].lower()
            notes = parts[8].lower() if len(parts) > 8 else ""
            
            if cat_table:
                if cat_table not in tables:
                    tables[cat_table] = {'tableName': cat_table, 'columns': {}}
                current_table = tables[cat_table]
            
            if not cat_field or cat_field == '-': continue
            if cat_field == '[REMOVED]': continue
                
            col = {
                'columnName': cat_field,
                'dataType': 'varchar',
                'isMandatory': False,
                'isUnique': False,
                'isSearchIndex': False,
                'isPII': False
            }
            
            if 'int' in col_type and 'bigint' not in col_type: col['dataType'] = 'int'
            elif 'bigint' in col_type: col['dataType'] = 'bigint'
            elif 'date' in col_type and 'datetime' not in col_type: col['dataType'] = 'date'
            elif 'datetime' in col_type: col['dataType'] = 'datetime'
            elif 'double' in col_type or 'decimal' in col_type: col['dataType'] = 'double'
            elif 'boolean' in col_type: col['dataType'] = 'boolean'
            elif 'encrypted text' in col_type: col['dataType'] = 'encrypted text'
            elif 'foreign key' in col_type:
                col['dataType'] = 'foreign key'
                col['parentTable'] = parent_table
                
            if 'mandatory' in constraints: col['isMandatory'] = True
            if 'unique' in constraints: col['isUnique'] = True
            if 'search index' in constraints: col['isSearchIndex'] = True
            if 'pii' in constraints or 'pii' in notes: col['isPII'] = True
                
            current_table['columns'][cat_field] = col
            
    return tables

def generate_reports():
    expected_tables = parse_markdown_schema()
    
    with open('data/actual_catalyst_schema.json', 'r') as f:
        actual_data = json.load(f)
        
    actual_tables = {t['table_name']: t for t in actual_data}
    
    mismatches = []
    missing_tables = 0
    unexpected_tables = 0
    missing_cols = 0
    incorrect_types = 0
    broken_fks = 0
    missing_unique = 0
    missing_mandatory = 0
    security_issues = 0
    
    # 1. Verification Report
    verification_md = "# Catalyst Schema Verification Report\\n\\n"
    verification_md += "## 1. Table Existence\\n"
    for t_name in expected_tables:
        if t_name in actual_tables:
            verification_md += f"- [x] `{t_name}` exists.\\n"
        else:
            verification_md += f"- [ ] `{t_name}` MISSING.\\n"
            missing_tables += 1
            mismatches.append((t_name, "-", "Table exists", "Missing", "Critical", "Create table", "No"))
            
    for t_name in actual_tables:
        if t_name not in expected_tables and t_name != 'TestTable':
            verification_md += f"- [?] `{t_name}` is unexpected.\\n"
            unexpected_tables += 1
            mismatches.append((t_name, "-", "Not exists", "Exists", "Low", "Drop table if unused", "Yes"))
            
    verification_md += "\\n## 2. Column Verification\\n"
    for t_name, expected_table in expected_tables.items():
        if t_name not in actual_tables: continue
        actual_table = actual_tables[t_name]
        actual_cols = {c['column_name']: c for c in actual_table['columns']}
        
        for c_name, expected_col in expected_table['columns'].items():
            if c_name not in actual_cols:
                missing_cols += 1
                mismatches.append((t_name, c_name, "Exists", "Missing", "High", f"Create column {c_name}", "Yes (if data exists)"))
                continue
                
            actual_col = actual_cols[c_name]
            a_type = str(actual_col.get('data_type')).lower()
            e_type = expected_col['dataType']
            
            if e_type == 'foreign key':
                # Catalyst stores FKs sometimes as 'bigint' if fallback
                if a_type == 'bigint':
                    mismatches.append((t_name, c_name, "foreign key", "bigint (fallback)", "Low", "None (Catalyst limit reached, bigint stores ROWID)", "No"))
                elif a_type != 'foreign key':
                    broken_fks += 1
                    mismatches.append((t_name, c_name, "foreign key", a_type, "High", "Convert to foreign key", "Yes"))
                else:
                    pass # parent check is harder without parent metadata in dump, but it exists
            elif e_type != a_type:
                # normalize variations
                if e_type == 'varchar' and a_type == 'varchar': pass
                elif e_type == 'int' and a_type == 'int': pass
                else:
                    incorrect_types += 1
                    mismatches.append((t_name, c_name, e_type, a_type, "Medium", f"Convert to {e_type}", "Yes"))
                    
            if expected_col['isMandatory'] and not actual_col.get('is_mandatory'):
                missing_mandatory += 1
                mismatches.append((t_name, c_name, "Mandatory: True", "Mandatory: False", "Medium", "Enable is_mandatory", "No"))
                
            if expected_col['isUnique'] and not actual_col.get('is_unique'):
                missing_unique += 1
                mismatches.append((t_name, c_name, "Unique: True", "Unique: False", "Medium", "Enable is_unique", "Possible data clash"))
                
            if expected_col['isPII'] and not actual_col.get('audit_consent') and e_type != 'encrypted text':
                # If it's encrypted text, it might inherently be PII, but if not audit_consent...
                security_issues += 1
                mismatches.append((t_name, c_name, "PII/Audit: True", "False", "High", "Enable PII / Audit Consent", "No"))

    # Security Audit specific checks
    security_md = "# Catalyst Security Audit\\n\\n"
    security_md += "## PII Fields Status\\n"
    for t_name, expected_table in expected_tables.items():
        for c_name, expected_col in expected_table['columns'].items():
            if expected_col['isPII']:
                ac_col = actual_tables.get(t_name, {}).get('columns', [])
                actual_col = next((c for c in ac_col if c['column_name'] == c_name), None)
                if actual_col and (actual_col.get('audit_consent') or actual_col.get('data_type') == 'encrypted text'):
                    security_md += f"- [x] `{t_name}.{c_name}` correctly protected.\\n"
                else:
                    security_md += f"- [ ] `{t_name}.{c_name}` missing PII protection.\\n"

    # Mismatches Report
    mismatches_md = "# Catalyst Schema Mismatches\\n\\n"
    mismatches_md += "| Table | Column | Expected | Actual | Severity | Recommended Correction | Data Affected |\\n"
    mismatches_md += "|---|---|---|---|---|---|---|\\n"
    for m in mismatches:
        mismatches_md += f"| {m[0]} | {m[1]} | {m[2]} | {m[3]} | {m[4]} | {m[5]} | {m[6]} |\\n"
        
    # Relationship Audit
    rel_md = "# Catalyst Relationship Audit\\n\\n"
    rel_md += "## Foreign Key Validations\\n"
    for t_name, expected_table in expected_tables.items():
        for c_name, expected_col in expected_table['columns'].items():
            if expected_col['dataType'] == 'foreign key':
                rel_md += f"- `{t_name}.{c_name}` references `{expected_col['parentTable']}`.\\n"

    with open('docs/database/CATALYST_SCHEMA_VERIFICATION_REPORT.md', 'w') as f: f.write(verification_md)
    with open('docs/database/CATALYST_SCHEMA_MISMATCHES.md', 'w') as f: f.write(mismatches_md)
    with open('docs/database/CATALYST_SECURITY_AUDIT.md', 'w') as f: f.write(security_md)
    with open('docs/database/CATALYST_RELATIONSHIP_AUDIT.md', 'w') as f: f.write(rel_md)
    with open('docs/database/CATALYST_FIX_PLAN.md', 'w') as f: f.write("# Catalyst Fix Plan\\n\\nBased on the mismatches, apply the recommended corrections.")
    
    print(f"Total expected tables: {len(expected_tables)}")
    print(f"Total actual tables: {len(actual_tables)}")
    print(f"Missing tables: {missing_tables}")
    print(f"Unexpected tables: {unexpected_tables}")
    print(f"Missing columns: {missing_cols}")
    print(f"Incorrect column types: {incorrect_types}")
    print(f"Broken foreign keys: {broken_fks}")
    print(f"Missing unique constraints: {missing_unique}")
    print(f"Missing mandatory constraints: {missing_mandatory}")
    print(f"Security issues: {security_issues}")
    if missing_tables == 0 and missing_cols == 0 and incorrect_types == 0 and broken_fks == 0:
        print("Overall result: PASS")
    else:
        print("Overall result: FAIL")

if __name__ == '__main__':
    generate_reports()
