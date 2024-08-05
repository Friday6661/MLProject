from typing import Optional
from sqlalchemy.orm import Session
from models.coal_price_model import CoalPrice
from repositories.generic_repository import GenericRepository

class CoalPriceRepository(GenericRepository[CoalPrice]):
    def __init__(self, db: Session):
        super().__init__(db, CoalPrice)