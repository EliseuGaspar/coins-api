# from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.log import configure_global_logging
from .settings import Settings


configure_global_logging()


api = FastAPI(
    title=Settings.app_title,
    description=Settings.app_description,
    version=Settings.app_version,
    contact=Settings.app_dev_contact,
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.debug = Settings.debug

