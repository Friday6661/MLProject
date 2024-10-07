from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from datetime import date

class MonthlyCoalPriceRequest(BaseModel):
    date: Optional[date]
    trade_region_and_specification: Optional[str]
    trade_terms: Optional[str]
    price: Optional[Decimal]

    class Config:
        from_attributes = True
        str_strip_whitespce = True