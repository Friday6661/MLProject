from database import Base
from sqlalchemy import Column, Integer, DECIMAL

class CoalPrice(Base):
    __tablename__ = 'T_COALPRICE'

    id = Column(Integer, primary_key=True, index=True)
    daily_coal_price = Column(DECIMAL(10, 5)) 