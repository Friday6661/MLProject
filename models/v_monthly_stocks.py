from sqlalchemy import Column, String, Integer
from database import Base

class VMonthlyStocks(Base):
    __tablename__ = 'V_MONTHLYSTOCKS'
    __table_args__ = {'extend_existing': True}

    month = Column(String, primary_key=True)
    total_stocks = Column(Integer)