from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from helper.enum_helper import FillingMethodEnum, MLModelsEnum

class DataFillingRequest(BaseModel):
    ml_models: MLModelsEnum
    filling_method: FillingMethodEnum
    month: Optional[int]
    total_sales: Optional[int]
    total_stocks: Optional[int]
    total_monthly_working_hours: Optional[Decimal]
    coal_price: Optional[Decimal]
    year: Optional[int]

    class Config:
        from_attributes = True
        str_strip_whitespce = True