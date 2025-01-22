from typing import Optional

from playwright.async_api import ElementHandle, Page

from src.api.controllers import ExchangesController
from src.api.entities import ExchangeBase
from src.interfaces import ISites
from src.log import logg


class BCI(ISites):
    """"""

    __object_id: str = "Scrapper_BancoBCI"
    __url: str = "https://www.bci.ao/particular/conversor-de-moeda"
    __exchange_table_class_name: str = ".table"
    __button_change_to_note_id_name: str = "#simple-tab-1"

    __datas_json: list[dict] = []
    __exchanges_controller = ExchangesController

    def __init__(self, page: Page):
        """"""
        self.__page: Optional[Page] = page if isinstance(page, Page) else None

    async def scrapy(self) -> bool:
        """"""
        if self.__page:
            await self.__change_to_notes__()
            exchange_table_element: ElementHandle = (
                await self.__page.query_selector(
                    self.__exchange_table_class_name
                )
            )
            if exchange_table_element:
                table_striped_body: ElementHandle = (
                    await exchange_table_element.query_selector("tbody")
                )
                all_tr: ElementHandle = (
                    await table_striped_body.query_selector_all("tr")
                )
                if all_tr and isinstance(all_tr, list):
                    for tr in all_tr:
                        coins: ElementHandle = await tr.query_selector(
                            "td:nth-of-type(1)"
                        )
                        sale: ElementHandle = await tr.query_selector(
                            "td:nth-of-type(2)"
                        )
                        buy: ElementHandle = await tr.query_selector(
                            "td:nth-of-type(3)"
                        )
                        if coins and sale and buy:
                            self.__datas_json.append(
                                {
                                    "coins": await coins.inner_text(),
                                    "sell": await sale.inner_text(),
                                    "buy": await buy.inner_text(),
                                }
                            )
                        else:
                            logg.error_message(
                                f"[{self.__object_id}]: error when getting the values ​​of (coin, sell and buy)"
                            )
                            return False
                else:
                    logg.error_message(
                        f"[{self.__object_id}]: error when getting tr tags"
                    )
                    return False
                return True
            logg.error_message(
                f"[{self.__object_id}]: error when getting the exchange table"
            )
            return False

    async def __change_to_notes__(self) -> None:
        """"""
        button_change_to_note: ElementHandle = await self.__page.query_selector(
            self.__button_change_to_note_id_name
        )
        if button_change_to_note:
            await button_change_to_note.click()

    async def save_datas(self) -> None:
        """"""
        try:
            exchange = (
                await self.__exchanges_controller.find_exchanges_for_bank_name(
                    bank_name="BCI", verify_only=True
                )
            )
            if not exchange:
                exchange_entitie = ExchangeBase(
                    bank_name="BCI", exchanges_values=self.__datas_json
                )
                result: bool = await self.__exchanges_controller.create(
                    exchange_entitie
                )
                return result
            else:
                result: bool = await self.__exchanges_controller.update(
                    bank_name="BCI", exchanges_values=self.__datas_json
                )
                return result
        except:
            return False

    @property
    def url(self) -> str:
        """"""
        return self.__url

    @property
    def object_id(self) -> str:
        """"""
        return self.__object_id
