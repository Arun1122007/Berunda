import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        catalyst_page = None
        for page in context.pages:
            if "console.catalyst.zoho" in page.url:
                catalyst_page = page
                break
        
        if not catalyst_page:
            print("Catalyst tab not found")
            return
            
        print(f"Connected to: {catalyst_page.url}")
        
        res = await catalyst_page.evaluate("""() => {
            let orgId = location.pathname.split('/')[2];
            let csrf = window.csrfToken || "";
            // check document cookie for zcsr_tmp if window.csrfToken doesn't work
            let match = document.cookie.match(new RegExp('(^| )_zcsr_tmp=([^;]+)'));
            if (match) csrf = match[2];
            
            return {
                csrf: csrf,
                project: window.projectId,
                orgId: orgId
            }
        }""")
        print("Page Info:", res)
        
        tables_res = await catalyst_page.evaluate(f"""async () => {{
            const csrfParam = window.csrfParamName || 'zd_csrparam';
            const url = `/baas/{res['orgId']}/project/{res['project']}/Development/cloudscale/datastore/tables`;
            const response = await fetch(url, {{
                method: 'GET',
                headers: {{
                    'X-ZCSRF-TOKEN': '{res['csrf']}',
                    [csrfParam]: '{res['csrf']}',
                    'Accept': 'application/json'
                }}
            }});
            return await response.text();
        }}""")
        print("Tables API response:", tables_res[:500])
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
