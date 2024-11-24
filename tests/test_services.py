import pytest
from datetime import datetime

from app.schemas import Tariffs
from app.models import CargoInsurance
from app.services import NotFoundException


def test_upload_update(cargo_service, db):
    initial_data = {
        datetime.strptime("2020-01-01", "%Y-%m-%d").date(): [
            {"cargo_type": "Glass", "rate": 0.041},
            {"cargo_type": "Other", "rate": 0.061}
        ],
        datetime.strptime("2020-02-01", "%Y-%m-%d").date(): [
            {"cargo_type": "Glass", "rate": 0.051},
            {"cargo_type": "Other", "rate": 0.0621}
        ]
    }
    tariffs_initial = Tariffs(root=initial_data)
    list_data = [
        {**cargo, 'date': date} for date, cargos in initial_data.items()
        for cargo in cargos
    ]

    cargo_service.upload(tariffs_initial)

    for cargo_insurance in list_data:
        exist = db.query(CargoInsurance) \
            .filter(CargoInsurance.cargo_type == cargo_insurance['cargo_type']) \
            .filter(CargoInsurance.rate == cargo_insurance['rate']) \
            .filter(CargoInsurance.date == cargo_insurance['date']) \
            .first()

        assert exist is not None, f"Not found cargo_insurance {str(cargo_insurance)}"


def test_read(cargo_service):
    exist = cargo_service.read(1)

    assert exist is not None, "Not found cargo_insurance"


def test_read_not_found(cargo_service):
    with pytest.raises(NotFoundException):
        cargo_service.read(0)
