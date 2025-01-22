from typing import Optional

from src.api.entities import WebhookBase
from src.log import logg
from src.storage.configs import session
from src.storage.models import Webhook


class WebhookController:
    """
    Controller for managing webhook operations in the database.
    """

    @classmethod
    async def register_url(cls, model: WebhookBase) -> bool:
        """
        Register a new webhook URL in the database.

        Args:
            model (WebhookBase): The webhook data model containing the URL to be registered.

        Returns:
            bool: True if the URL was successfully registered, False otherwise.
        """
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
        """
        Find a webhook entry by its URL.

        Args:
            url (str): The URL to search for.

        Returns:
            Webhook | None: The webhook object if found, or None if no entry exists.
        """
        with session() as _session:
            response: Optional[Webhook] = (
                _session.query(Webhook).filter_by(url=url).first()
            )
            return response

    @classmethod
    async def change_url_status(cls, url: str) -> bool:
        """
        Toggle the active status of a webhook URL.

        Args:
            url (str): The URL of the webhook to update.

        Returns:
            bool: True if the status was successfully changed, False otherwise.
        """
        webhook: Optional[Webhook] = await cls.find_webhook_for_url(url)
        if not webhook:
            logg.info_message(f"Webhook not found for URL: {url}")
            return False
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
        """
        Delete a webhook entry from the database.

        Args:
            webhook_object (Webhook): The webhook object to be deleted.

        Returns:
            bool: True if the entry was successfully deleted, False otherwise.
        """
        with session() as _session:
            try:
                _session.delete(webhook_object)
                _session.commit()
                return True
            except Exception as e:
                logg.info_message(f"failure to delete url({e})")
                return False

    @classmethod
    async def find_all_webhook(cls) -> list[Webhook] | list:
        """
        Retrieve all active webhook entries from the database.

        Returns:
            list[Webhook] | list: A list of active webhook entries, or an empty list if none are found.
        """
        with session() as _session:
            response: list[Webhook] | list = (
                _session.query(Webhook).filter_by(active=True).all()
            )
            return response
