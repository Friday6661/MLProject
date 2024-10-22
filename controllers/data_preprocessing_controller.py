from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from sqlalchemy.orm import Session

from database import SessionLocal
from database import SessionLocal1
from helper.enum_helper import FillingMethodEnum, MLModelsEnum
from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from services.filling_missing_value_services import FillingMissingValue

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_controllers/token")

def get_db_raw():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_clean():
    db = SessionLocal1()
    try:
        yield db
    finally:
        db.close()

@router.get("/all-data-filling/", status_code=status.HTTP_200_OK)
async def get_all_data_filling(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_clean)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    filling_missing_value_service = FillingMissingValue(db)
    service_response = filling_missing_value_service.get_all_data_filling()
    if service_response is None:
        return []
    return service_response

@router.get("/all-data-filling-by-ml-model", status_code=status.HTTP_200_OK)
async def get_all_data_filling_by_ml_model(ml_model: MLModelsEnum, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_clean)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    filling_missing_value_service = FillingMissingValue(db)
    service_response = filling_missing_value_service.get_all_data_by_ml_model(ml_model)
    if service_response is None:
        return []
    return service_response

@router.get("/all-data-filling-by-filling-method/", status_code=status.HTTP_200_OK)
async def get_all_data_filling_by_filling_method(filling_method: FillingMethodEnum, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_clean)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    filling_missing_value_service = FillingMissingValue(db)
    service_response = filling_missing_value_service.get_all_data_by_filling_method(filling_method)
    if service_response is None:
        return []
    return service_response

@router.get("/all-data-filling-by-ml-model-and-filling-method/", status_code=status.HTTP_200_OK)
async def get_all_data_fillign_by_ml_model_and_filling_method(ml_model: MLModelsEnum, filling_method: FillingMethodEnum, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_clean)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    filling_missing_value_service = FillingMissingValue(db)
    service_response = filling_missing_value_service.get_all_data_by_filling_method_and_ml_model(filling_method, ml_model)
    if service_response is None:
        return []
    return service_response