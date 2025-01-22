from typing import Optional

from playwright.async_api import ElementHandle, Page

from src.api.controllers import ExchangesController
from src.api.entities import ExchangeBase
from src.interfaces import ISites
from src.log import logg


class SOL(ISites):
    """"""

    __object_id: str = "Scrapper_BancoSOL"
    __url: str = "https://www.bancosol.ao/pt/particulares"
    __exchanges_table_class_name: str = ".draggable"
    __exchange_body_table_class_name: str = ".slick-track"
    __exchange_div_class_name: str = ".currency-content"

    __datas_json: list[dict] = []
    __exchanges_controller = ExchangesController

    def __init__(self, page: Page):
        """"""
        self.__page: Optional[Page] = page if isinstance(page, Page) else None

    async def scrapy(self) -> bool:
        """"""
        if self.__page:
            exchanges_table_element: ElementHandle = (
                await self.__page.query_selector_all(
                    self.__exchanges_table_class_name
                )
            )
            if exchanges_table_element[2]:
                exchanges_table_body: ElementHandle = (
                    await exchanges_table_element[2].query_selector(
                        self.__exchange_body_table_class_name
                    )
                )
                if exchanges_table_body:
                    exchanges_divs_elements_list: ElementHandle = (
                        await exchanges_table_body.query_selector_all(
                            self.__exchange_div_class_name
                        )
                    )
                    if exchanges_divs_elements_list and isinstance(
                        exchanges_divs_elements_list, list
                    ):
                        for div in exchanges_divs_elements_list:
                            coins: ElementHandle = await div.query_selector(
                                ".change-text p"
                            )
                            sale: ElementHandle = await div.query_selector(
                                ".sell p:nth-of-type(2)"
                            )
                            buy: ElementHandle = await div.query_selector(
                                ".buy p:nth-of-type(2)"
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
                            f"[{self.__object_id}]: error when getting .currency-content divs"
                        )
                        return False
                else:
                    logg.error_message(
                        f"[{self.__object_id}]: error when getting .slick-track div"
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
                    bank_name="Banco Sol", verify_only=True
                )
            )
            if not exchange:
                exchange_entitie = ExchangeBase(
                    bank_name="Banco Sol", exchanges_values=self.__datas_json
                )
                result: bool = await self.__exchanges_controller.create(
                    exchange_entitie
                )
                return result
            else:
                result: bool = await self.__exchanges_controller.update(
                    bank_name="Banco Sol", exchanges_values=self.__datas_json
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
