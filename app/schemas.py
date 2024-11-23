from typing import List, Dict
from datetime import datetime

from pydantic import BaseModel, Field


class CargoInsuranceBase(BaseModel):
    cargo_type: str
    rate: float


class CargoInsurance(CargoInsuranceBase):
    id: int


class Tariffs(BaseModel):
    data: Dict[datetime, List[CargoInsuranceBase]] = Field(alias='tariffs')
