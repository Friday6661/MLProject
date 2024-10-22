from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

class LinearRegressionResultRequest(BaseModel):
    month: Optional[int]
    total_stocks: Optional[int]
    total_monthly_working_hours: Optional[Decimal]
    coal_price: Optional[Decimal]
    year: Optional[int]
    predicted_sales_Recomendation: Optional[int]
    predicted_sales_Mean: Optional[int]
    predicted_sales_Median: Optional[int]
    predicted_sales_Mode: Optional[int]
    predicted_sales_Min: Optional[int]
    predicted_sales_Max: Optional[int]

    class Config:
        from_attributes = True
        str_strip_whitespce = True