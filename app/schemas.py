from typing import List, Dict
from datetime import date

from pydantic import BaseModel, RootModel, root_validator


class CargoInsuranceBase(BaseModel):
    cargo_type: str
    rate: float


class CargoInsurance(CargoInsuranceBase):
    id: int


class Tariffs(RootModel[Dict[date, List[CargoInsuranceBase]]]):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        """Schema for keys in yyyy-mm-dd format"""
        schema = handler(core_schema)
        schema.update({
            "type": "object",
            "description": "Keys are dates in 'yyyy-mm-dd' format.",
            "additionalProperties": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "cargo_type": {"type": "string", "example": "Glass"},
                        "rate": {"type": "number", "example": 0.04}
                    }
                }
            },
            "example": {
                "2020-01-01": [
                    {"cargo_type": "Glass", "rate": 0.04},
                    {"cargo_type": "Other", "rate": 0.06}
                ],
                "2020-02-01": [
                    {"cargo_type": "Glass", "rate": 0.05},
                    {"cargo_type": "Other", "rate": 0.07}
                ]
            }
        })
        return schema

    @root_validator(pre=True)
    def validate_keys_are_dates(cls, values):
        for key in values.keys():
            try:
                date.fromisoformat(key)
            except ValueError:
                raise ValueError(f"Key '{key}' is not a valid date in format 'yyyy-mm-dd'")
        return values
