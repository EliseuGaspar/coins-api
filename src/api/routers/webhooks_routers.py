from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.api.controllers import WebhookController
from src.api.entities import WebhookBase
from src.helpers.webhook_utils import WebhookUtils
from src.log import logg


webhook_routers = APIRouter(prefix="/webhooks", tags=["Webhooks"])


class WebHookRouter:

    @webhook_routers.post("/", response_model=bool, description="")
    async def register_webhook(webhook: WebhookBase = None) -> JSONResponse:
        """"""
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
                content="url inválida ou com defeito!", status_code=400
            )
        logg.info_message("POST /webhook/ HTTP/1.1 status = 400")
        return JSONResponse(
            content="Dados de url obrigatorio!", status_code=400
        )
