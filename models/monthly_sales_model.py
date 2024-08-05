from database import Base
from sqlalchemy import Column, String, Integer, DECIMAL, Date

class MonthlySales(Base):
    __tablename__ = 'T_MONTHLYSALES'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    serial_number = Column(String)
    longitude_location = Column(DECIMAL(10, 5))
    latitude_location = Column(DECIMAL(10, 5))
    date = Column(Date)