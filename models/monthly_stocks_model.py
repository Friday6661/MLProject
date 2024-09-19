from database import Base
from sqlalchemy import Column, String, Integer, DATE

class MonthlyStocks(Base):
    __tablename__ = 'M_MONTHLYSTOCKS'

    id = Column(Integer, primary_key=True, index=True)
    gr = Column(DATE, nullable=True)
    model = Column(String, nullable=True)
    model_spec = Column(String, nullable=True)
    sn = Column(String, nullable=True)
    stat = Column(String, nullable=True)
    loc = Column(String, nullable=True)
    aging = Column(Integer, nullable=True)
    sm_b = Column(String, nullable=True)