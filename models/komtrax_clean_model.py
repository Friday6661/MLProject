from database import Base1
from sqlalchemy import Column, Integer, DECIMAL

class KomtraxClean(Base1):
    __tablename__ = 'T_KOMTRAXCLEAN'

    id = Column(Integer, primary_key=True, index=True)
    smr = Column(DECIMAL(10, 5))
    working_hour = Column(DECIMAL(10, 5))
    actual_working_hour = Column(DECIMAL(10, 5))