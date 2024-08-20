from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from models.dto.coal_price_request import CoalPriceRequest
from services.coal_price_services import CoalPriceService
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
    service = CoalPriceService(db)
    return service.read_all_coal_price_service()

@router.get("/{coal_price_id}", status_code=status.HTTP_200_OK)
async def read_coal_price_by_id(db: db_dependency, coal_price_id: int = Path(gt=0)):
    service = CoalPriceService(db)
    coal_price = service.read_coal_price_by_id_service(coal_price_id)
    if coal_price is not None:
        return coal_price
    raise HTTPException(status_code=404, detail='Data not found')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_coal_price(db: db_dependency, coal_price_request: CoalPriceRequest):
    service = CoalPriceService(db)
    return service.create_coal_price_service(coal_price_request)

@router.put("/{coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_coal_price(db: db_dependency, coal_price_id: int, coal_price_request: CoalPriceRequest):
    service = CoalPriceService(db)
    coal_price = service.update_coal_price_service(coal_price_id, coal_price_request)
    if coal_price is None:
        raise HTTPException(status_code=404, detail='Data not found')

@router.delete("/{coal_price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coal_price(db: db_dependency, coal_price_id: int = Path(gt=0)):
    service = CoalPriceService(db)
    coal_price = service.delete_coal_price_service(coal_price_id)
    if coal_price is None:
        raise HTTPException(status_code=404, detail='Data not found')
