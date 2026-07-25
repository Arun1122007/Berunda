import asyncio
import json
import re
from playwright.async_api import async_playwright

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
                col['parentTable'] = parent_table
                col['onDelete'] = 'cascade' if 'cascade' in on_delete else 'restrict'
                
            if 'mandatory' in constraints:
                col['isMandatory'] = True
            if 'unique' in constraints:
                col['isUnique'] = True
                
            current_table['columns'].append(col)
            
    return tables

async def get_page(browser):
    context = browser.contexts[0]
    for p in context.pages:
        if "console.catalyst.zoho.in" in p.url:
            return p
    return None

async def main():
    schema = parse_markdown_schema()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        
        page = await get_page(browser)
        if not page:
            print("Tab not found")
            return
            
        print("Connected to:", page.url)

        setup_js = """async () => {
            window.my_csrf = window.csrfToken || document.cookie.match(new RegExp('(^| )_zcsr_tmp=([^;]+)'))[2];
            window.my_project = window.projectId || "48591000000013025";
            window.my_orgId = "60079736152";
            window.my_baseUrl = `/baas/v1/project/${window.my_project}/table`;
            window.my_headers = {
                'Accept': 'application/vnd.catalyst.v2+json',
                'Content-Type': 'application/json',
                'catalyst-org': window.my_orgId,
                'x-zcsrf-token': `zd_csrparam=${window.my_csrf}`
            };
        }"""
        await page.evaluate(setup_js)

        get_tables_js = """async () => {
            let res = await fetch(window.my_baseUrl, { headers: window.my_headers });
            let tableData = await res.json();
            let tableMap = {}; 
            if(tableData.data) {
                tableData.data.forEach(t => tableMap[t.table_name] = t.table_id);
            }
            return tableMap;
        }"""
        
        tableMap = await page.evaluate(get_tables_js)

        for table in schema:
            tName = table['tableName']
            if tName not in tableMap:
                print(f"Creating table {tName}")
                create_table_js = f"""async () => {{
                    let res = await fetch(window.my_baseUrl, {{
                        method: 'POST',
                        headers: window.my_headers,
                        body: JSON.stringify({{ table_name: '{tName}' }})
                    }});
                    let td = await res.json();
                    return td.data ? td.data.table_id : null;
                }}"""
                new_id = await page.evaluate(create_table_js)
                if new_id:
                    tableMap[tName] = new_id
                else:
                    print(f"Failed to create {tName}")

        for table in schema:
            tName = table['tableName']
            tId = tableMap.get(tName)
            if not tId: continue
            
            get_cols_js = f"""async () => {{
                let res = await fetch(`${{window.my_baseUrl}}/{tId}/column`, {{ headers: window.my_headers }});
                let data = await res.json();
                return data.data ? data.data.map(c => c.column_name) : [];
            }}"""
            existingCols = set(await page.evaluate(get_cols_js))
            
            for col in table.get('columns', []):
                cName = col['columnName']
                if cName in existingCols or cName in ["ROWID", "CREATORID", "CREATEDTIME", "MODIFIEDTIME"]:
                    continue
                
                payload = {
                    "column_name": cName,
                    "data_type": col['dataType'],
                    "is_mandatory": col.get('isMandatory', False),
                    "is_unique": col.get('isUnique', False)
                }
                if col['dataType'] in ['varchar', 'text']:
                    payload['max_length'] = col.get('maxLength', 255)
                
                if col['dataType'] == 'foreign key':
                    parent = col.get('parentTable')
                    if parent in tableMap:
                        payload['parent_table'] = tableMap[parent]
                    del_rule = col.get('onDelete', 'restrict').lower()
                    if del_rule == 'cascade':
                        payload['constraint_type'] = 'ON-DELETE-CASCADE'
                    else:
                        payload['constraint_type'] = 'ON-DELETE-SET-NULL'

                payload_json = json.dumps([payload])
                print(f"Creating column {cName} in {tName}")
                create_col_js = f"""async () => {{
                    let res = await fetch(`${{window.my_baseUrl}}/{tId}/column`, {{
                        method: 'POST',
                        headers: window.my_headers,
                        body: JSON.stringify({payload_json})
                    }});
                    return await res.json();
                }}"""
                try:
                    cres = await page.evaluate(create_col_js)
                    if cres.get('status') != 'success':
                        print(f"Error {cName}:", cres)
                        if col['dataType'] == 'foreign key':
                            print(f"Fallback to bigint for {cName}")
                            payload['data_type'] = 'bigint'
                            if 'parent_table' in payload: del payload['parent_table']
                            if 'constraint_type' in payload: del payload['constraint_type']
                            payload_json_fb = json.dumps([payload])
                            create_col_fb_js = f"""async () => {{
                                let res = await fetch(`${{window.my_baseUrl}}/{tId}/column`, {{
                                    method: 'POST',
                                    headers: window.my_headers,
                                    body: JSON.stringify({payload_json_fb})
                                }});
                                return await res.json();
                            }}"""
                            cres_fb = await page.evaluate(create_col_fb_js)
                            if cres_fb.get('status') != 'success':
                                print(f"Fallback Error {cName}:", cres_fb)
                except Exception as e:
                    print(f"Error on {cName}: {e}")
                    page = await get_page(browser)
                    if page: await page.evaluate(setup_js)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
