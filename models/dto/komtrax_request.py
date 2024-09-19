from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class KomtraxRequest(BaseModel):
    year: Optional[int]
    month: Optional[int]
    model: Optional[str]
    type: Optional[str]
    serial_number: Optional[str]
    customer_name: Optional[str]
    current_smr: Optional[Decimal]
    current_smr_time: Optional[date]
    sum_monthly_working_hours: Optional[Decimal]
    sum_monthly_working_days: Optional[int]

    class Config:
        from_attributes = True
        str_strip_whitespace = True
