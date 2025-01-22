from src.storage.models import Exchanges


class Convertor:
    """
    Utility class for converting `Exchanges` objects or lists of objects into dictionary representations.
    """

    @classmethod
    def exchange_to_dict(
        cls, exchange: Exchanges | list[Exchanges], many: bool = False
    ) -> dict | list[dict]:
        """
        Converts one or multiple `Exchanges` objects to dictionary format.

        Args:
            exchange (Exchanges | list[Exchanges]): A single `Exchanges` object or a list of them.
            many (bool): Indicates if the input is a list of `Exchanges`. Defaults to False.

        Returns:
            dict | list[dict]: A dictionary representation for a single object or a list of dictionaries for multiple objects.
        """
        if not many:
            return cls._format_exchange(exchange)

        exchange_list: list[dict] = [cls._format_exchange(single) for single in exchange]
        return exchange_list

    @staticmethod
    def _format_exchange(exchange: Exchanges) -> dict:
        """
        Formats a single `Exchanges` object into a dictionary.

        Args:
            exchange (Exchanges): An `Exchanges` object.

        Returns:
            dict: The dictionary representation of the `Exchanges` object.
        """
        updated_date: str = str(exchange.updated_at)
        return {
            "bank_name": exchange.bank_name,
            "exchanges": exchange.exchanges_values,
            "updated_at": updated_date[: updated_date.rfind(".")],
        }
