from sqlalchemy.orm import Session
from fastapi import Depends

from .db import SessionLocal
from .services import CargoService, CargoServiceInterface, CargoLoggingService


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cargo_service(db: Session = Depends(get_db)) -> CargoServiceInterface:
    return CargoLoggingService(CargoService(db))
