from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class KomtraxRequest(BaseModel):
    model: str
    serial_number: str
    smr: Decimal
    working_hour: Decimal
    actual_working_hour: Decimal
    longitude_location: Decimal
    latitude_location: Decimal

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        min_anystr_length = 1
