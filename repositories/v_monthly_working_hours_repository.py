from typing import Type
from sqlalchemy.orm import Session
from models.v_monthly_working_hours import VMonthlyWorkingHours
from repositories.generic_repository import GenericRepository

class VMonthlyWorkingHoursRepository(GenericRepository[VMonthlyWorkingHours]):
    def __init__(self, db: Session):
        super().__init__(db, VMonthlyWorkingHours)