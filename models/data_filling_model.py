from sqlalchemy import Column, Date, Integer, DECIMAL, Enum
from helper.enum_helper import FillingMethodEnum, MLModelsEnum
from database import Base1

class DataFillingModel(Base1):
    __tablename__ = 'T_DATAFILLING'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ml_model = Column(Enum(MLModelsEnum), nullable= True)
    filling_method = Column(Enum(FillingMethodEnum), nullable=True)
    month = Column(Integer, nullable=True)
    total_sales = Column(Integer, nullable=True)
    total_stocks = Column(Integer, nullable=True)
    total_monthly_working_hours = Column(DECIMAL(10, 2), nullable=True)
    coal_price = Column(DECIMAL(10, 2), nullable=True)
    year = Column(Integer, nullable=True)
