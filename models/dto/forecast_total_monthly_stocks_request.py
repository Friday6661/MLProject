from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ForecastTotalMonthlyStocksRequest(BaseModel):
    month: Optional[datetime]
    total_stocks: Optional[int]

    class Config:
        from_attributes = True
        str_strip_whitespace = True