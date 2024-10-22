from decimal import Decimal
from pydantic import BaseModel

from helper.enum_helper import FillingMethodEnum, MLModelsEnum


class CoefisienConfigRequest(BaseModel):

    ml_model: MLModelsEnum
    method: FillingMethodEnum
    value: Decimal

    class Config:
        from_attributes = True
        str_strip_whitespace = True