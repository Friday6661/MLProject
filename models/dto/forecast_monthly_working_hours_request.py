from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

class ForecastMonthlyWorkingHoursRequest(BaseModel):
    month: Optional[datetime]
    total_monthly_working_hours: Optional[Decimal]

    class Config:
        from_attributes = True
        str_strip_whitespace = True