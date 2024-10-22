from sqlalchemy import Column, String, Integer
from database import Base

class VMonthlySales(Base):
    __tablename__ = 'V_MONTHLYSALES'
    __table_args__ = {'extend_existing': True}

    month = Column(String, primary_key=True)
    total_sales = Column(Integer)