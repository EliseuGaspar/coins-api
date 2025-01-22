from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.api.controllers import ExchangesController
from src.api.entities import ExchangeBase
from src.helpers import Convertor
from src.log import logg
from src.storage.models import Exchanges

exchange_routers = APIRouter(prefix="/exchanges", tags=["Exchanges"])


class ExchangesRouters:
    """
    Routers for handling exchanges-related API endpoints.
    """

    @exchange_routers.get(
        '/',
        response_model=list[ExchangeBase],
        description="Return all exchanges registered in the database",
    )
    async def get_all_exchanges() -> JSONResponse:
        """
        Retrieve all registered exchanges from the database.

        Returns:
            JSONResponse: A JSON response containing a list of exchanges or an empty list if no exchanges are found.
        """
        exchanges: list[Exchanges] = await ExchangesController.find_all_exchanges()
        exchnages_formated: list[dict] = Convertor.exchange_to_dict(
            exchange=exchanges, many=True
        )
        logg.info_message("GET /exchanges/ HTTP/1.1 status = 200")
        return JSONResponse(content=exchnages_formated, status_code=200)

    @exchange_routers.get(
        "/detail/{bank_name}",
        response_model=ExchangeBase,
        description="Returns the exchange of a specific bank",
    )
    async def get_one_exchange(bank_name: str = None) -> JSONResponse:
        """
        Retrieve the exchange details for a specific bank.

        Args:
            bank_name (str): The name of the bank whose exchange details are being retrieved.

        Returns:
            JSONResponse: A JSON response containing the exchange details if found,
                          or an error message if the bank is not registered.
        """
        exchange: Optional[Exchanges] = await ExchangesController.find_exchanges_for_bank_name(bank_name)
        if exchange:
            exchnage_formated: dict = Convertor.exchange_to_dict(exchange=exchange)
            logg.info_message(
                f"GET /exchanges/detail/{bank_name}/ HTTP/1.1 status = 200"
            )
            return JSONResponse(content=exchnage_formated, status_code=200)
        logg.info_message(
            f"GET /exchanges/detail/{bank_name}/ HTTP/1.1 status = 204"
        )
        return JSONResponse(
            content={"detail": "There is no record of this bank"},
            status_code=200,
        )
