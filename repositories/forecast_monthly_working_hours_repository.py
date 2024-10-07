from typing import Optional, Type
from sqlalchemy.orm import Session
from models.forecast_monthly_working_hours_model import ForecastMontlyWorkingHours
from repositories.generic_repository import GenericRepository

class ForecastMonthlyWorkingHoursRepository(GenericRepository[ForecastMontlyWorkingHours]):
    def __init__(self, db: Session):
        super().__init__(db, ForecastMontlyWorkingHours)