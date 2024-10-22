from typing import Optional, Type
from sqlalchemy.orm import Session
from models.forecast_monthly_coal_price import ForecastMonthlyCoalPrice
from repositories.generic_repository import GenericRepository

class ForecastMonthlyCoalPriceRepository(GenericRepository[ForecastMonthlyCoalPrice]):
    def __init__(self, db: Session):
        super().__init__(db, ForecastMonthlyCoalPrice)
    
    def delete_all(self) -> bool:
        try:
            self.db.query(ForecastMonthlyCoalPrice).delete()
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(str(e))
            return False