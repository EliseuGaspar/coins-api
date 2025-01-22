from typing import Optional

from src.api.entities import WebhookBase
from src.log import logg
from src.storage.configs import session
from src.storage.models import Webhook


class WebhookController:

    @classmethod
    async def register_url(cls, model: WebhookBase) -> bool:
        """"""
        url_exist: Webhook = await cls.find_webhook_for_url(model.url)
        if not url_exist:
            with session() as _session:
                try:
                    webhook = Webhook(model.url)
                    _session.add(webhook)
                    _session.commit()
                    logg.info_message(f"new registered url({model.url})")
                    return True
                except Exception as e:
                    logg.info_message(f"failure to register new url({e})")
                    return False

    @classmethod
    async def find_webhook_for_url(cls, url: str) -> Webhook | None:
        """"""
        with session() as _session:
            response: Optional[Webhook] = (
                _session.query(Webhook).filter_by(url=url).first()
            )
            return response

    @classmethod
    async def change_url_status(cls, url: str) -> bool:
        """"""
        webhook: Optional[Webhook] = cls.find_webhook_for_url(url)
        webhook.active = not webhook.active
        with session() as _session:
            try:
                _session.add(webhook)
                _session.commit()
                _session.refresh(webhook)
                return True
            except Exception as e:
                logg.info_message(f"failure to update url state({e})")
                return False

    @classmethod
    async def delete_url(cls, webhook_object: Webhook) -> bool:
        """"""
        with session() as _session:
            try:
                _session.delete(webhook_object)
                _session.commit()
                return True
            except Exception as e:
                logg.info_message(f"failure to delete url({e})")
                return False

    @classmethod
    async def find_all_webhook(
        cls,
    ) -> list[Webhook] | list:
        """"""
        with session() as _session:
            response: list[Webhook] | list = (
                _session.query(Webhook).filter_by(active=True).all()
            )
            return response
