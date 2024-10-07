from datetime import date
from decimal import Decimal
from io import BytesIO
import json
import math
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
import pandas as pd
from models.komtrax_model import Komtrax
from models.v_monthly_working_hours import VMonthlyWorkingHours
from models.forecast_monthly_working_hours_model import ForecastMontlyWorkingHours
from repositories.komtrax_repository import KomtraxRepository
from repositories.v_monthly_working_hours_repository import VMonthlyWorkingHoursRepository
from repositories.forecast_monthly_working_hours_repository import ForecastMonthlyWorkingHoursRepository
from models.dto.komtrax_request import KomtraxRequest
from models.dto.forecast_monthly_working_hours_request import ForecastMonthlyWorkingHoursRequest
from sqlalchemy.orm import Session

from services.filling_missing_value_services import FillingMissingValue
from services.general_parshing_services import GeneralParshing
from services.forecasting_time_series_services import ForecastingTimeSeriesService

class KomtraxService:
    def __init__(self, db: Session):
        self.repo = KomtraxRepository(db)
        self.parshing_service = GeneralParshing()
        self.v_repo = VMonthlyWorkingHoursRepository(db)
        self.forecasting_service = ForecastingTimeSeriesService()
        self.forecasting_repo = ForecastMonthlyWorkingHoursRepository(db)

    def read_all_komtrax_service(self):
        return self.repo.get_all()

    def read_komtrax_by_id_service(self, komtrax_id: int):
        return self.repo.get_by_id(komtrax_id)

    def create_komtrax_service(self, komtrax_request: KomtraxRequest):
        komtrax = Komtrax(
            year = komtrax_request.year,
            month = komtrax_request.month,
            model = komtrax_request.model,
            type = komtrax_request.type,
            serial_number = komtrax_request.serial_number,
            customer_name = komtrax_request.customer_name,
            current_smr = komtrax_request.current_smr,
            current_smr_time = komtrax_request.current_smr_time,
            sum_monthly_working_hours = komtrax_request.sum_monthly_working_hours,
            sum_monthly_working_days = komtrax_request.sum_monthly_working_days
        )
        return self.repo.create(komtrax)
    
    def bulk_create_komtrax_service(self, list_komtrax_request: list[KomtraxRequest]):
        komtraxs = [
            Komtrax(
                year = komtrax_request.year,
                month = komtrax_request.month,
                model = komtrax_request.model,
                type = komtrax_request.type,
                serial_number = komtrax_request.serial_number,
                customer_name = komtrax_request.customer_name,
                current_smr = komtrax_request.current_smr,
                current_smr_time = komtrax_request.current_smr_time,
                sum_monthly_working_hours = komtrax_request.sum_monthly_working_hours,
                sum_monthly_working_days = komtrax_request.sum_monthly_working_days
            )
            for komtrax_request in list_komtrax_request
        ]
        return self.repo.bulk_create(komtraxs)

    def delete_komtrax_service(self, komtrax_id: int):
        komtrax = self.repo.get_by_id(komtrax_id)
        return self.repo.delete(komtrax)

    def update_komtrax_service(self, komtrax_id: int, komtrax_request: KomtraxRequest):
        komtrax = self.repo.get_by_id(komtrax_id)
        komtrax.year = komtrax_request.year
        komtrax.month = komtrax_request.month
        komtrax.model = komtrax_request.model
        komtrax.type = komtrax_request.type
        komtrax.serial_number = komtrax_request.serial_number
        komtrax.customer_name = komtrax_request.customer_name
        komtrax.current_smr = komtrax_request.current_smr
        komtrax.current_smr_time = komtrax_request.current_smr_time
        komtrax.sum_monthly_working_hours = komtrax_request.sum_monthly_working_hours
        komtrax.sum_monthly_working_days = komtrax_request.sum_monthly_working_days
        return self.repo.update(komtrax)
    
    def parse_and_create_komtrax(self, file_stream: BytesIO):
        try:
            service_name = "komtraxFile"
            parsed_data = self.parshing_service.parse_file(file_stream, service_name)
            komtrax_requests = []
            for data in parsed_data:
                current_smr = round(Decimal(data["currentSMRColumn"]), 2) if data["currentSMRColumn"] else Decimal('0.00')
                sum_monthly_working_hours = round(Decimal(data["sumMonthlyWorkingHoursColumn"]), 2) if data["sumMonthlyWorkingHoursColumn"] else Decimal('0.00')
                
                komtrax_request = KomtraxRequest(
                    year=data["yearColumn"],
                    month=data["monthColumn"],
                    model=data["modelColumn"],
                    type=data["typeColumn"],
                    serial_number=data["serialNumberColumn"],
                    customer_name=data["customerNameColumn"],
                    current_smr=current_smr,
                    current_smr_time=data["currentSMRTimeColumn"],
                    sum_monthly_working_hours=sum_monthly_working_hours,
                    sum_monthly_working_days=data["sumMonthlyWorkingDaysColumn"]
                )
                komtrax_requests.append(komtrax_request)
            return komtrax_requests
        except Exception as e:
            raise e

    def filling_missing_value(self):
        data = self.read_all_komtrax_service()
        df = pd.DataFrame(data)
        df_columns = df.columns

        for column in df_columns:
            if column.lower() == 'year':
                df = self.filling_service.fill_column_with_mean(df, column)
            elif column.lower() == 'month':
                df = self.filling_service.fill_column_with_mean(df, column)
            elif column.lower() == 'model':
                df = self.filling_service.fill_column_with_mode(df, column)
            elif column.lower() == 'type':
                df = self.filling_service.fill_column_with_mode(df, column)
            elif column.lower() == 'serial_number':
                df = self.filling_service.fill_column_with_mode(df, column)
            elif column.lower() == 'customer name':
                df = self.filling_service.fill_column_with_unknown(df, column)
            elif column.lower() == 'current_smr':
                df = self.filling_service.fill_column_with_mean(df, column)
            elif column.lower() == 'current_smr_time':
                df = self.filling_service.fill_column_with_mode(df, column)
            elif column.lower() == 'sum_monthly_working_hours':
                df = self.filling_service.fill_column_with_mean(df, column)
            elif column.lower() == 'sum_monthly_working_days':
                df = self.filling_service.fill_column_with_mean(df, column)

    def get_data_v_monthly_working_hours(self):
        return self.v_repo.get_all()
    
    def forecast_monthly_working_hours(self) -> pd.DataFrame:
        monthly_working_hours = self.v_repo.get_all()
        monthly_working_hours_list = []
        for obj in monthly_working_hours:
            monthly_working_hours_dict = {
                "month": obj.month,
                "total_monthly_working_hours": obj.total_monthly_working_hours
            }
            monthly_working_hours_list.append(monthly_working_hours_dict)

        df_monthly_working_hours = self.forecasting_service.create_dataframe_from_list(monthly_working_hours_list, 'month')
        y = df_monthly_working_hours['total_monthly_working_hours']
        predicted_values_monthly_working_hours = self.forecasting_service.run_sarimax_model(y)
        return predicted_values_monthly_working_hours
    
    def create_forecast_monthly_working_hours_request(self, predicted_values: pd.Series) -> list[ForecastMonthlyWorkingHoursRequest]:
        forecast_working_hours = [
            ForecastMonthlyWorkingHoursRequest(
                month=month,
                total_monthly_working_hours = round(total_monthly_working_hours, 2)
            )
            for month, total_monthly_working_hours in zip(predicted_values.index, predicted_values.values)
        ]
        return forecast_working_hours
    
    def bulk_create_forecast_monthly_working_hours(self, list_forecast_monthly_working_hours_request: list[ForecastMonthlyWorkingHoursRequest]) -> bool:
        forecast_working_hours = [
            ForecastMontlyWorkingHours(
                month=forecast_working_hours_request.month,
                total_monthly_working_hours=forecast_working_hours_request.total_monthly_working_hours
            )
            for forecast_working_hours_request in list_forecast_monthly_working_hours_request
        ]
        return self.forecasting_repo.bulk_create(forecast_working_hours)