import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        catalyst_page = None
        for page in context.pages:
            if "console.catalyst" in page.url:
                catalyst_page = page
                break
        
        if not catalyst_page:
            print("Catalyst tab not found")
            return
            
        print(f"Connected to: {catalyst_page.url}")
        
        # Wait for the Data Store page to fully load
        await catalyst_page.wait_for_timeout(2000)
        
        # Get the page content
        content = await catalyst_page.content()
        with open("catalyst_dom.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("DOM saved to catalyst_dom.html")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
