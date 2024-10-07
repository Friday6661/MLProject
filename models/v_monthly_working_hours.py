from sqlalchemy import Column, String, Float
from database import Base

class VMonthlyWorkingHours(Base):
    __tablename__ = 'V_MONTHLYWORKINGHOURS'
    __table_args__ = {'extend_existing': True}

    month = Column(String, primary_key=True)
    total_monthly_working_hours = Column(Float)