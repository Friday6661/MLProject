from database import Base
from sqlalchemy import Column, Integer, DECIMAL, String, DATE

class Komtrax(Base):
    __tablename__ = 'M_KOMTRAX'

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    model = Column(String, nullable=True)
    type = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)
    current_smr = Column(DECIMAL(10, 2), nullable=True)
    current_smr_time = Column(DATE, nullable=True)
    sum_monthly_working_hours = Column(DECIMAL(10, 2), nullable=True)
    sum_monthly_working_days = Column(Integer, nullable=True)