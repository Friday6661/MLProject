from typing import Optional
from sqlalchemy.orm import Session
from models.monthly_sales_clean_model import MonthlySalesClean
from repositories.generic_repository import GenericRepository

class MonthlySalesCleanRepository(GenericRepository[MonthlySalesClean]):
    def __init__(self, db: Session):
        super().__init__(db, MonthlySalesClean)
    
    def find_by_model(self, model: str) -> Optional[MonthlySalesClean]:
        return self.db.query(MonthlySalesClean).filter(MonthlySalesClean.model == model).first()
