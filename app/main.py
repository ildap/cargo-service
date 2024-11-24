import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from .models import create_models
from .config import settings
from .logger import KafkaLogHandler


# setup logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# add kafkalog_handler
topic = settings.app_name.replace(' ', '')
kafkalog_handler = KafkaLogHandler(settings.broker_url, topic)
kafkalog_handler.setLevel(logging.INFO)
logger.addHandler(kafkalog_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before start
    create_models()
    logger.info("Application started")
    yield
    # before shutdown
    kafkalog_handler.stop()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
