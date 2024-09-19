from io import BytesIO
import json
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from helper.jwt_helper import JWTAuthHelper
from models.dto.monthly_stocks_request import MonthlyStocksRequest
from services.monthly_stocks_services import MonthlyStocksService
from database import SessionLocal

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_db_monthly_stocks():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Annotated[Session, Depends(get_db_monthly_stocks)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_monthly_stocks(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = MonthlyStocksService(db)
    return service.read_all_monthly_stocks_service()

@router.get("/{monthly_stocks_id}", status_code=status.HTTP_200_OK)
async def read_monthly_stocks_by_id(monthly_stocks_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = MonthlyStocksService(db)
    monthly_stocks_service_response = service.read_monthly_stocks_by_id_service(monthly_stocks_id)
    if monthly_stocks_service_response is not None:
        return monthly_stocks_service_response
    raise HTTPException(status_code=404, detail='Data not found')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_monthly_stocks(monthly_stocks_request: MonthlyStocksRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = MonthlyStocksService(db)
    return service.create_monthly_stocks_service(db, monthly_stocks_request)

@router.put("/{monthly_stocks_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_monthly_stocks(monthly_stocks_id: int, monthly_stocks_request: MonthlyStocksRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = MonthlyStocksService(db)
    monthly_stocks_service_response = service.update_monthly_stocks_service(db, monthly_stocks_id, monthly_stocks_request)
    if monthly_stocks_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')

@router.delete("/{monthly_stocks_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monthly_stocks(monthly_stocks_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = MonthlyStocksService(db)
    monthly_stocks_service_response = service.delete_stock_sales_serive(db, monthly_stocks_id)
    if monthly_stocks_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')

@router.post("/upload-excel/", status_code=status.HTTP_201_CREATED)
async def upload_excel_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_stocks)):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
        config_file_path = "configfile.json"
        with open(config_file_path, "r") as config_file:
            # config = json.load(config_file)
            # service_name = "monthlyStockFile"
            service = MonthlyStocksService(db)
            file_content = await file.read()
            file_stream = BytesIO(file_content)
            service.parse_and_create_monthly_sales(file_stream)
            return {"message": "File successfully processed and data saved to database"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

