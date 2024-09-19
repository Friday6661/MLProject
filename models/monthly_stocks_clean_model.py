from database import Base1
from sqlalchemy import Column, String, Integer, DATE

class MonthlyStocksClean(Base1):
    __tablename__ = 'T_MONTHLYSTOCKSCLEAN'

    id = Column(Integer, primary_key=True, index=True)
    gr = Column(DATE)
    model = Column(String)
    model_spec = Column(String)
    sn = Column(String)
    stat = Column(String)
    loc = Column(String)
    aging = Column(Integer)
    sm_b = Column(String)