import pytest

from app.dependencies import get_cargo_service, get_db


@pytest.fixture(scope='session')
def db():
    return next(get_db())


@pytest.fixture(scope='session')
def cargo_service(db):
    return get_cargo_service(db)


