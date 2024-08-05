# models/dto/komtrax_request.py
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class KomtraxRequest(BaseModel):
    smr: Decimal
    working_hour: Decimal
    actual_working_hour: Decimal

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        min_anystr_length = 1
