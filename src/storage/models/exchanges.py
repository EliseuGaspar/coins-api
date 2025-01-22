from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String

from src.storage.configs import base


class Exchanges(base):
    """Model to represent exchanges for a bank."""

    __object_id: str = "exchanges_model"
    __tablename__: str = "exchanges"

    id = Column(Integer, autoincrement=True, primary_key=True)
    bank_name = Column(String(100), index=True, nullable=False, unique=True)
    exchanges_values = Column(JSON(), nullable=False, default=[])
    updated_at = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, bank_name: str, exchanges_values: list[dict]) -> None:
        """"""
        self.bank_name = bank_name
        self.exchanges_values = exchanges_values

    def __str__(self) -> str:
        """String representation of the object."""
        return f"{self.bank_name}"
