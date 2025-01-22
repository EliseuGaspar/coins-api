import requests
import asyncio

from src.api.controllers import ExchangesController, WebhookController
from src.log import logg
from src.storage.models import Exchanges, Webhook

from .convertor import Convertor


class WebhookUtils:

    __webhook_controller = WebhookController

    @classmethod
    def run_tests(cls) -> None:
        """"""
        asyncio.run(cls.check_urls_state())

    @classmethod
    async def check_urls_state(cls) -> None:
        """"""
        urls: list[Webhook] = await cls.__webhook_controller.find_all_webhook()
        if len(urls) > 0:
            for url in urls:
                test = await cls.test_url(url.url)
                if test:
                    continue
                await cls.__webhook_controller.delete_url(url)

    @classmethod
    async def test_url(cls, url: str) -> bool:
        """"""
        try:
            response = requests.post(url=url, json={"Test": True}, timeout=5, headers={
                "Content-Type": "application/json"
            })
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.ConnectionError:
            return False
        except Exception as e:
            logg.info_message(f"Error testing url({url}) - Error: {e}")
            return False

    @classmethod
    async def send_data_for_urls(cls) -> None:
        """"""
        exchanges: list[Exchanges] | list = (
            await ExchangesController.find_all_exchanges()
        )
        exchanges_formated: list[dict] = Convertor.exchange_to_dict(
            exchange=exchanges, many=True
        )

        urls: list[Webhook] = await cls.__webhook_controller.find_all_webhook()

        if len(urls) > 0:
            for url in urls:
                try:
                    response = requests.post(url=url.url, json=exchanges_formated, timeout=5, headers={
                        "Content-Type": "application/json"
                    })
                    if response.status_code == 200:
                        logg.info_message(
                            f"dados enviado com sucesso para({url.url})"
                        )
                        continue
                    else:
                        logg.error_message(
                            f"falha ao emviar os dados para({url.url})"
                        )
                        # response.raise_for_status
                except Exception as e:
                    logg.error_message(f"Error sending data to({url.url}) - Error({e})")
        pass
