from pydantic import BaseModel


class WebhookBase(BaseModel):
    __object_id: str = "webhook_entitie"

    url: str
