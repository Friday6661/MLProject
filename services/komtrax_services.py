from datetime import date
from decimal import Decimal
from io import BytesIO
import json
import math
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
import pandas as pd
from models.komtrax_model import Komtrax
from repositories.komtrax_repository import KomtraxRepository
from models.dto.komtrax_request import KomtraxRequest
from sqlalchemy.orm import Session
from services.filling_missing_value_services import FillingMissingValue
from services.general_parshing_services import GeneralParshing

class KomtraxService:
    def __init__(self, db: Session):
        self.repo = KomtraxRepository(db)
        # with open(config_file_path, "r") as config_file:
        #     config = json.load(config_file)
        # if config_file and service_name:
        #     self.parshing_service = GeneralParshing(config, service_name)
        # else:
        #     self.parshing_service = None
        self.parshing_service = GeneralParshing()
        # self.filling_service = FillingMissingValue()

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

    def delete_komtrax_service(self, komtrax_id: int):
        komtrax = self.repo.get_by_id(komtrax_id)
        if komtrax is None:
            return None
        self.repo.delete(komtrax)
        return komtrax

    def update_komtrax_service(self, komtrax_id: int, komtrax_request: KomtraxRequest):
        komtrax = self.repo.get_by_id(komtrax_id)
        if komtrax is None:
            return None
        komtrax.smr = komtrax_request.smr
        komtrax.working_hour = komtrax_request.working_hour
        komtrax.actual_working_hour = komtrax_request.actual_working_hour
        return self.repo.update(komtrax)
    
    def parse_and_create_komtrax(self, file_stream: BytesIO):
        service_name = "komtraxFile"
        parsed_data = self.parshing_service.parse_file(file_stream, service_name)
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
            self.create_komtrax_service(komtrax_request)
    
    # def parse_and_create_komtrax(self, file_stream: BytesIO):
        # parsed_data = self.parshing_service.parse_file(file_stream)
        # for data in parsed_data:
        #     current_smr = round(Decimal(data["currentSMRColumn"]), 2) if data["currentSMRColumn"] else Decimal('0.00')
        #     sum_monthly_working_hours = round(Decimal(data["sumMonthlyWorkingHoursColumn"]), 2) if data["sumMonthlyWorkingHoursColumn"] else Decimal('0.00')
        #     komtrax_request = KomtraxRequest(
        #         year=data["yearColumn"] or 0,
        #         month=data["monthColumn"] or 0,
        #         model=data["modelColumn"] or "",
        #         type=data["typeColumn"] or "",
        #         serial_number=data["serialNumberColumn"] or "",
        #         customer_name=data["customerNameColumn"] or "",
        #         current_smr=current_smr,
        #         current_smr_time=data["currentSMRTimeColumn"] or date.min(),
        #         sum_monthly_working_hours=sum_monthly_working_hours,
        #         sum_monthly_working_days=data["sumMonthlyWorkingDaysColumn"] or 0
        #     )
        #     self.create_komtrax_service(komtrax_request)

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