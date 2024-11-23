from sqlalchemy.orm import Session
from fastapi import Depends

from app.db import SessionLocal
from app.services import CargoService, CargoServiceInterface


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cargo_service(db: Session = Depends(get_db)) -> CargoServiceInterface:
    return CargoService(db)