# controllers/komtrax_controller.py
from io import BytesIO
import json
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from helper.jwt_helper import JWTAuthHelper
from models.dto.komtrax_request import KomtraxRequest
from services.komtrax_services import KomtraxService
from database import SessionLocal

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db_komtrax():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Annotated[Session, Depends(get_db_komtrax)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_komtrax(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = KomtraxService(db)
    return service.read_all_komtrax_service()

@router.get("/{komtrax_id}", status_code=status.HTTP_200_OK)
async def read_komtrax_by_id(komtrax_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = KomtraxService(db)
    komtrax_service_response = service.read_komtrax_by_id_service(komtrax_id)
    if komtrax_service_response is not None:
        return komtrax_service_response
    raise HTTPException(status_code=404, detail='Data not found')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_komtrax(komtrax_request: KomtraxRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = KomtraxService(db)
    return service.create_komtrax_service(komtrax_request)

@router.put("/{komtrax_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_komtrax(komtrax_id: int, komtrax_request: KomtraxRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = KomtraxService(db)
    komtrax_service_response = service.update_komtrax_service(komtrax_id, komtrax_request)
    if komtrax_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')
    
@router.delete("/{komtrax_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_komtrax(komtrax_id: int = Path(gt=0), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
    service = KomtraxService(db)
    komtrax_service_response = service.delete_komtrax_service(komtrax_id)
    if komtrax_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')
    
@router.post("/upload-excel/", status_code=status.HTTP_201_CREATED)
async def upload_excel_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_komtrax)):
    try:
        # config_file_path = "configfile.json"
        # with open(config_file_path, "r") as config_file:
        #     config = json.load(config_file)
        # service_name = "komtraxFile"
        current_user = JWTAuthHelper.get_current_user(token)
        if current_user is None:
            raise HTTPException(status_code=401, detail="Invalid Authentication Credentials")
        service = KomtraxService(db)
        file_content = await file.read()
        file_stream = BytesIO(file_content)
        service.parse_and_create_komtrax(file_stream)
        
        return {"message": "File successfully processed and data saved to database"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
