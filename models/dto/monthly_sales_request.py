from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from datetime import date

class MonthlySalesRequest(BaseModel):
    customer_name: Optional[str]
    sec: Optional[str]
    gr: Optional[date]
    model: Optional[str]
    model_specification: Optional[str]
    sn: Optional[str]
    loc: Optional[str]
    billing: Optional[date]
    sm_b: Optional[str]
    gov_soe: Optional[str]

    class Config:
        from_attributes = True
        str_strip_whitespace = True
