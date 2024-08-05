from models.coal_price_model import CoalPrice
from repositories.coal_price_repository import CoalPriceRepository
from models.dto.coal_price_request import CoalPriceRequest
from sqlalchemy.orm import Session

def read_all_coal_price_service(db: Session):
    repo = CoalPriceRepository(db)
    return repo.get_all()

def read_coal_price_by_id_service(db: Session, coal_price_id: int):
    repo = CoalPriceRepository(db)
    return repo.get_by_id(coal_price_id)

def create_coal_price_service(db: Session, coal_price_request: CoalPriceRequest):
    repo = CoalPriceRepository(db)
    coal_price = CoalPrice(
        daily_coal_price = coal_price_request.daily_coal_price
    )
    return repo.create(coal_price)

def delete_coal_price_service(db: Session, coal_price_id: int):
    repo = CoalPriceRepository(db)
    coal_price = repo.get_by_id(coal_price_id)
    if coal_price is None:
        return None
    repo.delete(coal_price)
    return coal_price

def update_coal_price_service(db: Session, coal_price_id: int, coal_price_request: CoalPriceRequest):
    repo = CoalPriceRepository(db)
    coal_price = repo.get_by_id(coal_price_id)
    if coal_price is None:
        return None
    coal_price.daily_coal_price = coal_price_request.daily_coal_price