import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = None
        for p in context.pages:
            if "console.catalyst.zoho.in" in p.url:
                page = p
                break
        
        if not page:
            print("Tab not found")
            return
            
        print("Connected to:", page.url)

        js_code = """async () => {
            let csrf = window.csrfToken || document.cookie.match(new RegExp('(^| )_zcsr_tmp=([^;]+)'))[2];
            let project = window.projectId || "48591000000013025";
            let orgId = "60079736152"; // from cURL
            
            let url = `/baas/v1/project/${project}/table`;
            let res = await fetch(url, {
                headers: {
                    'Accept': 'application/vnd.catalyst.v2+json',
                    'catalyst-org': orgId,
                    'x-zcsrf-token': `zd_csrparam=${csrf}`
                }
            });
            
            if (!res.ok) {
                return {error: res.status, text: await res.text()};
            }
            return await res.json();
        }"""
        
        result = await page.evaluate(js_code)
        print("Tables Data:", json.dumps(result, indent=2))
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
