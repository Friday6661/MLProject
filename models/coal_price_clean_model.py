from database import Base1
from sqlalchemy import Column, Integer, DECIMAL, Date, String

class CoalPriceClean(Base1):
    __tablename__ = 'T_COALPRICECLEAN'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    price_per_ton = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(10), nullable=False)
    location = Column(String(100), nullable=True)
    grade = Column(String(50), nullable=True)
    supplier = Column(String(100), nullable=True)
    notes = Column(String(255), nullable=True)