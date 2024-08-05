from typing import Optional
from sqlalchemy.orm import Session
from models.monthly_sales_model import MonthlySales
from repositories.generic_repository import GenericRepository

class MonthlySalesRepository(GenericRepository[MonthlySales]):
    def __init__(self, db: Session):
        super().__init__(db, MonthlySales)
    
    def find_by_model(self, model: str) -> Optional[MonthlySales]:
        return self.db.query(MonthlySales).filter(MonthlySales.model == model).first()
