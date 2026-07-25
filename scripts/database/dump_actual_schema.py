import asyncio
import json
from playwright.async_api import async_playwright

async def get_page(browser):
    context = browser.contexts[0]
    for p in context.pages:
        if "console.catalyst.zoho.in" in p.url:
            return p
    return None

async def main():
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

        get_schema_js = """async () => {
            let res = await fetch(window.my_baseUrl, { headers: window.my_headers });
            let tableData = await res.json();
            
            let schema = [];
            
            if (tableData.data) {
                for (let table of tableData.data) {
                    let tableInfo = {
                        table_name: table.table_name,
                        table_id: table.table_id,
                        columns: []
                    };
                    
                    let colRes = await fetch(`${window.my_baseUrl}/${table.table_id}/column`, { headers: window.my_headers });
                    let colData = await colRes.json();
                    
                    if (colData.data) {
                        for (let col of colData.data) {
                            tableInfo.columns.push(col);
                        }
                    }
                    schema.push(tableInfo);
                }
            }
            return schema;
        }"""
        
        print("Fetching full schema from Catalyst... this might take a minute.")
        actual_schema = await page.evaluate(get_schema_js)
        
        with open('data/actual_catalyst_schema.json', 'w') as f:
            json.dump(actual_schema, f, indent=2)
            
        print(f"Dumped schema to data/actual_catalyst_schema.json with {len(actual_schema)} tables.")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
