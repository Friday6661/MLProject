from typing import Optional, Type
from sqlalchemy.orm import Session
from models.forecast_total_monthly_stocks_model import ForecastTotalMonthlyStocks
from repositories.generic_repository import GenericRepository

class ForecastTotalMonthlyStocksRepository(GenericRepository[ForecastTotalMonthlyStocks]):
    def __init__(self, db: Session):
        super().__init__(db, ForecastTotalMonthlyStocks)
    
    def delete_all(self) -> bool:
        try:
            self.db.query(ForecastTotalMonthlyStocks).delete()
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(str(e))
            return False