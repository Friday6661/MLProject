from sqlalchemy import Column, Date, Integer
from database import Base1

class ForecastTotalMonthlyStocks(Base1):
    __tablename__ = 'T_FORECASTTOTALMONTHLYSTOCKS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Date)
    total_stocks = Column(Integer)
