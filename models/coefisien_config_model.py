from sqlalchemy import Column, Integer, DECIMAL, Enum
from database import Base2
from helper.enum_helper import MLModelsEnum, FillingMethodEnum

class CoefisienConfigModel(Base2):
    __tablename__ = 'M_COEFISIENCONFIG'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ml_model = Column(Enum(MLModelsEnum), nullable=False) #berisi enum MLModelsEnum
    method = Column(Enum(FillingMethodEnum), nullable=False) #berisi enum filling method
    value = Column(DECIMAL(10, 2), nullable=False)