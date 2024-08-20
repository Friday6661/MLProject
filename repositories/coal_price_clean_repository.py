from typing import Optional
from sqlalchemy.orm import Session
from models.coal_price_clean_model import CoalPriceClean
from repositories.generic_repository import GenericRepository

class CoalPriceRepository(GenericRepository[CoalPriceClean]):
    def __init__(self, db: Session):
        super().__init__(db, CoalPriceClean)