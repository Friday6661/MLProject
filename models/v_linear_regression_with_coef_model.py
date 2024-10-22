from sqlalchemy import DECIMAL, Column, String, Integer
from database import Base2

class VLinearRegressionWithCoef(Base2):
    __tablename__ = 'V_LINEARREGRESSIONWITHCOEF'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    month = Column(Integer, nullable=True)
    total_stocks = Column(Integer, nullable=True)
    total_monthly_working_hours = Column(DECIMAL(10, 2), nullable=True)
    coal_price = Column(DECIMAL(10,2), nullable=True)
    year = Column(Integer, nullable=True)
    predicted_sales_Recomendation_with_coef = Column(Integer)
    predicted_sales_Mean_with_coef = Column(Integer)
    predicted_sales_Median_with_coef = Column(Integer)
    predicted_sales_Mode_with_coef = Column(Integer)
    predicted_sales_Min_with_coef = Column(Integer)
    predicted_sales_Max_with_coef = Column(Integer)