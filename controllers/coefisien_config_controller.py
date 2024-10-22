from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal2
from starlette import status
from sqlalchemy.orm import Session

from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from models.dto.coefisien_config_request import CoefisienConfigRequest
from services.coefisien_config_service import CoefisienConfigService


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_controllers/token")
def get_db_clean():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()

@router.get("/", status_code=status.HTTP_200_OK)
async def get_coefisien_configs(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_clean)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    coefisien_config_service = CoefisienConfigService(db)
    service_response = coefisien_config_service.get_coefisien_configs()
    if service_response is None:
        return []
    return service_response

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_coefisien_config(request: CoefisienConfigRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_clean)):
    # Autentikasi user dari token
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    # Memanggil service untuk membuat CoefisienConfig baru
    coefisien_config_service = CoefisienConfigService(db)
    created_config = coefisien_config_service.create_coefisien_config(request)
    if created_config is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
    return {"message": ResponseMessageHelper.success_message_create()}   