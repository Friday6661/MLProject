from sqlalchemy import Column, Date, Float
from database import Base

class MonthlyCoalPriceM38(Base):
    __tablename__ = 'V_MONTHLYCOALPRICE_M38'
    __table_args__ = {'extend_existing': True} 

    date = Column(Date, primary_key=True)
    coal_price = Column(Float)