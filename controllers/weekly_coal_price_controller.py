from io import BytesIO
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from sqlalchemy.orm import Session

from database import SessionLocal
from helper.jwt_helper import JWTAuthHelper
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
async def read_all_komtrax(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = WeeklyCoalPriceService(db)
    return service.read_all_weekly_coal_price()

@router.get("/{weekly_coal_price_id}", status_code=status.HTTP_200_OK)
async def read_coal_price_by_id(weekly_coal_price_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = WeeklyCoalPriceService(db)
    weekly_coal_price_service_response = service.read_weekly_coal_price(weekly_coal_price_id)
    if weekly_coal_price_service_response is not None:
        return weekly_coal_price_service_response
    raise HTTPException(status_code=404, detail='Data not found')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_weekly_coal_price(weekly_coal_price_request: WeeklyCoalPriceRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = WeeklyCoalPriceService(db)
    return service.create_weekly_coal_price(weekly_coal_price_request)

@router.put("/{komtrax_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_weekly_coal_price(weekly_coal_price_id: int, weekly_coal_price_request: WeeklyCoalPriceRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = WeeklyCoalPriceService(db)
    weekly_coal_price_service_response = service.update_weekly_coal_price(weekly_coal_price_id, weekly_coal_price_request)
    if weekly_coal_price_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')

@router.delete("/{weekly_coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weekly_coal_price(weekly_coal_price_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication credentials")
    service = WeeklyCoalPriceService(db)
    weekly_coal_price_service_response = service.delete_weekly_coal_price(weekly_coal_price_id)
    if weekly_coal_price_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')

@router.post("/upload-excel/", status_code=status.HTTP_201_CREATED)
async def upload_excel_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_weekly_coal_price)):
    try:
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
        service = WeeklyCoalPriceService(db)
        file_content = await file.read()
        file_stream = BytesIO(file_content)
        service.parse_and_create_weekly_coal_price(file_stream)

        return {"message": "File successfully processed and data saved to database"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))