from io import BytesIO
import json
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from models.dto.monthly_stocks_request import MonthlyStocksRequest
from services.monthly_stocks_services import MonthlyStocksService
from database import SessionLocal, SessionLocal1

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_db_monthly_stocks():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_forecast_monthly_stocks():
    db = SessionLocal1()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Annotated[Session, Depends(get_db_monthly_stocks)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_monthly_stocks(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyStocksService(db)
    return service.read_all_monthly_stocks_service()

@router.get("/{monthly_stocks_id}", status_code=status.HTTP_200_OK)
async def read_monthly_stocks_by_id(monthly_stocks_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    service = MonthlyStocksService(db)
    monthly_stocks_service_response = service.read_monthly_stocks_by_id_service(monthly_stocks_id)
    if monthly_stocks_service_response is not None:
        return monthly_stocks_service_response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Stocks"))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_monthly_stocks(monthly_stocks_request: MonthlyStocksRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyStocksService(db)

    create_response = service.create_monthly_stocks_service(monthly_stocks_request)
    if create_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}

@router.put("/{monthly_stocks_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_monthly_stocks(monthly_stocks_id: int, monthly_stocks_request: MonthlyStocksRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyStocksService(db)
    
    monthly_stocks_service_response = service.read_all_monthly_stocks_service(monthly_stocks_id)
    if monthly_stocks_service_response is None:
        raise HTTPException(status_code=status, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Stocks"))
    
    update_monthly_stocks_service_response = service.update_monthly_stocks_service(monthly_stocks_id, monthly_stocks_request)
    if update_monthly_stocks_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_update())
    return {"message": ResponseMessageHelper.success_message_update()}

@router.delete("/{monthly_stocks_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monthly_stocks(monthly_stocks_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyStocksService(db)

    monthly_stocks_service_response = service.read_all_monthly_stocks_service(monthly_stocks_id)
    if monthly_stocks_service_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Stocks"))

    delete_monthly_stocks_service_response = service.delete_stock_sales_serive(monthly_stocks_id)
    if delete_monthly_stocks_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_delete())
    return {"message": ResponseMessageHelper.success_message_delete()}

@router.post("/upload-excel/", status_code=status.HTTP_201_CREATED)
async def upload_excel_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
        service = MonthlyStocksService(db)
        file_content = await file.read()
        file_stream = BytesIO(file_content)

        parsing_response = service.parse_and_create_monthly_sales(file_stream)
        if parsing_response is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_failed_parsing_file())
        
        create_response = service.bulk_create_monthly_stock_service(parsing_response)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": ResponseMessageHelper.success_message_create()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/bulk-upload-excel/", status_code=status.HTTP_201_CREATED)
async def bulk_upload_excel_file(
    files: list[UploadFile] = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_monthly_stocks)
):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
        
        service = MonthlyStocksService(db)
        list_monthly_stocks_requests = []

        for file in files:
            file_content = await file.read()
            file_stream = BytesIO(file_content)

            parsing_response = service.parse_and_create_monthly_sales(file_stream)
            if parsing_response is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_failed_parsing_file())
            
            list_monthly_stocks_requests.extend(parsing_response)

        create_response = service.bulk_create_monthly_stock_service(list_monthly_stocks_requests)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": ResponseMessageHelper.success_message_create()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/total_monthly_stocks/", status_code=status.HTTP_200_OK)
async def read_all_total_monthly_stocks(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyStocksService(db)
    return service.get_data_v_monthly_stocks()

@router.get("/forecast_monthly_stocks/", status_code=status.HTTP_200_OK)
async def forecast_monthly_stocks(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyStocksService(db)
    forecast_response = service.forecast_monthly_stocks()
    if len(forecast_response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    return forecast_response

@router.post("/save_forecast_monthly_stocks/", status_code=status.HTTP_201_CREATED)
async def save_forecast_monthly_stocks(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db_monthly_stocks), db1: Session=Depends(get_db_forecast_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyStocksService(db)
    service1 = MonthlyStocksService(db1)
    forecast_response = service.forecast_monthly_stocks()
    if len(forecast_response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    create_request_response = service.create_forecast_monthly_stocks_request(forecast_response)
    if len(create_request_response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    bulk_create_response = service1.bulk_create_forecast_monthly_stocks(create_request_response)
    if bulk_create_response is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}
    


