from src.storage.models import Exchanges


class Convertor:

    @classmethod
    def exchange_to_dict(
        cls, exchange: Exchanges | list[Exchanges], many: bool = False
    ) -> dict | list[dict]:
        """"""
        if not many:
            bank_name: str = exchange.bank_name
            exchanges_values: list = exchange.exchanges_values
            updated_date: str = str(exchange.updated_at)
            return {
                "bank_name": bank_name,
                "exchanges": exchanges_values,
                "updated_at": updated_date[: updated_date.rfind(".")],
            }
        exchange_list: list[dict] = []
        for single in exchange:
            bank_name: str = single.bank_name
            exchanges_values: list = single.exchanges_values
            updated_date: str = str(single.updated_at)
            exchange_list.append(
                {
                    "bank_name": bank_name,
                    "exchanges": exchanges_values,
                    "updated_at": updated_date[: updated_date.rfind(".")],
                }
            )
        return exchange_list
