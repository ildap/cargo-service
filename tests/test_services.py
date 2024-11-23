import pytest

from app.schemas import Tariffs
from app.models import CargoInsurance
from app.services import NotFoundException


def test_upload_update(cargo_service, db):
    initial_data = {
        "2020-01-01": [
            {"cargo_type": "Glass", "rate": 0.04},
            {"cargo_type": "Other", "rate": 0.06}
        ],
        "2020-02-01": [
            {"cargo_type": "Glass", "rate": 0.05},
            {"cargo_type": "Other", "rate": 0.062}
        ]
    }
    tariffs_initial = Tariffs(tariffs=initial_data)
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

    assert exist is not None, f"Not found cargo_insurance"


def test_read_not_found(cargo_service):
    with pytest.raises(NotFoundException):
        cargo_service.read(0)
