# controllers/komtrax_controller.py
from io import BytesIO
import json
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from models.dto.komtrax_request import KomtraxRequest
from services.komtrax_services import KomtraxService
from database import SessionLocal
from database import SessionLocal1

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db_komtrax():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_forecast_working_hours():
    db1 = SessionLocal1()
    try:
        yield db1
    finally:
        db1.close()

# db_dependency = Annotated[Session, Depends(get_db_komtrax)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_komtrax(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = KomtraxService(db)
    return service.read_all_komtrax_service()

@router.get("/{komtrax_id}", status_code=status.HTTP_200_OK)
async def read_komtrax_by_id(komtrax_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = KomtraxService(db)
    komtrax_service_response = service.read_komtrax_by_id_service(komtrax_id)
    if komtrax_service_response is not None:
        return komtrax_service_response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Komtrax"))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_komtrax(komtrax_request: KomtraxRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = KomtraxService(db)

    create_response = service.create_komtrax_service(komtrax_request)
    if create_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}

@router.put("/{komtrax_id}", status_code=status.HTTP_200_OK)
async def update_komtrax(komtrax_id: int, komtrax_request: KomtraxRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = KomtraxService(db)

    komtrax_service_response = service.read_komtrax_by_id_service(komtrax_id)
    if komtrax_service_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Komtrax"))
    
    update_komtrax_service_response = service.update_komtrax_service(komtrax_id, komtrax_request)
    if update_komtrax_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_update())
    return {"message": ResponseMessageHelper.success_message_update()}
    
@router.delete("/{komtrax_id}", status_code=status.HTTP_200_OK)
async def delete_komtrax(komtrax_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authentication Credentials")
    service = KomtraxService(db)

    komtrax_service_response = service.read_komtrax_by_id_service(komtrax_id)
    if komtrax_service_response is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_data_not_found("Komtrax"))
    
    delete_komtrax_service_response = service.delete_komtrax_service(komtrax_id)
    if delete_komtrax_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_delete())
    return {"message": ResponseMessageHelper.success_message_delete()}
    
@router.post("/upload-excel/", status_code=status.HTTP_201_CREATED)
async def upload_excel_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
        service = KomtraxService(db)
        file_content = await file.read()
        file_stream = BytesIO(file_content)
        
        parsing_response = service.parse_and_create_komtrax(file_stream)
        if parsing_response is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_failed_parsing_file())
        
        create_response = service.bulk_create_komtrax_service(parsing_response)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": ResponseMessageHelper.success_message_upload_file()}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/bulk-upload-excel/", status_code=status.HTTP_201_CREATED)
async def bulk_upload_excel_file(
    files: list[UploadFile] = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_komtrax)
):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
        
        service = KomtraxService(db)
        list_komtrax_requests = []

        for file in files:
            file_content = await file.read()
            file_stream = BytesIO(file_content)

            parsing_response = service.parse_and_create_komtrax(file_stream)
            if parsing_response is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_failed_parsing_file())
            list_komtrax_requests.extend(parsing_response)

        create_response = service.bulk_create_komtrax_service(list_komtrax_requests)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": ResponseMessageHelper.success_message_upload_file()}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/monthly_working_hours/", status_code=status.HTTP_200_OK)
async def read_all_monthly_working_hours(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = KomtraxService(db)
    return service.get_data_v_monthly_working_hours()

@router.get("/forecast_monthly_working_hours/", status_code=status.HTTP_200_OK)
async def forecast_monthly_working_hours(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = KomtraxService(db)
    forecast_response = service.forecast_monthly_working_hours()
    if len(forecast_response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    return forecast_response

@router.get("/save_forecast_monthly_coal_price/", status_code=status.HTTP_201_CREATED)
async def save_forecast_monthly_working_hours(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db_komtrax), db1: Session=Depends(get_db_forecast_working_hours)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = KomtraxService(db)
    service1 = KomtraxService(db1)
    forecast_response = service.forecast_monthly_working_hours()
    if len(forecast_response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    create_monthly_working_hours_request = service.create_forecast_monthly_working_hours_request(forecast_response)
    if len(create_monthly_working_hours_request) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    bulk_create_response = service1.bulk_create_forecast_monthly_working_hours(create_monthly_working_hours_request)
    if bulk_create_response is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}