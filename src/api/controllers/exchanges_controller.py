from typing import Optional
from datetime import datetime

from src.api.entities import ExchangeBase
from src.log import logg
from src.storage.configs import session
from src.storage.models import Exchanges


class ExchangesController:
    """
    Controller for managing operations related to exchanges in the database.
    """

    @classmethod
    async def create(cls, model: ExchangeBase) -> bool:
        """
        Create a new exchange entry in the database.

        Args:
            model (ExchangeBase): The exchange data model containing bank name and exchange values.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
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
        """
        Find exchanges for a specific bank name.

        Args:
            bank_name (str): The name of the bank to search for.
            verify_only (bool, optional): If True, return only a boolean indicating existence. Defaults to False.

        Returns:
            None | Exchanges: The exchange record if found, or None if `verify_only` is False.
            bool: True if the exchange exists, False otherwise (if `verify_only` is True).
        """
        with session() as _session:
            response = (
                _session.query(Exchanges).filter_by(bank_name=bank_name).first()
            )
            if response:
                return response if not verify_only else True
            return None if not verify_only else False

    @classmethod
    async def find_all_exchanges(cls) -> list | list[Exchanges]:
        """
        Retrieve all exchange records from the database.

        Returns:
            list | list[Exchanges]: A list of all exchange records.
        """
        with session() as _session:
            response = _session.query(Exchanges).all()
            return response

    @classmethod
    async def update(cls, bank_name: str, exchanges_values: list[dict]) -> bool:
        """
        Update the exchange values for a specific bank.

        Args:
            bank_name (str): The name of the bank to update.
            exchanges_values (list[dict]): The new exchange values to be set.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
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
