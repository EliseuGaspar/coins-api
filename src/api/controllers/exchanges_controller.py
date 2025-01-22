from typing import Optional
from datetime import datetime

from src.api.entities import ExchangeBase
from src.log import logg
from src.storage.configs import session
from src.storage.models import Exchanges


class ExchangesController:

    @classmethod
    async def create(cls, model: ExchangeBase) -> bool:
        exchange = Exchanges(
            bank_name=model.bank_name, exchanges_values=model.exchanges_values
        )
        with session() as _session:
            try:
                _session.add(exchange)
                _session.commit()
                logg.info_message(f"new registered exchange({model.bank_name})")
                return True
            except Exception as e:
                logg.info_message(f"failure to register new exchange({e})")
                return False

    @classmethod
    async def find_exchanges_for_bank_name(
        cls, bank_name: str, verify_only: bool = False
    ) -> None | Exchanges:
        """"""
        with session() as _session:
            response = (
                _session.query(Exchanges).filter_by(bank_name=bank_name).first()
            )
            if response:
                return response if not verify_only else True
            return None if not verify_only else False

    @classmethod
    async def find_all_exchanges(cls) -> list | list[Exchanges]:
        """"""
        with session() as _session:
            response = _session.query(Exchanges).all()
            return response

    @classmethod
    async def update(cls, bank_name: str, exchanges_values: list[dict]) -> bool:
        """"""
        exchange: Optional[Exchanges] = await cls.find_exchanges_for_bank_name(
            bank_name
        )
        if not exchange:
            return False
        with session() as _session:
            try:
                exchange.exchanges_values = exchanges_values
                exchange.updated_at = datetime.now()
                _session.add(exchange)
                _session.commit()
                return True
            except Exception as e:
                logg.info_message(f"failure to update exchange({e})")
                return False
