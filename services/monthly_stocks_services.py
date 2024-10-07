from datetime import date
from io import BytesIO
from typing import Any, Dict, List, Optional, Union

from fastapi import HTTPException
from models.dto.forecast_total_monthly_stocks_request import ForecastTotalMonthlyStocksRequest
from models.monthly_stocks_model import MonthlyStocks
from models.v_monthly_stocks import VMonthlyStocks
from models.forecast_total_monthly_stocks_model import ForecastTotalMonthlyStocks
from repositories.monthly_stocks_repository import MonthlyStocksRepository
from repositories.v_monthly_stocks_repository import VMonthlyStocksRepository
from repositories.forecast_total_monthly_stocks_repository import ForecastTotalMonthlyStocksRepository
from models.dto.monthly_stocks_request import MonthlyStocksRequest
from sqlalchemy.orm import Session
import pandas as pd

from services.general_parshing_services import GeneralParshing
from services.forecasting_time_series_services import ForecastingTimeSeriesService

class MonthlyStocksService:
    def __init__(self, db: Session):
        self.repo = MonthlyStocksRepository(db)
        self.parshing_service = GeneralParshing()
        self.v_repo = VMonthlyStocksRepository(db)
        self.forecasting_service = ForecastingTimeSeriesService()
        self.forecasting_repo = ForecastTotalMonthlyStocksRepository(db)

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
            sm_b  = monthly_stocks_request.sm_b,
            month = monthly_stocks_request.month,
            year = monthly_stocks_request.year

        )
        return self.repo.create(monthly_stocks)
    
    def bulk_create_monthly_stock_service(self, list_monthly_stocks_request: list[MonthlyStocksRequest]):
        monthly_stocks = [
            MonthlyStocks(
                gr = monthly_stocks_request.gr,
                model = monthly_stocks_request.model,
                model_spec = monthly_stocks_request.model_specification,
                sn = monthly_stocks_request.sn,
                stat = monthly_stocks_request.stat,
                loc = monthly_stocks_request.loc,
                aging = monthly_stocks_request.aging,
                sm_b  = monthly_stocks_request.sm_b,
                month = monthly_stocks_request.month,
                year = monthly_stocks_request.year
            )
            for monthly_stocks_request in list_monthly_stocks_request
        ]
        return self.repo.bulk_create(monthly_stocks)
    
    def delete_stock_sales_serive(self, monthly_stocks_id: int):
        monthly_stock = self.repo.get_by_id(monthly_stocks_id)
        return self.repo.delete(monthly_stock)

    def update_monthly_stocks_service(self, monthly_stocks_id: int, monthly_stocks_request: MonthlyStocksRequest):
        monthly_stocks = self.repo.get_by_id(monthly_stocks_id)
        monthly_stocks.gr = monthly_stocks_request.gr
        monthly_stocks.model = monthly_stocks_request.model
        monthly_stocks.model_spec = monthly_stocks_request.model_specification
        monthly_stocks.sn = monthly_stocks_request.sn
        monthly_stocks.stat = monthly_stocks_request.stat
        monthly_stocks.loc = monthly_stocks_request.loc
        monthly_stocks.aging = monthly_stocks_request.aging
        monthly_stocks.sm_b = monthly_stocks_request.sm_b
        monthly_stocks.month = monthly_stocks_request.month
        monthly_stocks.year = monthly_stocks_request.year
        return self.repo.update(monthly_stocks)
    
    def parse_and_create_monthly_sales(self, file_stream: BytesIO):
        try:
            service_name = "monthlyStockFile"
            parsed_data = self.parshing_service.parse_file(file_stream, service_name)
            monthly_stocks_requests = []
            for data in parsed_data:
                monthly_stocks_request = MonthlyStocksRequest(
                    gr=data['grColumn'],
                    model=data['modelColumn'],
                    model_specification=data['modelSpecificationColumn'],
                    sn=data['snColumn'],
                    stat=data['statColumn'],
                    loc=data['locColumn'],
                    aging=data['agingColumn'],
                    sm_b=data['sm_bColumn'],
                    month=data['monthColumn'],
                    year=data['yearColumn']
                )
                monthly_stocks_requests.append(monthly_stocks_request)
            return monthly_stocks_requests
        except Exception as e:
            raise e
        
    def get_data_v_monthly_stocks(self):
        return self.v_repo.get_all()
    
    def forecast_monthly_stocks(self) -> pd.DataFrame:
        monthly_stocks = self.v_repo.get_all()
        monthly_stocks_list = []
        for obj in monthly_stocks:
            monthly_stocks_dict = {
                "month": obj.month,
                "total_stocks": obj.total_stocks
            }
            monthly_stocks_list.append(monthly_stocks_dict)

        df_monthly_stocks = self.forecasting_service.create_dataframe_from_list(monthly_stocks_list, 'month')
        y = df_monthly_stocks['total_stocks']
        predicted_values_monthly_stocks = self.forecasting_service.run_sarimax_model(y)
        return predicted_values_monthly_stocks
    
    def create_forecast_monthly_stocks_request(self, predicted_values: pd.Series) -> list[ForecastTotalMonthlyStocksRequest]:
        forecast_stocks = [
            ForecastTotalMonthlyStocksRequest(
                month=month,
                total_stocks=int(sales)
            )
            for month, sales in zip(predicted_values.index, predicted_values.values)
        ]
        return forecast_stocks
    
    def bulk_create_forecast_monthly_stocks(self, list_forecast_monthly_stocks_request: list[ForecastTotalMonthlyStocksRequest]) -> bool:
        forecast_total_monthly_stocks = [
            ForecastTotalMonthlyStocks(
                month = forecast_monthly_stocks_request.month,
                total_stocks = forecast_monthly_stocks_request.total_stocks
            )
            for forecast_monthly_stocks_request in list_forecast_monthly_stocks_request
        ]
        return self.forecasting_repo.bulk_create(forecast_total_monthly_stocks)
