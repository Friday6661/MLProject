from sqlalchemy import Column, Date, Integer, DECIMAL
from database import Base2

class LinearRegressionResultModel(Base2):
    __tablename__ = 'T_LINEARREGRESSIONRESULT'

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Integer, nullable=True)
    total_stocks = Column(Integer, nullable=True)
    total_monthly_working_hours = Column(DECIMAL(10, 2), nullable=True)
    coal_price = Column(DECIMAL(10,2), nullable=True)
    year = Column(Integer, nullable=True)
    predicted_sales_Recomendation = Column(Integer)
    predicted_sales_Mean = Column(Integer)
    predicted_sales_Median = Column(Integer)
    predicted_sales_Mode = Column(Integer)
    predicted_sales_Min = Column(Integer)
    predicted_sales_Max = Column(Integer)