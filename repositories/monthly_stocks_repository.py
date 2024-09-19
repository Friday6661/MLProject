from typing import Optional, Type
from sqlalchemy.orm import Session
from models.monthly_stocks_model import MonthlyStocks
from repositories.generic_repository import GenericRepository

class MonthlyStocksRepository(GenericRepository[MonthlyStocks]):
    def __init__(self, db: Session):
        super().__init__(db, MonthlyStocks)