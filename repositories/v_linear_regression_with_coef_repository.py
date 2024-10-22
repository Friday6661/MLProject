from typing import Type
from sqlalchemy.orm import Session
from repositories.generic_repository import GenericRepository
from models.v_linear_regression_with_coef_model import VLinearRegressionWithCoef


class VLinearReegressionWithCoefRepository(GenericRepository[VLinearRegressionWithCoef]):
    def __init__(self, db: Session):
        super().__init__(db, VLinearRegressionWithCoef)