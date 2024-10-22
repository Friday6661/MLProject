from sqlalchemy.orm import Session
from helper.enum_helper import FillingMethodEnum, MLModelsEnum
from models.coefisien_config_model import CoefisienConfigModel
from models.dto.coefisien_config_request import CoefisienConfigRequest
from repositories.coefisien_config_repository import CoefisienConfigRepository

class CoefisienConfigService:
    def __init__(self, db: Session):
        self.coefisien_config_repo = CoefisienConfigRepository(db)

    def get_coefisien_configs(self):
        coefisien_configs = self.coefisien_config_repo.get_all()
        return coefisien_configs
    
    def get_coefisien_config(self, id: int):
        coefisien_config = self.coefisien_config_repo.get_by_id(id)
        return coefisien_config
    
    def get_coefisien_config_by_model(self, model: MLModelsEnum):
        coefisien_configs = self.coefisien_config_repo.get_by_model(model)
        return coefisien_configs
    
    def get_coefisien_config_by_model_and_method(self, model: MLModelsEnum, method: FillingMethodEnum):
        coefisien_configs = self.coefisien_config_repo.get_by_model_and_method(model, method)
        return coefisien_configs
    
    def create_coefisien_config(self, request: CoefisienConfigRequest):
        # Membuat objek CoefisienConfigModel berdasarkan request yang diterima
        coefisien_config = CoefisienConfigModel(
            ml_model=request.ml_model,
            method=request.method,
            value=request.value
        )
        # Menyimpan ke database menggunakan repository
        created_config = self.coefisien_config_repo.create(coefisien_config)
        return created_config