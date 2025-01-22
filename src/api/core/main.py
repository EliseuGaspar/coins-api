# from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.log import configure_global_logging

configure_global_logging()


api = FastAPI(
    title="CoinsAPI",
    description="APi de taxa de câmbio dos principais bancos de Angola",
    version="1.0",
    contact={"email": "eliseugaspar4@gmail.com"},
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
