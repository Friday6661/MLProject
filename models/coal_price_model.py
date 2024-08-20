from database import Base
from sqlalchemy import Column, Integer, DECIMAL, String, Date

class CoalPrice(Base):
    __tablename__ = 'T_COALPRICE'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    price_per_ton = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(10), nullable=False)
    location = Column(String(100), nullable=True)
    grade = Column(String(50), nullable=True)
    supplier = Column(String(100), nullable=True)
    notes = Column(String(255), nullable=True)