from typing import Optional

from playwright.async_api import ElementHandle, Page

from src.api.controllers import ExchangesController
from src.api.entities import ExchangeBase
from src.interfaces import ISites
from src.log import logg


class BIR(ISites):
    """"""

    __object_id: str = "Scrapper_BancoBIR"
    __url: str = "https://www.bir.ao/"
    __exchange_table_class_name: str = ".draggable"

    __datas_json: list[dict] = []
    __exchanges_controller = ExchangesController

    def __init__(self, page: Page):
        """"""
        self.__page: Optional[Page] = page if isinstance(page, Page) else None

    async def scrapy(self) -> bool:
        """"""
        if self.__page:
            exchange_table_element: ElementHandle = (
                await self.__page.query_selector(
                    self.__exchange_table_class_name
                )
            )
            if exchange_table_element:
                exchange_table_body_element: ElementHandle = (
                    await exchange_table_element.query_selector(".slick-track")
                )
                exchange_all_divs_cards_element: list[ElementHandle] = (
                    await exchange_table_body_element.query_selector_all(
                        ".slick-slide"
                    )
                )
                if exchange_all_divs_cards_element and isinstance(
                    exchange_all_divs_cards_element, list
                ):
                    for div in exchange_all_divs_cards_element:
                        coins: ElementHandle = await div.query_selector(
                            ".caption-gray"
                        )
                        sale_and_buy_div_element: list[ElementHandle] = (
                            await div.query_selector_all(
                                ".smalltitle-primary-red"
                            )
                        )
                        if (
                            coins
                            and sale_and_buy_div_element[0]
                            and sale_and_buy_div_element[1]
                        ):
                            self.__datas_json.append(
                                {
                                    "coins": await coins.inner_text(),
                                    "sell": await sale_and_buy_div_element[
                                        0
                                    ].inner_text(),
                                    "buy": await sale_and_buy_div_element[
                                        1
                                    ].inner_text(),
                                }
                            )
                        else:
                            logg.error_message(
                                f"[{self.__object_id}]: error when getting the values ​​of (coin, sell and buy)"
                            )
                            return False
                else:
                    logg.error_message(
                        f"[{self.__object_id}]: error when getting slick divs"
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
                    bank_name="BIR", verify_only=True
                )
            )
            if not exchange:
                exchange_entitie = ExchangeBase(
                    bank_name="BIR", exchanges_values=self.__datas_json
                )
                result: bool = await self.__exchanges_controller.create(
                    exchange_entitie
                )
                return result
            else:
                result: bool = await self.__exchanges_controller.update(
                    bank_name="BIR", exchanges_values=self.__datas_json
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
