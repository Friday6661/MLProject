# controllers/komtrax_controller.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from models.dto.monthly_sales_request import MonthlySalesRequest
from services.monthly_sales_services import MonthlySalesService
from database import SessionLocal

router = APIRouter()

def get_db_monthly_sales():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db_monthly_sales)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_monthly_sales(db: db_dependency):
    service = MonthlySalesService(db)
    return service.read_all_monthly_sales_service(db)

@router.get("/{monthly_sales_id}", status_code=status.HTTP_200_OK)
async def read_komtrax_by_id(db: db_dependency, monthly_sales_id: int = Path(gt=0)):
    service = MonthlySalesService(db)
    monthly_sales_service_response = service.read_all_monthly_sales_by_id_service(db, monthly_sales_id)
    if monthly_sales_service_response is not None:
        return monthly_sales_service_response
    raise HTTPException(status_code=404, detail='Data not found')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_monthly_sales(db: db_dependency, monthly_sales_request: MonthlySalesRequest):
    service = MonthlySalesService(db)
    return service.create_monthly_sales_service(db, monthly_sales_request)

@router.put("/{monthly_sales_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_monthly_sales(db: db_dependency, monthly_sales_id: int, monthly_sales_request: MonthlySalesRequest):
    service = MonthlySalesService(db)
    monthly_sales_service_response = service.update_monthly_sales_service(db, monthly_sales_id, monthly_sales_request)
    if monthly_sales_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')
    
@router.delete("/{monthly_sales_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monthly_sales(db:db_dependency, monthly_sales_id: int = Path(gt=0)):
    service = MonthlySalesService(db)
    monthly_sales_service_response = service.delete_monthly_sales_service(db, monthly_sales_id)
    if monthly_sales_service_response is None:
        raise HTTPException(status_code=404, detail='Data not found')
