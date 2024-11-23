from fastapi import FastAPI
from contextlib import asynccontextmanager

from .models import create_models
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before start
    create_models()
    yield
    # before shutdown

app = FastAPI(title=settings.app_name, lifespan=lifespan)

