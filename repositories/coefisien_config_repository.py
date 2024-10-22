from typing import Type
from sqlalchemy.orm import Session
from helper.enum_helper import FillingMethodEnum, MLModelsEnum
from models.coefisien_config_model import CoefisienConfigModel
from repositories.generic_repository import GenericRepository

class CoefisienConfigRepository(GenericRepository[CoefisienConfigModel]):
    def __init__(self, db: Session):
        super().__init__(db, CoefisienConfigModel)
        
    def get_by_model(self, model: MLModelsEnum):
        return self.db.query(self.model).filter(self.model.ml_model == model).all()
    
    def get_by_model_and_method(self, model: MLModelsEnum, method: FillingMethodEnum):
        return self.db.query(self.model).filter(self.model.ml_model == model, self.model.method == method).all()