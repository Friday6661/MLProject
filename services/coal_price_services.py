# services/coal_price_services.py
from models.coal_price_model import CoalPrice
from repositories.coal_price_repository import CoalPriceRepository
from models.dto.coal_price_request import CoalPriceRequest
from sqlalchemy.orm import Session

class CoalPriceService:
    def __init__(self, db: Session):
        self.repo = CoalPriceRepository(db)

    def read_all_coal_price_service(self):
        return self.repo.get_all()

    def read_coal_price_by_id_service(self, coal_price_id: int):
        return self.repo.get_by_id(coal_price_id)

    def create_coal_price_service(self, coal_price_request: CoalPriceRequest):
        coal_price = CoalPrice(
            daily_coal_price = coal_price_request.daily_coal_price
        )
        return self.repo.create(coal_price)

    def delete_coal_price_service(self, coal_price_id: int):
        coal_price = self.repo.get_by_id(coal_price_id)
        if coal_price is None:
            return None
        self.repo.delete(coal_price)
        return coal_price

    def update_coal_price_service(self, coal_price_id: int, coal_price_request: CoalPriceRequest):
        coal_price = self.repo.get_by_id(coal_price_id)
        if coal_price is None:
            return None
        coal_price.daily_coal_price = coal_price_request.daily_coal_price
        return self.repo.update(coal_price)