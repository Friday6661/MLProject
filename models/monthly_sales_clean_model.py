from database import Base1
from sqlalchemy import DATE, Column, String, Integer, DECIMAL, Date

class MonthlySalesClean(Base1):
    __tablename__ = 'T_MONTHLYSALESCLEAN'

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    sec = Column(String)
    gr = Column(DATE)
    model = Column(String)
    model_spec = Column(String)
    sn = Column(String)
    loc = Column(String)
    billing = Column(DATE)
    sm_b = Column(String)
    gov_soe = Column(String)