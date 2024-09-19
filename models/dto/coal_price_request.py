from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional

class CoalPriceRequest(BaseModel):
    date: date
    price_per_ton: Decimal
    currency: str
    location: Optional[str] = None
    grade: Optional[str] = None
    supplier: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        str_min_length = 1
