from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from datetime import date

class MonthlySalesRequest(BaseModel):
    date: date
    model: str
    serial_number: str
    quantity_sold: int
    price_per_unit: Decimal
    total_sales: Decimal
    sales_region: Optional[str] = None
    salesperson: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        min_anystr_length = 1
