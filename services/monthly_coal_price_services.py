from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from difflib import SequenceMatcher
from io import BytesIO
import io
import json
import pandas as pd
from sqlalchemy.orm import Session
import xlsxwriter

from models.dto.monthly_coal_price_request import MonthlyCoalPriceRequest
from models.dto.forecast_monthly_coal_price_request import ForecastMonthlyCoalPriceRequest
from models.monthly_coal_price_model import MonthlyCoalPrice
from models.v_monthly_coal_price_m38_model import MonthlyCoalPriceM38
from models.forecast_monthly_coal_price import ForecastMonthlyCoalPrice
from repositories.monthly_coal_price_repository import MonthlyCoalPriceRepository
from repositories.monthly_coal_price_m38_repository import MonthlyCoalPriceM38Repository
from repositories.forecast_monthly_coal_price_repository import ForecastMonthlyCoalPriceRepository
from services.general_parshing_services import GeneralParshing
from services.forecasting_time_series_services import ForecastingTimeSeriesService

class MonthlyCoalPriceService:
    def __init__(self, db: Session):
        self.repo = MonthlyCoalPriceRepository(db)
        self.parshing_service = GeneralParshing()
        self.v_repo = MonthlyCoalPriceM38Repository(db)
        self.forecasting_service = ForecastingTimeSeriesService()
        self.forecasting_repo = ForecastMonthlyCoalPriceRepository(db)

    def read_all_monthly_coal_price(self):
        return self.repo.get_all()
    
    def read_monthly_coal_price(self, monthly_coal_price_id: int):
        return self.repo.get_by_id(monthly_coal_price_id)
    
    def create_monthly_coal_price(self, monthly_coal_price_request: MonthlyCoalPriceRequest):
        monthly_coal_price = MonthlyCoalPrice(
            date = monthly_coal_price_request.date,
            trade_region_and_specification = monthly_coal_price_request.trade_region_and_specification,
            trade_terms = monthly_coal_price_request.trade_terms,
            price = monthly_coal_price_request.price
        )
        return self.repo.create(monthly_coal_price)
    
    def bulk_create_monthly_coal_price(self, list_monthly_coal_price_request: list[MonthlyCoalPriceRequest]):
        monthly_coal_prices = [
            MonthlyCoalPrice(
                date=request.date,
                trade_region_and_specification=request.trade_region_and_specification,
                trade_terms=request.trade_terms,
                price=request.price
            )
            for request in list_monthly_coal_price_request
        ]
        return self.repo.bulk_create(monthly_coal_prices)
    
    def delete_monthly_coal_price(self, monthly_coal_price_id: int):
        monthly_coal_price = self.repo.get_by_id(monthly_coal_price_id)
        return self.repo.delete(monthly_coal_price) 
    
    def update_monthly_coal_price(self, monthly_coal_price_id: int, monthly_coal_price_request: MonthlyCoalPriceRequest):
        monthly_coal_price = self.repo.get_by_id(monthly_coal_price_id)
        monthly_coal_price.date = monthly_coal_price_request.date
        monthly_coal_price.trade_region_and_specification = monthly_coal_price_request.trade_region_and_specification
        monthly_coal_price.trade_terms = monthly_coal_price_request.trade_terms
        monthly_coal_price.price = monthly_coal_price_request.price
        return self.repo.update(monthly_coal_price)
    
    def dataframe_to_excel_stream(self, df: pd.DataFrame, sheet_name: str) -> io.BytesIO:
        file_stream = io.BytesIO()
        with pd.ExcelWriter(file_stream, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        file_stream.seek(0)
        return file_stream
    
    def change_file_input_structure(self, service_name: str, file_stream: BytesIO):
        sheet_name = self.parshing_service.find_sheet_name(file_stream, service_name)
        df = self.parshing_service.load_excel_to_dataframe(file_stream, sheet_name)
        key_header = "(US dollars per metric ton)"
        header_row_index = self.find_table_header_row_index(df, key_header)
        df.columns = df.iloc[header_row_index]
        df = df[header_row_index + 1:]
        df = df.reset_index(drop=True)
        # df = self.parshing_service.trim_dataframe(df, service_name)   
        df = df.loc[:, df.columns.notna()]

        join_data = {
            'date': ['date'],
            'trade regions': ['trade regions'],
            'trade terms': ['trade terms'],
            'price': ['price']
        }

        key_dates_column = key_header
        dates = df[key_dates_column].iloc[1:]
        df.columns = df.columns.str.replace(r'\n', '', regex=True).str.strip()
        columns = df.columns[1:]

        for col in columns:
            trade_term = df[col].iloc[0]
            prices = df[col].iloc[1:]

            for idx, (date, price) in enumerate(zip(dates, prices), start=1):
                try:
                    join_data['date'].append(date)
                    join_data['trade regions'].append(col)
                    join_data['trade terms'].append(trade_term)

                    if price == '-':
                        join_data['price'].append(None)
                    else:
                        price_decimal = Decimal(price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                        join_data['price'].append(price_decimal)
                
                except (InvalidOperation, ValueError) as e:
                    print(f"Error at row {idx} for date {date}, price {price}: {str(e)}")
                    join_data['price'].append(None)

        df_joined = pd.DataFrame(join_data)
        return self.dataframe_to_excel_stream(df_joined, sheet_name)
    
    def find_table_header_row_index(self, df: pd.DataFrame, key_header: str) -> int:
        header_key = key_header.lower()
        if not header_key:
            raise ValueError("Table Header tidak ditemukan")
        
        def is_similar(s1, s2, threshold=0.8):
            return SequenceMatcher(None, s1, s2).ratio() >= threshold
        
        for index, row in df.iterrows():
            for item in row.values:
                if pd.isna(item):
                    continue

                normalize_item = str(item).lower().strip()
                if is_similar(normalize_item, header_key):
                    return index
                
        raise ValueError(f"Header dengan key '{header_key}' tidak ditemukan dalam file.")
    
    def parse_and_create_monthly_coal_price(self, file_stream: BytesIO):
        try:
            service_name = "monthlyCoalPriceFile"
            new_file_stream = self.change_file_input_structure(service_name, file_stream)
            parsed_data = self.parshing_service.parse_file(new_file_stream, service_name)
            monthly_coal_price_requests = []
            for data in parsed_data:
                try:
                    date_value = pd.to_datetime(data['dateColumn'], errors='raise')
                except (ValueError, TypeError):
                    print(f"Data tidak memiliki tanggal yang valid: {data['dateColumn']}, melewati entri ini.")
                    continue

                if not data.get("tradeRegionAndSpecificationsColumn"):
                    print("Data tidak memiliki wilayah perdagangan yang valid, melewati entri ini.")
                    continue

                if data.get("priceColumn") is None:
                    print(f"Harga tidak tersedia untuk {data['tradeRegionAndSpecificationsColumn']}, melewati entri ini.")
                    continue

                monthly_coal_price_request = MonthlyCoalPriceRequest(
                    date = date_value,
                    trade_region_and_specification=data["tradeRegionAndSpecificationsColumn"],
                    trade_terms=data["tradeTermsColumn"],
                    price=data["priceColumn"]
                )
                monthly_coal_price_requests.append(monthly_coal_price_request)
            return monthly_coal_price_requests
        
        except Exception as e:
            raise e
    
    def get_data_v_monthly_coal_price_indonesia(self):
        return self.v_repo.get_all()
    
    def forecast_monthly_coal_price_indonesia(self) -> pd.DataFrame:
        coal_price_indonesia_m38 = self.v_repo.get_all() # load data from view
        coal_price_indonesia_m38_list = []
        for obj in coal_price_indonesia_m38:
            coal_price_indonesia_m38_dict = {
                "date": obj.date,
                "coal_price":obj.coal_price
            }
            coal_price_indonesia_m38_list.append(coal_price_indonesia_m38_dict)

        df_coal_price = self.forecasting_service.create_dataframe_from_list(coal_price_indonesia_m38_list, 'date')
        df_coal_price = df_coal_price.loc[df_coal_price['coal_price'] >= 0]
        y = df_coal_price['coal_price']
        predicted_values_coal_price = self.forecasting_service.run_sarimax_model(y)
        return predicted_values_coal_price
    
    def create_forecast_monthly_coal_price_request(self, predicted_values: pd.Series) -> list[ForecastMonthlyCoalPriceRequest]:
        forecast_coal_price = [
            ForecastMonthlyCoalPriceRequest(
                month=month,
                coal_price= round(coal_price, 2)
            )
            for month, coal_price in zip(predicted_values.index, predicted_values.values)
        ]
        return forecast_coal_price
    
    def bulk_create_forecast_monthly_coal_price(self, list_forecast_coal_price_request: list[ForecastMonthlyCoalPriceRequest]) -> bool:
        forecast_coal_prices = [
            ForecastMonthlyCoalPrice(
                month = forecast_coal_price_request.month,
                coal_price = forecast_coal_price_request.coal_price
            )
            for forecast_coal_price_request in list_forecast_coal_price_request
        ]
        return self.forecasting_repo.bulk_create(forecast_coal_prices)