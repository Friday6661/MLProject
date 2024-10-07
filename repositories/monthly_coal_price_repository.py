from typing import Type
from sqlalchemy.orm import Session
from models.monthly_coal_price_model import MonthlyCoalPrice
from repositories.generic_repository import GenericRepository

class MonthlyCoalPriceRepository(GenericRepository[MonthlyCoalPrice]):
    def __init__(self, db: Session):
        super().__init__(db, MonthlyCoalPrice)