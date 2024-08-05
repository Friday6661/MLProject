from models.monthly_sales_model import MonthlySales
from repositories.monthly_sales_repository import MonthlySalesRepository
from models.dto.monthly_sales_request import MonthlySalesRequest
from sqlalchemy.orm import Session

def read_all_monthly_sales_service(db: Session):
    repo = MonthlySalesRepository(db)
    return repo.get_all()

def read_all_monthly_sales_by_id_service(db: Session, monthly_sales_id: int):
    repo = MonthlySalesRepository(db)
    return repo.get_by_id(monthly_sales_id)

def create_monthly_sales_service(db: Session, monthly_sales_request: MonthlySalesRequest):
    repo = MonthlySalesRepository(db)
    monthly_sales = MonthlySales(
        model = monthly_sales_request.model,
        serial_number = monthly_sales_request.serial_number,
        longitude_location = monthly_sales_request.longitude_location,
        latitude_location = monthly_sales_request.latitude_location,
        date = monthly_sales_request.date
    )
    return repo.create(monthly_sales)

def delete_monthly_sales_service(db: Session, monthly_sales_id: int):
    repo = MonthlySalesRepository(db)
    monthly_sales = repo.get_by_id(monthly_sales_id)
    if monthly_sales is None:
        return None
    repo.delete(monthly_sales)
    return monthly_sales

def update_monthly_sales_service(db: Session, monthly_sales_id: int, monthly_sales_request: MonthlySalesRequest):
    repo = MonthlySalesRepository(db)
    monthly_sales = repo.get_by_id(monthly_sales_id)
    if monthly_sales is None:
        return None
    monthly_sales.model = monthly_sales_request.model
    monthly_sales.serial_number = monthly_sales_request.serial_number
    monthly_sales.longitude_location = monthly_sales_request.longitude_location
    monthly_sales.latitude_location = monthly_sales_request.latitude_location
    monthly_sales.date = monthly_sales_request.latitude_location