from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy.orm import Session

from .schemas import Tariffs
from .schemas import CargoInsurance as CargoInsuranceSchema
from .models import CargoInsurance


class NotFoundException(Exception):
    pass


class CargoServiceInterface(ABC):
    @abstractmethod
    def upload(self, tariffs: Tariffs):
        pass

    @abstractmethod
    def read(self, id: int) -> CargoInsurance:
        pass

    @abstractmethod
    def update(self, cargo_insurance_schema: CargoInsuranceSchema) -> CargoInsurance:
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

    @abstractmethod
    def get_rate(self, date: datetime, type: str) -> float:
        pass


class CargoService(CargoServiceInterface):
    def __init__(self, db: Session):
        self.db = db

    def upload(self, tariffs: Tariffs):
        # get exist cargo_insurances
        existing_cargos = (
            self.db.query(CargoInsurance)
            .filter(
                CargoInsurance.date.in_(tariffs.root.keys())
            )
            .all()
        )

        existing_map = {
            cargo.date.strftime('%Y-%m-%d') + cargo.cargo_type: cargo
            for cargo in existing_cargos
        }
        # create data for save/update
        cargo_insurances = []
        for date, cargos in tariffs.root.items():
            for cargo in cargos:
                key = date.strftime('%Y-%m-%d') + cargo.cargo_type
                if key in existing_map:
                    existing_cargo = existing_map[key]
                    existing_cargo.rate = cargo.rate  # update rate
                    cargo_insurances.append(existing_cargo)
                    print('existing append', existing_cargo)
                else:
                    new_cargo = CargoInsurance(
                        cargo_type=cargo.cargo_type,
                        rate=cargo.rate,
                        date=date
                    )
                    cargo_insurances.append(new_cargo)
                    print('new append', new_cargo)
        # multiple save/update
        self.db.bulk_save_objects(cargo_insurances)
        self.db.commit()

    def read(self, id: int) -> CargoInsurance:
        cargo_insurance = self.db.get(CargoInsurance, id)
        if cargo_insurance is None:
            raise NotFoundException()

        return cargo_insurance

    def update(self, cargo_insurance_schema: CargoInsuranceSchema) -> CargoInsurance:
        cargo_insurance = self.read(cargo_insurance_schema.id)
        # update fields
        cargo_insurance.cargo_type = cargo_insurance_schema.cargo_type
        cargo_insurance.rate = cargo_insurance_schema.rate
        cargo_insurance.date = cargo_insurance_schema.date
        # save
        self.db.commit()
        self.db.refresh(cargo_insurance)
        return cargo_insurance

    def delete(self, id: int):
        cargo_insurance = self.read(id)
        self.db.delete(cargo_insurance)
        self.db.commit()

    def get_rate(self, date: datetime, type: str) -> float:
        cargo_insurance = self.db.query(CargoInsurance) \
            .filter(CargoInsurance.cargo_type == type) \
            .filter(CargoInsurance.date == date) \
            .first()

        if cargo_insurance is None:
            raise NotFoundException

        return cargo_insurance.rate
