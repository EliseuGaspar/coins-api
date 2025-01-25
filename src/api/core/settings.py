from os import getenv
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic.config import ConfigDict


load_dotenv()


class _Settings(BaseModel):
    """"""    
    model_config: ConfigDict = ConfigDict(
        frozen=True,
    )

    port: int = int(getenv("port", 8000))
    debug: bool = getenv("debug", "false").lower() == "true"
    mode: str = getenv("mode", "development")
    secret_key: str = getenv("secret_key", "secret_key")

    app_title: str = "CoinsAPI"
    app_description: str = "APi de taxa de câmbio dos principais bancos de Angola"
    app_version: str = "1.0"
    app_dev_contact: dict = {"email": "eliseugaspar4@gmail.com"}

    
Settings = _Settings()
