from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.api.controllers import WebhookController
from src.api.entities import WebhookBase
from src.helpers.webhook_utils import WebhookUtils
from src.log import logg

webhook_routers = APIRouter(prefix="/webhooks", tags=["Webhooks"])


class WebHookRouter:
    """
    Handles webhook-related routes and operations.
    """

    @webhook_routers.post("/", response_model=bool, description="Register a new webhook URL.")
    async def register_webhook(webhook: WebhookBase = None) -> JSONResponse:
        """
        Registers a new webhook URL in the system.

        Args:
            webhook (WebhookBase, optional): An object containing the URL to be registered.

        Returns:
            JSONResponse: A JSON response indicating whether the registration was successful.
                          - 201: Registration successful.
                          - 400: Invalid or missing URL.
                          - 508: Failed to register the URL.
        """
        if webhook:
            valid_webhook: bool = await WebhookUtils.test_url(webhook.url)
            if valid_webhook:
                response: bool = await WebhookController.register_url(webhook)
                logg.info_message(
                    f"POST /webhook/ HTTP/1.1 status = {201 if response else 508}"
                )
                return JSONResponse(
                    content=response, status_code=201 if response else 508
                )
            logg.info_message("POST /webhook/ HTTP/1.1 status = 400")
            return JSONResponse(
                content="Invalid or faulty URL!", status_code=400
            )
        logg.info_message("POST /webhook/ HTTP/1.1 status = 400")
        return JSONResponse(
            content="URL data is required!", status_code=400
        )
