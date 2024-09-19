from database import Base
from sqlalchemy import Column, Integer, DECIMAL, String, DATE

class WeeklyCoalPrice(Base):
    __tablename__ = 'M_WEEKLYCOALPRICE'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DATE, nullable=True)
    trade_region_and_specification = Column(String, nullable=True)
    trade_terms = Column(String, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=True)