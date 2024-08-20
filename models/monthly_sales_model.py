from database import Base
from sqlalchemy import Column, String, Integer, DECIMAL, Date

class MonthlySales(Base):
    __tablename__ = 'T_MONTHLYSALES'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    model = Column(String(50), nullable=False)
    serial_number = Column(String(50), nullable=False, unique=True)
    quantity_sold = Column(Integer, nullable=False)
    price_per_unit = Column(DECIMAL(12, 2), nullable=False)
    total_sales = Column(DECIMAL(15, 2), nullable=False)
    sales_region = Column(String(100), nullable=True)
    salesperson = Column(String(100), nullable=True)
    notes = Column(String(255), nullable=True)