import asyncio
from typing import Any

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from src.helpers.webhook_utils import WebhookUtils
from src.interfaces import ISites
from src.log import logg


class BOTScrapy:

    __object_id: str = "bot_scrapy"

    def __init__(self, sites_object: list[ISites]) -> None:
        """"""
        self.__sites = sites_object

    async def run_scrapy(self) -> None:
        """"""
        async with async_playwright() as instance:
            browser: Browser | Any = await instance.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions",
                    "--disable-blink-features=AutomationControlled",
                ],
            )

            context: BrowserContext | Any = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                java_script_enabled=True,
            )
            page: Page | Any = await context.new_page()

            for site_instance in self.__sites:
                """"""
                site: ISites = site_instance(page)
                try:
                    await page.goto(
                        site.url, timeout=120000, wait_until='domcontentloaded'
                    )
                    await asyncio.sleep(4)
                    result: bool = await site.scrapy()
                    if result:
                        await site.save_datas()
                    print({"process": site.object_id, "success": result})
                    logg.info_message(
                        f'("process": {site.object_id},"success": {result})'
                    )
                except Exception as e:
                    logg.error_message(f"Error when scrapping({site.url}) - Error({e})")

            await WebhookUtils.send_data_for_urls()
            await asyncio.sleep(2)
