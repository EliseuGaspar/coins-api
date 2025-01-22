import requests
import asyncio

from src.api.controllers import ExchangesController, WebhookController
from src.log import logg
from src.storage.models import Exchanges, Webhook
from .convertor import Convertor


class WebhookUtils:
    """
    Utility class for managing and testing webhooks, as well as sending data to registered URLs.
    """

    __webhook_controller = WebhookController

    @classmethod
    def run_tests(cls) -> None:
        """
        Executes the asynchronous method to verify the state of all registered webhooks.
        """
        asyncio.run(cls.check_urls_state())

    @classmethod
    async def check_urls_state(cls) -> None:
        """
        Validates the status of all registered webhook URLs.
        Removes any URLs that fail the connection test.
        """
        urls: list[Webhook] = await cls.__webhook_controller.find_all_webhook()
        if urls:
            for url in urls:
                test = await cls.test_url(url.url)
                if not test:
                    await cls.__webhook_controller.delete_url(url)

    @classmethod
    async def test_url(cls, url: str) -> bool:
        """
        Tests if a given URL is reachable and responds with a status code of 200.

        Args:
            url (str): The webhook URL to be tested.

        Returns:
            bool: True if the URL responds successfully, otherwise False.
        """
        try:
            response = requests.post(
                url=url,
                json={"Test": True},
                timeout=5,
                headers={"Content-Type": "application/json"},
            )
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
        except Exception as e:
            logg.info_message(f"Error testing URL({url}) - Error: {e}")
            return False

    @classmethod
    async def send_data_for_urls(cls) -> None:
        """
        Sends formatted exchange rate data to all active webhook URLs.
        Logs the success or failure of each attempt.
        """
        exchanges: list[Exchanges] | list = await ExchangesController.find_all_exchanges()
        exchanges_formatted: list[dict] = Convertor.exchange_to_dict(exchange=exchanges, many=True)

        urls: list[Webhook] = await cls.__webhook_controller.find_all_webhook()

        if urls:
            for url in urls:
                try:
                    response = requests.post(
                        url=url.url,
                        json=exchanges_formatted,
                        timeout=5,
                        headers={"Content-Type": "application/json"},
                    )
                    if response.status_code == 200:
                        logg.info_message(f"Data successfully sent to({url.url})")
                    else:
                        logg.error_message(f"Failed to send data to({url.url}) - Status code: {response.status_code}")
                except Exception as e:
                    logg.error_message(f"Error sending data to({url.url}) - Error: {e}")
