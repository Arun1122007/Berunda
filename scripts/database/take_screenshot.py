import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        catalyst_page = None
        for page in context.pages:
            if "console.catalyst.zoho.in" in page.url:
                catalyst_page = page
                break
        
        if not catalyst_page:
            print("Catalyst tab not found")
            return
            
        print(f"Connected to: {catalyst_page.url}")
        
        # Take a screenshot to see what's there
        await catalyst_page.screenshot(path="catalyst_screen.png")
        print("Screenshot saved to catalyst_screen.png")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
