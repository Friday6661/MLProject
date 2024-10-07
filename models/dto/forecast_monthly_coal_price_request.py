from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

class ForecastMonthlyCoalPriceRequest(BaseModel):
    month: Optional[datetime]
    coal_price: Optional[Decimal]

    class Config:
        from_attributes = True
        str_strip_whitespace = True