from datetime import date
from io import BytesIO
from typing import Any, Dict, List, Optional, Union

from fastapi import HTTPException
from models.monthly_stocks_model import MonthlyStocks
from repositories.monthly_stocks_repository import MonthlyStocksRepository
from models.dto.monthly_stocks_request import MonthlyStocksRequest
from sqlalchemy.orm import Session
import pandas as pd

from services.general_parshing_services import GeneralParshing

class MonthlyStocksService:
    # def __init__(self, db: Session, config: Dict[str, Any], service_name: str):
    #     self.repo = MonthlyStocksRepository(db)
    #     self.repo.clean = MonthlyStocksRepository(db)
    #     self.parshing_service = GeneralParshing(config, service_name)
    def __init__(self, db: Session):
        self.repo = MonthlyStocksRepository(db)
        self.parshing_service = GeneralParshing()

    def read_all_monthly_stocks_service(self):
        return self.repo.get_all()
    
    def read_monthly_stocks_by_id_service(self, monthly_stock_id: int):
        return self.repo.get_by_id(monthly_stock_id)
    
    def create_monthly_stocks_service(self, monthly_stocks_request: MonthlyStocksRequest):
        monthly_stocks = MonthlyStocks(
            gr = monthly_stocks_request.gr,
            model = monthly_stocks_request.model,
            model_spec = monthly_stocks_request.model_specification,
            sn = monthly_stocks_request.sn,
            stat = monthly_stocks_request.stat,
            loc = monthly_stocks_request.loc,
            aging = monthly_stocks_request.aging,
            sm_b  = monthly_stocks_request.sm_b
        )
        return self.repo.create(monthly_stocks)
    
    def delete_stock_sales_serive(self, monthly_stocks_id: int):
        monthly_stock = self.repo.get_by_id(monthly_stocks_id)
        if monthly_stock is None:
            return None
        self.repo.delete(monthly_stock)

    def update_monthly_stocks_service(self, monthly_stocks_id: int, monthly_stocks_request: MonthlyStocksRequest):
        monthly_stocks = self.repo.get_by_id(monthly_stocks_id)
        if monthly_stocks is None:
            return None
        monthly_stocks.gr = monthly_stocks_request.gr
        monthly_stocks.model = monthly_stocks_request.model
        monthly_stocks.model_spec = monthly_stocks_request.model_specification
        monthly_stocks.sn = monthly_stocks_request.sn
        monthly_stocks.stat = monthly_stocks_request.stat
        monthly_stocks.loc = monthly_stocks_request.loc
        monthly_stocks.aging = monthly_stocks_request.aging
        monthly_stocks.sm_b = monthly_stocks_request.sm_b
        return self.repo.update(monthly_stocks)
    
    def parse_and_create_monthly_sales(self, file_stream: BytesIO):
        service_name = "monthlyStockFile"
        parsed_data = self.parshing_service.parse_file(file_stream, service_name)
        for data in parsed_data:
            monthly_stocks_request = MonthlyStocksRequest(
                gr=data['grColumn'],
                model=data['modelColumn'],
                model_specification=data['modelSpecificationColumn'],
                sn=data['snColumn'],
                stat=data['statColumn'],
                loc=data['locColumn'],
                aging=data['agingColumn'],
                sm_b=data['sm_bColumn']
            )
            self.create_monthly_stocks_service(monthly_stocks_request)
