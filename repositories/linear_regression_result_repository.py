from typing import Optional, Type
from sqlalchemy.orm import Session
from models.linear_regression_result_model import LinearRegressionResultModel
from repositories.generic_repository import GenericRepository

class LinearRegressionResultRepository(GenericRepository[LinearRegressionResultModel]):
    def __init__(self, db: Session):
        super().__init__(db, LinearRegressionResultModel)