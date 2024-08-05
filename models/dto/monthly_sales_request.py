# models/dto/komtrax_request.py
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import date

class MonthlySalesRequest(BaseModel):
    model: str
    serial_number: str
    longitude_location: Decimal
    latitude_location: Decimal
    date: date

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        min_anystr_length = 1
