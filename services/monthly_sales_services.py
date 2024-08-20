from models.monthly_sales_model import MonthlySales
from repositories.monthly_sales_repository import MonthlySalesRepository
from repositories.monthly_sales_clean_repository import MonthlySalesCleanRepository
from models.dto.monthly_sales_request import MonthlySalesRequest
from sqlalchemy.orm import Session
import pandas as pd

class MonthlySalesService:
    def __init__(self, db: Session):
        self.repo = MonthlySalesRepository(db)
        self.repo_clean = MonthlySalesCleanRepository(db)

    def read_all_monthly_sales_service(self):
        return self.repo.get_all()

    def read_all_monthly_sales_by_id_service(self, monthly_sales_id: int):
        return self.repo.get_by_id(monthly_sales_id)

    def create_monthly_sales_service(self, monthly_sales_request: MonthlySalesRequest):
        monthly_sales = MonthlySales(
            model = monthly_sales_request.model,
            serial_number = monthly_sales_request.serial_number,
            longitude_location = monthly_sales_request.longitude_location,
            latitude_location = monthly_sales_request.latitude_location,
            date = monthly_sales_request.date
        )
        return self.repo.create(monthly_sales)

    def delete_monthly_sales_service(self, monthly_sales_id: int):
        monthly_sales = self.repo.get_by_id(monthly_sales_id)
        if monthly_sales is None:
            return None
        self.repo.delete(monthly_sales)
        return monthly_sales

    def update_monthly_sales_service(self, monthly_sales_id: int, monthly_sales_request: MonthlySalesRequest):
        monthly_sales = self.repo.get_by_id(monthly_sales_id)
        if monthly_sales is None:
            return None
        monthly_sales.model = monthly_sales_request.model
        monthly_sales.serial_number = monthly_sales_request.serial_number
        monthly_sales.longitude_location = monthly_sales_request.longitude_location
        monthly_sales.latitude_location = monthly_sales_request.latitude_location
        monthly_sales.date = monthly_sales_request.latitude_location
        return self.repo.update(monthly_sales)
    
    def clean_raw_data_from_duplicate(self):
        all_sales = self.repo.get_all()
        df = pd.DataFrame([sale.__dict__ for sale in all_sales])

        df = df.drop_duplicates(subset=['model', 'serial_number'], keep='first')
        for _, row in df.iterrows():
            new_record = MonthlySalesRequest(
                model= row['model'],
                serial_number=row['serial_number'],
                longitude_location=row['longitude_location'],
                latitude_location=row['latitude_location'],
                date=row['date']
            )
            self.repo_clean.create(new_record)