from io import BytesIO
import json
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from models.dto.monthly_sales_request import MonthlySalesRequest
from services.monthly_sales_services import MonthlySalesService
from database import SessionLocal

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_db_monthly_sales():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Annotated[Session, Depends(get_db_monthly_sales)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_monthly_sales(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_sales)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlySalesService(db)
    return service.read_all_monthly_sales_service()

@router.get("/{monthly_sales_id}", status_code=status.HTTP_200_OK)
async def read_monthly_sales_by_id(monthly_sales_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_sales)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlySalesService(db)
    monthly_sales_service_response = service.read_monthly_sales_by_id_service(monthly_sales_id)
    if monthly_sales_service_response is not None:
        return monthly_sales_service_response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Sales"))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_monthly_sales(monthly_sales_request: MonthlySalesRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_sales)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    service = MonthlySalesService(db)
    create_response = service.create_monthly_sales_service(monthly_sales_request)
    if create_response is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}

@router.put("/{monthly_sales_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_monthly_sales(monthly_sales_id: int, monthly_sales_request: MonthlySalesRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_sales)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())

    service = MonthlySalesService(db)
    monthly_sales_service_response = service.read_monthly_sales_by_id_service(monthly_sales_id)
    if monthly_sales_service_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Sales"))
    
    update_monthly_sales_service_response = service.update_monthly_sales_service(monthly_sales_id, monthly_sales_request)
    if update_monthly_sales_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_update())
    return {"message": ResponseMessageHelper.success_message_update()}
    
@router.delete("/{monthly_sales_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monthly_sales(monthly_sales_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_sales)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = MonthlySalesService(db)

    monthly_sales_service_response = service.read_monthly_sales_by_id_service(monthly_sales_id)
    if monthly_sales_service_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Monthly Sales"))
    
    delete_monthly_sales_service_response = service.delete_monthly_sales_service(db, monthly_sales_id)
    if delete_monthly_sales_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_delete())
    return {"message": ResponseMessageHelper.success_message_delete()}

@router.post("/upload-excel/", status_code=status.HTTP_201_CREATED)
async def upload_excel_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_monthly_sales)):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
        service = MonthlySalesService(db)
        file_content = await file.read()
        file_stream = BytesIO(file_content)
        parsing_response = service.parse_and_create_monthly_sales(file_stream)
        if parsing_response is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_failed_parsing_file())
        
        create_response = service.bulk_create_monthly_sales_service(parsing_response)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": "File successfully processed and data saved to database"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/bulk-upload-excel/", status_code=status.HTTP_201_CREATED)
async def bulk_upload_excel_file(
    files: list[UploadFile] = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_monthly_sales)
):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
        
        service = MonthlySalesService(db)
        list_monthly_sales_requests = []

        for file in files:
            file_content = await file.read()
            file_stream = BytesIO(file_content)

            parsing_response = service.parse_and_create_monthly_sales(file_stream)
            if parsing_response is None:
                continue
                # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_failed_parsing_file())
            
            list_monthly_sales_requests.extend(parsing_response)
        
        create_response = service.bulk_create_monthly_sales_service(list_monthly_sales_requests)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": ResponseMessageHelper.success_message_upload_file()}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

