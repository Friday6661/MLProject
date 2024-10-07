from io import BytesIO
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from sqlalchemy.orm import Session

from database import SessionLocal
from database import SessionLocal1
from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from models.dto.monthly_coal_price_request import MonthlyCoalPriceRequest
from services.monthly_coal_price_services import MonthlyCoalPriceService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db_monthly_coal_price():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_db_forecast_monthly_coal_price():
    db1 = SessionLocal1()
    try:
        yield db1
    finally:
        db1.close()

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_monthly_coal_price(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyCoalPriceService(db)
    return service.read_all_monthly_coal_price()

@router.get("/{monthly_coal_price_id}", status_code=status.HTTP_200_OK)
async def read_monthly_coal_price_by_id(monthly_coal_price_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyCoalPriceService(db)
    monthly_coal_price_service_response = service.read_monthly_coal_price(monthly_coal_price_id)
    if monthly_coal_price_service_response is not None:
        return monthly_coal_price_service_response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Coal Price"))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_monthly_coal_price(monthly_coal_price_request: MonthlyCoalPriceRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_data_not_found())
    service = MonthlyCoalPriceService(db)

    create_response = service.create_monthly_coal_price(monthly_coal_price_request)
    if create_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}

@router.put("/{monthly_coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_monthly_coal_price(monthly_coal_price_id: int, monthly_coal_price_request: MonthlyCoalPriceRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyCoalPriceService(db)

    monthly_coal_price_service_response = service.read_monthly_coal_price(monthly_coal_price_id)
    if monthly_coal_price_service_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Coal Price"))
    
    update_monthly_coal_price_service_response = service.update_monthly_coal_price(monthly_coal_price_id, monthly_coal_price_request)
    if update_monthly_coal_price_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_update())
    return {"message": ResponseMessageHelper.success_message_update()}
    
@router.delete("/{monthly_coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monthly_coal_price(monthly_coal_price_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyCoalPriceService(db)

    monthly_coal_price_service_response = service.read_monthly_coal_price(monthly_coal_price_id)
    if monthly_coal_price_service_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Coal Price"))
    
    delete_monthly_coal_price_service_response = service.delete_monthly_coal_price(monthly_coal_price_id)
    if delete_monthly_coal_price_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_delete())
    return {"message": ResponseMessageHelper.success_message_delete()}
    
@router.post("/upload-excel/", status_code=status.HTTP_201_CREATED)
async def upload_excel_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_coal_price)):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=401, detail=ResponseMessageHelper.error_message_jwt_authentication)
        service = MonthlyCoalPriceService(db)
        file_content = await file.read()
        file_stream = BytesIO(file_content)
        parsing_response = service.parse_and_create_monthly_coal_price(file_stream)
        if parsing_response is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_failed_parsing_file())
        
        create_response = service.bulk_create_monthly_coal_price(parsing_response)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": ResponseMessageHelper.success_message_upload_file()}
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/bulk-upload-excel/", status_code=status.HTTP_201_CREATED)
async def bulk_upload_excel_file(
    files: list[UploadFile] = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_monthly_coal_price) 
):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
        
        service = MonthlyCoalPriceService(db)
        list_monthly_coal_price_requests = []

        for file in files:
            file_content = await file.read()
            file_stream = BytesIO(file_content)

            parsing_response = service.parse_and_create_monthly_coal_price(file_stream)
            if parsing_response is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_upload_file())
            
            list_monthly_coal_price_requests.extend(parsing_response)
        
        create_response = service.bulk_create_monthly_coal_price(list_monthly_coal_price_requests)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": ResponseMessageHelper.success_message_upload_file()}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/monthly_indonesian_coal_price/", status_code=status.HTTP_200_OK)
async def read_all_monthly_indonesian_coal_price(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyCoalPriceService(db)
    return service.get_data_v_monthly_coal_price_indonesia()

@router.get("/forecast_monthly_indonesian_coal_price/", status_code=status.HTTP_200_OK)
async def forecast_monthly_indonesian_coal_price(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyCoalPriceService(db)
    forecast_response = service.forecast_monthly_coal_price_indonesia()
    if len(forecast_response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    return forecast_response 

@router.get("/save_forecast_monthly_coal_price/", status_code=status.HTTP_201_CREATED)
async def save_forecast_monthly_coal_price(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db_monthly_coal_price), db1: Session=Depends(get_db_forecast_monthly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlyCoalPriceService(db)
    service1 = MonthlyCoalPriceService(db1)
    forecast_response = service.forecast_monthly_coal_price_indonesia()
    if len(forecast_response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    create_monthly_coal_price_request = service.create_forecast_monthly_coal_price_request(forecast_response)
    if len(create_monthly_coal_price_request) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found())
    bulk_create_response = service1.bulk_create_forecast_monthly_coal_price(create_monthly_coal_price_request)
    if bulk_create_response is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}