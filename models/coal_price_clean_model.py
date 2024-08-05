from database import Base1
from sqlalchemy import Column, Integer, DECIMAL

class CoalPriceClean(Base1):
    __tablename__ = 'T_COALPRICECLEAN'

    id = Column(Integer, primary_key=True, index=True)
    daily_coal_price = Column(DECIMAL(10, 5)) 