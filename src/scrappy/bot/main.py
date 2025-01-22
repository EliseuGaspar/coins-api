import asyncio
from typing import Any
from playwright.async_api import Browser, BrowserContext, Page, async_playwright
from src.helpers.webhook_utils import WebhookUtils
from src.interfaces import ISites
from src.log import logg


class BOTScrapy:
    __object_id: str = "bot_scrapy"

    def __init__(self, sites_object: list[ISites]) -> None:
        """Initialize the BOTScrapy with a list of site objects."""
        self.__sites = sites_object

    async def run_scrapy(self) -> None:
        """Run the scraping process for the given sites."""
        async with async_playwright() as instance:
            browser: Browser = await instance.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions",
                    "--disable-blink-features=AutomationControlled",
                ],
            )

            for site_instance in self.__sites:
                context: BrowserContext = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/91.0.4472.124 Safari/537.36"
                    ),
                    java_script_enabled=True,
                )
                page: Page = await context.new_page()

                site: ISites = site_instance(page)
                try:
                    logg.info_message(f"Starting scraping for {site.object_id}")
                    await page.goto(
                        site.url, timeout=60000, wait_until="domcontentloaded"
                    )

                    await page.wait_for_load_state("networkidle")
                    result: bool = await site.scrapy()

                    if result:
                        await site.save_datas()
                        logg.info_message(
                            f"Scraping succeeded for {site.object_id}"
                        )
                    else:
                        logg.warning_message(
                            f"Scraping returned false for {site.object_id}"
                        )
                except Exception as e:
                    logg.error_message(
                        f"Error when scraping {site.url} - Error: {e}"
                    )
                finally:
                    await context.close()

            # Notify webhooks after processing all sites
            await WebhookUtils.send_data_for_urls()
            logg.info_message("Finished scraping for all sites.")
