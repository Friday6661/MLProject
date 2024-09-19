from database import Base1
from sqlalchemy import DATE, Column, Integer, DECIMAL, String

class KomtraxClean(Base1):
    __tablename__ = 'T_KOMTRAXCLEAN'

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    model = Column(String)
    type = Column(String)
    serial_number = Column(String)
    customer_name = Column(String)
    current_smr = Column(DECIMAL(10, 2))
    current_smr_time = Column(DATE)
    sum_monthly_working_hours = Column(DECIMAL(10, 2))
    sum_monthly_working_days = Column(Integer)