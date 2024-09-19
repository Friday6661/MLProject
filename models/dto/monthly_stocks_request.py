from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from datetime import date

class MonthlyStocksRequest(BaseModel):
    gr: Optional[date]
    model: Optional[str]
    model_specification: Optional[str]
    sn: Optional[str]
    stat: Optional[str]
    loc: Optional[str]
    aging: Optional[int]
    sm_b: Optional[str]

    class Config:
        from_attributes = True
        str_strip_whitespace = True
