from typing import Type
from sqlalchemy.orm import Session
from models.weekly_coal_price_model import WeeklyCoalPrice
from repositories.generic_repository import GenericRepository


class WeeklyCoalPriceRepository(GenericRepository[WeeklyCoalPrice]):
    def __init__(self, db: Session):
        super().__init__(db, WeeklyCoalPrice)