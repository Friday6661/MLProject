from database import Base
from sqlalchemy import Column, Integer, DECIMAL, String

class Komtrax(Base):
    __tablename__ = 'T_KOMTRAX'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    serial_number = Column(String)
    smr = Column(DECIMAL(10))
    working_hour = Column(DECIMAL(10))
    actual_working_hour = Column(DECIMAL(10))
    longitude_location = Column(DECIMAL(10))
    latitude_location = Column(DECIMAL(10))