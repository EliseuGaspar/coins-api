from typing import Optional

from playwright.async_api import ElementHandle, Page

from src.api.controllers import ExchangesController
from src.api.entities import ExchangeBase
from src.interfaces import ISites
from src.log import logg


class StandardBank(ISites):
    """"""

    __object_id: str = "Scrapper_BancoStandardBank"
    __url: str = (
        "https://www.standardbank.co.ao/angola/pt/Grandes-Empresas/Mercado-de-Capitais/cambios"
    )
    __exchange_table_class_name: str = ".market-rates__table"

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
                table_striped_body: ElementHandle = (
                    await exchange_table_element.query_selector(
                        ".market-rates__table--body"
                    )
                )
                table_div_elements_list: list[ElementHandle] = (
                    await table_striped_body.query_selector_all(
                        ".market-rates__table--row"
                    )
                )
                if table_div_elements_list and isinstance(
                    table_div_elements_list, list
                ):
                    del table_div_elements_list[0]
                    for div in table_div_elements_list:
                        coins: ElementHandle = await div.query_selector(
                            ".market-rates__table--cell__forex--details__title"
                        )
                        sale: ElementHandle = await div.query_selector(
                            ".market-rates__table--cell:nth-of-type(3)"
                        )
                        buy: ElementHandle = await div.query_selector(
                            ".market-rates__table--cell:nth-of-type(2)"
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
                        f"[{self.__object_id}]: error when getting .market-rates__table--row divs"
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
                    bank_name="Standard Bank", verify_only=True
                )
            )
            if not exchange:
                exchange_entitie = ExchangeBase(
                    bank_name="Standard Bank",
                    exchanges_values=self.__datas_json,
                )
                result: bool = await self.__exchanges_controller.create(
                    exchange_entitie
                )
                return result
            else:
                result: bool = await self.__exchanges_controller.update(
                    bank_name="Standard Bank",
                    exchanges_values=self.__datas_json,
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
