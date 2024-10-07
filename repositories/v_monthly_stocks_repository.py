from typing import Type
from sqlalchemy.orm import Session
from models.v_monthly_stocks import VMonthlyStocks
from repositories.generic_repository import GenericRepository

class VMonthlyStocksRepository(GenericRepository[VMonthlyStocks]):
    def __init__(self, db: Session):
        super().__init__(db, VMonthlyStocks)