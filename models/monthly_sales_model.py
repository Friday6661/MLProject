from database import Base
from sqlalchemy import Column, String, Integer, DATE

class MonthlySales(Base):
    __tablename__ = 'M_MONTHLYSALES'

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=True)
    sec = Column(String, nullable=True)
    gr = Column(DATE, nullable=True)
    model = Column(String, nullable=True)
    model_spec = Column(String, nullable=True)
    sn = Column(String, nullable=True)
    loc = Column(String, nullable=True)
    billing = Column(DATE, nullable=True)
    sm_b = Column(String, nullable=True)
    gov_soe = Column(String, nullable=True)