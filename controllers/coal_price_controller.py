from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from models.dto.coal_price_request import CoalPriceRequest
from services.coal_price_services import (
    create_coal_price_service,
    delete_coal_price_service,
    read_all_coal_price_service,
    read_coal_price_by_id_service,
    read_coal_price_by_id_service,
    update_coal_price_service
)

from database import SessionLocal

router = APIRouter()

def get_db_coal_price():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db_coal_price)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_coal_price(db: db_dependency):
    return read_all_coal_price_service(db)

@router.get("/{coal_price_id}", status_code=status.HTTP_200_OK)
async def read_coal_price_by_id(db: db_dependency, coal_price_id: int = Path(gt=0)):
    coal_price_service_response = read_coal_price_by_id_service(db, coal_price_id)
    if coal_price_service_response is not None:
        return coal_price_service_response
    raise HTTPException(status_code=404, detail='Data not found')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_coal_price(db: db_dependency, coal_price_request: CoalPriceRequest):
    return create_coal_price_service(db, coal_price_request)

@router.put("/{coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_coal_price(db: db_dependency, coal_price_id: int, coal_price_request: CoalPriceRequest):
    coal_price_service_response = update_coal_price_service(db, coal_price_id, coal_price_request)
    if coal_price_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')
    
@router.delete("/{coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_komtrax(db:db_dependency, coal_price_id: int = Path(gt=0)):
    coal_price_service_response = delete_coal_price_service(db, coal_price_id)
    if coal_price_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')
