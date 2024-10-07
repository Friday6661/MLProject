from sqlalchemy import Column, Date, Integer, DECIMAL
from database import Base1

class ForecastMonthlyCoalPrice(Base1):
    __tablename__ = 'T_FORECASTMONTHLYCOALPRICE_M38'

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Date)
    coal_price = Column(DECIMAL(10, 2))