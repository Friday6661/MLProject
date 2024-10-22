from typing import Type
from sqlalchemy.orm import Session
from models.data_filling_model import DataFillingModel
from repositories.generic_repository import GenericRepository
from helper.enum_helper import MLModelsEnum, FillingMethodEnum

class DataFillingRepository(GenericRepository[DataFillingModel]):
    def __init__(self, db: Session):
        super().__init__(db, DataFillingModel)

    def get_by_ml_model(self, ml_model: MLModelsEnum):
        return self.db.query(DataFillingModel).filter(DataFillingModel.ml_model == ml_model).all()
    
    def get_by_filling_method(self, filling_method: FillingMethodEnum):
        return self.db.query(DataFillingModel).filter(DataFillingModel.filling_method == filling_method).all()
    
    def get_by_filling_method_and_ml_model(self, filling_method: FillingMethodEnum, ml_model: MLModelsEnum):
        return self.db.query(DataFillingModel).filter(
            (DataFillingModel.filling_method == filling_method) & 
            (DataFillingModel.ml_model == ml_model)
        ).all()