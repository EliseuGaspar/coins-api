from pydantic import BaseModel


class ExchangeBase(BaseModel):
    """"""

    __object_id: str = "exchange_entitie"

    bank_name: str
    exchanges_values: list[dict]
