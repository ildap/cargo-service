import logging

from fastapi import FastAPI, status, Request, Depends
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from .models import create_models
from .config import settings
from .logger import KafkaLogHandler
from .services import NotFoundException, CargoServiceInterface
from .schemas import CargoInsurance, Tariffs
from .dependencies import get_cargo_service


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


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Not found"},
    )


@app.get("/{id}", response_model=CargoInsurance)
def read(id: int, service: CargoServiceInterface = Depends(get_cargo_service)):
    return service.read(id)


@app.post("/upload", status_code=201)
def upload_tariffs(tariffs: Tariffs, service: CargoServiceInterface = Depends(get_cargo_service)):
    return service.upload(tariffs)


@app.put("/", response_model=CargoInsurance)
def update(cargo_insurance: CargoInsurance,
           service: CargoServiceInterface = Depends(get_cargo_service)):
    updated_cargo = service.update(cargo_insurance)
    return updated_cargo


@app.delete("/{id}")
def delete_cargo(id: int, service: CargoServiceInterface = Depends(get_cargo_service)):
    service.delete(id)
    return
