from io import BytesIO
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from sqlalchemy.orm import Session

from database import SessionLocal
from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from models.dto.weekly_coal_price_request import WeeklyCoalPriceRequest
from services.weekly_coal_price_services import WeeklyCoalPriceService


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db_weekly_coal_price():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_weekly_coal_price(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = WeeklyCoalPriceService(db)
    return service.read_all_weekly_coal_price()

@router.get("/{weekly_coal_price_id}", status_code=status.HTTP_200_OK)
async def read_weekly_coal_price_by_id(weekly_coal_price_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = WeeklyCoalPriceService(db)
    weekly_coal_price_service_response = service.read_weekly_coal_price(weekly_coal_price_id)
    if weekly_coal_price_service_response is not None:
        return weekly_coal_price_service_response
    raise HTTPException(status_code=404, detail=ResponseMessageHelper.error_message_data_not_found("Weekly Coal Price"))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_weekly_coal_price(weekly_coal_price_request: WeeklyCoalPriceRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = WeeklyCoalPriceService(db)
    
    create_response = service.create_weekly_coal_price(weekly_coal_price_request)
    if create_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}

@router.put("/{weekly_coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_weekly_coal_price(weekly_coal_price_id: int, weekly_coal_price_request: WeeklyCoalPriceRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = WeeklyCoalPriceService(db)

    weekly_coal_price_service_response = service.read_weekly_coal_price(weekly_coal_price_id)
    if weekly_coal_price_service_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Weekly Coal Price"))
    
    update_weekly_coal_price_service_response = service.update_weekly_coal_price(weekly_coal_price_id, weekly_coal_price_request)
    if update_weekly_coal_price_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_update())
    return {"message": ResponseMessageHelper.success_message_update()}

@router.delete("/{weekly_coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weekly_coal_price(weekly_coal_price_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    service = WeeklyCoalPriceService(db)

    weekly_coal_price_response = service.read_weekly_coal_price(weekly_coal_price_id)
    if weekly_coal_price_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessageHelper.error_message_data_not_found("Weekly Coal Price"))
    delete_weekly_coal_price_service_response = service.delete_weekly_coal_price(weekly_coal_price_id)
    if delete_weekly_coal_price_service_response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_delete())
    return {"message": ResponseMessageHelper.success_message_delete()}

@router.post("/upload-excel/", status_code=status.HTTP_201_CREATED)
async def upload_excel_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication)
        service = WeeklyCoalPriceService(db)
        file_content = await file.read()
        file_stream = BytesIO(file_content)
        
        parsing_response = service.parse_and_create_weekly_coal_price(file_stream)
        if parsing_response is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_failed_parsing_file())
        
        create_response = service.bulk_create_weekly_coal_price(parsing_response)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
        return {"message": ResponseMessageHelper.success_message_upload_file()}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/bulk-upload-excel/", status_code=status.HTTP_201_CREATED)
async def bulk_upload_excel_file(
    files: list[UploadFile] = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_weekly_coal_price)
):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
        
        service = WeeklyCoalPriceService(db)
        list_weekly_coal_price_requests = []

        for file in files:
            file_content = await file.read()
            file_stream = BytesIO(file_content)

            parsing_response = service.parse_and_create_weekly_coal_price(file_stream)
            if parsing_response is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_upload_file())

            list_weekly_coal_price_requests.extend(parsing_response)

        create_response = service.bulk_create_weekly_coal_price(list_weekly_coal_price_requests)
        if create_response is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create)
        return {"message": ResponseMessageHelper.success_message_upload_file()}

    except Exception as e:
        # Mengembalikan pesan error jika terjadi exception
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


            

