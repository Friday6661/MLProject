from database import Base1
from sqlalchemy import Column, String, Integer, DECIMAL, Date

class MonthlySalesClean(Base1):
    __tablename__ = 'T_MONTHLYSALESCLEAN'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    serial_number = Column(String)
    longitude_location = Column(DECIMAL(10, 5))
    latitude_location = Column(DECIMAL(10, 5))
    date = Column(Date)