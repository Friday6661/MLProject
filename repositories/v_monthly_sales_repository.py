from typing import Type
from sqlalchemy.orm import Session
from models.v_monthly_sales import VMonthlySales
from repositories.generic_repository import GenericRepository

class VMonthlySalesRepository(GenericRepository[VMonthlySales]):
    def __init__(self, db: Session):
        super().__init__(db, VMonthlySales)