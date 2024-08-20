# controllers/komtrax_controller.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from models.dto.komtrax_request import KomtraxRequest
from services.komtrax_services import KomtraxService
from database import SessionLocal

router = APIRouter()

def get_db_komtrax():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db_komtrax)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_komtrax(db: db_dependency):
    service = KomtraxService(db)
    return service.read_all_komtrax_service()

@router.get("/{komtrax_id}", status_code=status.HTTP_200_OK)
async def read_komtrax_by_id(db: db_dependency, komtrax_id: int = Path(gt=0)):
    service = KomtraxService(db)
    komtrax_service_response = service.read_komtrax_by_id_service(komtrax_id)
    if komtrax_service_response is not None:
        return komtrax_service_response
    raise HTTPException(status_code=404, detail='Data not found')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_komtrax(db: db_dependency, komtrax_request: KomtraxRequest):
    service = KomtraxService(db)
    return service.create_komtrax_service(komtrax_request)

@router.put("/{komtrax_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_komtrax(db: db_dependency, komtrax_id: int, komtrax_request: KomtraxRequest):
    service = KomtraxService(db)
    komtrax_service_response = service.update_komtrax_service(komtrax_id, komtrax_request)
    if komtrax_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')
    
@router.delete("/{komtrax_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_komtrax(db:db_dependency, komtrax_id: int = Path(gt=0)):
    service = KomtraxService(db)
    komtrax_service_response = service.delete_komtrax_service(komtrax_id)
    if komtrax_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')
