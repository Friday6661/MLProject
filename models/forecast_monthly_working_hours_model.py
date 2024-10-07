from sqlalchemy import Column, Date, Integer, DECIMAL
from database import Base1

class ForecastMontlyWorkingHours(Base1):
    __tablename__ = 'T_FORECASTMONTHLYWORKINGHOURS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Date)
    total_monthly_working_hours = Column(DECIMAL(12, 2))