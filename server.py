from apscheduler.schedulers.background import BackgroundScheduler

from src.api.core import api
from src.api.routers import exchange_routers, webhook_routers
from src.scrappy.main import run_bot
from src.storage.configs import base, engine
from src.helpers.webhook_utils import WebhookUtils
from src.storage.models import Exchanges as Exchanges
from src.storage.models import Webhook as Webhook


api.include_router(exchange_routers)
api.include_router(webhook_routers)

base.metadata.create_all(engine)

scheduler = BackgroundScheduler()

scheduler.add_job(run_bot, 'interval', minutes=60)
scheduler.add_job(WebhookUtils.run_tests, 'interval', minutes=50)

scheduler.start()
