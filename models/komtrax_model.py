from database import Base
from sqlalchemy import Column, Integer, DECIMAL

class Komtrax(Base):
    __tablename__ = 'T_KOMTRAX'

    id = Column(Integer, primary_key=True, index=True)
    smr = Column(DECIMAL(10, 5))
    working_hour = Column(DECIMAL(10, 5))
    actual_working_hour = Column(DECIMAL(10, 5))