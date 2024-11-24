import pytest

from app.dependencies import get_db
from app.services import CargoService


@pytest.fixture(scope='session')
def db():
    return next(get_db())


@pytest.fixture(scope='session')
def cargo_service(db) -> CargoService:
    return CargoService(db)
