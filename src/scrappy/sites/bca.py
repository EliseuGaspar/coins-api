from typing import Optional

from playwright.async_api import ElementHandle, Page

from src.api.controllers import ExchangesController
from src.api.entities import ExchangeBase
from src.interfaces import ISites
from src.log import logg


class BCA(ISites):
    """"""

    __object_id: str = "Scrapper_BancoBCA"
    __url: str = "https://www.bca.co.ao/inicio/servicos/cambios-moedas/"
    __exchange_table_class_name: str = ".w-100"

    __datas_json: list[dict] = []
    __exchanges_controller = ExchangesController

    def __init__(self, page: Page):
        """"""
        self.__page: Optional[Page] = page if isinstance(page, Page) else None

    async def scrapy(self) -> bool:
        """"""
        if self.__page:
            exchange_table_element: ElementHandle = (
                await self.__page.query_selector_all(
                    self.__exchange_table_class_name
                )
            )
            if exchange_table_element[1]:
                table_striped_body: ElementHandle = (
                    await exchange_table_element[1].query_selector("tbody")
                )
                all_tr: list[ElementHandle] = (
                    await table_striped_body.query_selector_all("tr")
                )
                if all_tr and isinstance(all_tr, list):
                    del all_tr[0]
                    for tr in all_tr:
                        coins: ElementHandle = await tr.query_selector(".pl-20")
                        sell_and_buy_element: ElementHandle = (
                            await tr.query_selector("td:nth-of-type(3)")
                        )
                        if sell_and_buy_element:
                            sale: ElementHandle = await tr.query_selector(
                                "span:nth-of-type(2)"
                            )
                            buy: ElementHandle = await tr.query_selector(
                                "span:nth-of-type(1)"
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

    async def save_datas(self) -> None:
        """"""
        try:
            exchange = (
                await self.__exchanges_controller.find_exchanges_for_bank_name(
                    bank_name="BCA", verify_only=True
                )
            )
            if not exchange:
                exchange_entitie = ExchangeBase(
                    bank_name="BCA", exchanges_values=self.__datas_json
                )
                result: bool = await self.__exchanges_controller.create(
                    exchange_entitie
                )
                return result
            else:
                result: bool = await self.__exchanges_controller.update(
                    bank_name="BCA", exchanges_values=self.__datas_json
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
