from datetime import date
from io import BytesIO
from typing import Any, Dict, List, Optional, Union

from fastapi import HTTPException
from models.monthly_sales_model import MonthlySales
from repositories.monthly_sales_repository import MonthlySalesRepository
from repositories.monthly_sales_clean_repository import MonthlySalesCleanRepository
from models.dto.monthly_sales_request import MonthlySalesRequest
from sqlalchemy.orm import Session
import pandas as pd

from services.general_parshing_services import GeneralParshing

class MonthlySalesService:
    def __init__(self, db: Session):
        self.repo = MonthlySalesRepository(db)
        self.repo_clean = MonthlySalesCleanRepository(db)
        self.parshing_service = GeneralParshing()

    def read_all_monthly_sales_service(self):
        return self.repo.get_all()

    def read_monthly_sales_by_id_service(self, monthly_sales_id: int):
        return self.repo.get_by_id(monthly_sales_id)

    def create_monthly_sales_service(self, monthly_sales_request: MonthlySalesRequest):
        monthly_sales = MonthlySales(
            customer_name = monthly_sales_request.customer_name,
            sec = monthly_sales_request.sec,
            gr = monthly_sales_request.gr,
            model = monthly_sales_request.model,
            model_spec = monthly_sales_request.model_specification,
            sn = monthly_sales_request.sn,
            loc = monthly_sales_request.loc,
            billing = monthly_sales_request.billing,
            sm_b = monthly_sales_request.sm_b,
            gov_soe = monthly_sales_request.gov_soe
        )
        return self.repo.create(monthly_sales)
    
    def bulk_create_monthly_sales_service(self, list_monthly_sales_request: list[MonthlySalesRequest]):
        monthly_sales_requests = [
            MonthlySales(
                customer_name = monthly_sales_request.customer_name,
                sec = monthly_sales_request.sec,
                gr = monthly_sales_request.gr,
                model = monthly_sales_request.model,
                model_spec = monthly_sales_request.model_specification,
                sn = monthly_sales_request.sn,
                loc = monthly_sales_request.loc,
                billing = monthly_sales_request.billing,
                sm_b = monthly_sales_request.sm_b,
                gov_soe = monthly_sales_request.gov_soe
            )
            for monthly_sales_request in list_monthly_sales_request
        ]
        return self.repo.bulk_create(monthly_sales_requests)

    def delete_monthly_sales_service(self, monthly_sales_id: int):
        monthly_sales = self.repo.get_by_id(monthly_sales_id)
        return self.repo.delete(monthly_sales)

    def update_monthly_sales_service(self, monthly_sales_id: int, monthly_sales_request: MonthlySalesRequest):
        monthly_sales = self.repo.get_by_id(monthly_sales_id)
        monthly_sales.model = monthly_sales_request.model
        monthly_sales.model_spec = monthly_sales_request.model_specification
        monthly_sales.sn = monthly_sales_request.sn
        monthly_sales.loc = monthly_sales_request.loc
        monthly_sales.billing = monthly_sales_request.billing
        monthly_sales.sm_b = monthly_sales_request.sm_b
        monthly_sales.gov_soe = monthly_sales_request.gov_soe
        return self.repo.update(monthly_sales)
    
    def parse_and_create_monthly_sales(self, file_stream: BytesIO):
        try:
            service_name = "monthlySalesFile"
            parsed_data = self.parshing_service.parse_file(file_stream, service_name)
            monthly_sales_requests = []
            for data in parsed_data:
                monthly_sales_request = MonthlySalesRequest(
                    customer_name=data["customerNameColumn"] or "",
                    sec=data["secColumn"] or "",
                    gr=self.convert_to_date(data.get("grColumn")),
                    model=data["modelColumn"] or "",
                    model_specification=data["modelSpecificationColumn"] or "",
                    sn=data["snColumn"] or "",
                    loc=data["locColumn"] or "",
                    billing=self.convert_to_date(data.get("billingColumn")),
                    sm_b=data["sm_bColumn"] or "",
                    gov_soe=data["gov_soeColumn"] or "",
                )
                monthly_sales_requests.append(monthly_sales_request)
            return monthly_sales_requests
        except Exception as e:
            raise e
        
    def convert_to_date(self, value: Optional[Union[str, int]]) -> Optional[date]:
        if isinstance(value, int):
            return date.min
        
        if value:
            try:
                return pd.to_datetime(value).date()
            except Exception:
                return date.min
        
        return date.min
