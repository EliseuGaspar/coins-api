from sqlalchemy import Boolean, Column, Integer, String

from src.storage.configs import base


class Webhook(base):
    __object_id: str = "webhook_model"
    __tablename__: str = "webhook"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), index=True, nullable=False, unique=True)
    active = Column(Boolean, default=True)

    def __init__(self, url: str) -> None:
        """"""
        self.url: str = url

    def __str__(self) -> str:
        """String representation of the object."""
        return self.url
