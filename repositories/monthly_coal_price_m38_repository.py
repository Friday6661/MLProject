from typing import Type
from sqlalchemy.orm import Session
from models.v_monthly_coal_price_m38_model import MonthlyCoalPriceM38
from repositories.generic_repository import GenericRepository

class MonthlyCoalPriceM38Repository(GenericRepository[MonthlyCoalPriceM38]):
    def __init__(self, db: Session):
        super().__init__(db, MonthlyCoalPriceM38)