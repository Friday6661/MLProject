from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from difflib import SequenceMatcher
from io import BytesIO
import io
import json
import os
import pandas as pd
from sqlalchemy.orm import Session
import xlsxwriter

from models.dto.weekly_coal_price_request import WeeklyCoalPriceRequest
from models.weekly_coal_price_model import WeeklyCoalPrice
from repositories.weekly_coal_price_repository import WeeklyCoalPriceRepository
from services.general_parshing_services import GeneralParshing

class WeeklyCoalPriceService:
    def __init__(self, db: Session):
        self.repo = WeeklyCoalPriceRepository(db)
        self.parshing_service = GeneralParshing()

    def read_all_weekly_coal_price(self):
        return self.repo.get_all()
    
    def read_weekly_coal_price(self, weekly_coal_price_id: int):
        return self.repo.get_by_id(weekly_coal_price_id)
    
    def create_weekly_coal_price(self, weekly_coal_price_request: WeeklyCoalPriceRequest):
        weekly_coal_price = WeeklyCoalPrice(
            date = weekly_coal_price_request.date,
            trade_region_and_specification = weekly_coal_price_request.trade_region_and_specification,
            trade_terms = weekly_coal_price_request.trade_terms,
            price = weekly_coal_price_request.price
        )
        return self.repo.create(weekly_coal_price)
    
    def bulk_create_weekly_coal_price(self, list_weekly_coal_price_request: list[WeeklyCoalPriceRequest]):
        weekly_coal_prices = [
            WeeklyCoalPrice(
                date=request.date,
                trade_region_and_specification=request.trade_region_and_specification,
                trade_terms=request.trade_terms,
                price=request.price
            )
            for request in list_weekly_coal_price_request
        ]
        return self.repo.bulk_create(weekly_coal_prices)
    
    def delete_weekly_coal_price(self, weekly_coal_price_id: int):
        weekly_coal_price = self.repo.get_by_id(weekly_coal_price_id)
        return self.repo.delete(weekly_coal_price)
    
    def update_weekly_coal_price(self, weekly_coal_price_id: int, weekly_coal_price_request: WeeklyCoalPriceRequest):
        weekly_coal_price = self.repo.get_by_id(weekly_coal_price_id)
        weekly_coal_price.date = weekly_coal_price_request.date
        weekly_coal_price.trade_region_and_specification = weekly_coal_price_request.trade_region_and_specification
        weekly_coal_price.trade_terms = weekly_coal_price_request.trade_terms
        weekly_coal_price.price = weekly_coal_price_request.price
        return self.repo.update(weekly_coal_price)
    
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
        # table_header = self.parshing_service.find_table_header(df, service_name, header_row_index)
        df.columns = df.iloc[header_row_index]
        df = df[header_row_index + 1:]
        df = df.reset_index(drop=True)
        df = self.parshing_service.trim_dataframe(df, service_name)
        df = df.loc[:, df.columns.notna()]

        join_data = {
            'date': ['date'],
            'trade regions': ['trade regions'],
            'trade terms' : ['trade terms'],
            'price': ['price']
        }

        # key_dates_column = self.load_header_row_header_table_key(service_name, key_header)
        key_dates_column = key_header
        dates = df[key_dates_column].iloc[1:]  # Mengambil baris 1 ke bawah (tanggal)
        df.columns = df.columns.str.replace(r'\n', '', regex=True).str.strip()
        columns = df.columns[1:]

        for col in columns:
            trade_term = df[col].iloc[0]
            prices = df[col].iloc[1:]

            # Memasukkan data ke join_data
            for date, price in zip(dates, prices):
                join_data['date'].append(date)
                join_data['trade regions'].append(col)
                join_data['trade terms'].append(trade_term)
                # join_data['price'].append(price)
                # Jika price bernilai '-', ganti dengan None
                if price == '-':
                    join_data['price'].append(None)
                else:
                    price_decimal = Decimal(price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    join_data['price'].append(price_decimal)

        # Mengonversi join_data ke DataFrame baru
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
                
                # Normalisasi item
                normalize_item = str(item).lower().strip()
                if is_similar(normalize_item, header_key):
                    return index
        
        raise ValueError(f"Header dengan key '{header_key}' tidak ditemukan dalam file.")

    def parse_and_create_weekly_coal_price(self, file_stream: BytesIO):
        try:
            service_name = "weeklyCoalPriceFile"
            new_file_stream = self.change_file_input_structure(service_name, file_stream)
            parsed_data = self.parshing_service.parse_file(new_file_stream, service_name)
            weekly_coal_price_requests = []
            for data in parsed_data:
                try:
                    # Coba parsing tanggal menggunakan format yang sesuai
                    date_value = pd.to_datetime(data['dateColumn'], errors='raise')
                except (ValueError, TypeError):
                    # Jika parsing gagal, lewati entri ini
                    print(f"Data tidak memiliki tanggal yang valid: {data['dateColumn']}, melewati entri ini.")
                    continue

                if not data.get("tradeRegionAndSpecificationsColumn"):
                    print("Data tidak memiliki wilayah perdagangan yang valid, melewati entri ini.")
                    continue

                if data.get("priceColumn") is None:
                    print(f"Harga tidak tersedia untuk {data['tradeRegionAndSpecificationsColumn']}, melewati entri ini.")
                    continue


                weekly_coal_price_request = WeeklyCoalPriceRequest(
                    date=date_value,
                    trade_region_and_specification=data["tradeRegionAndSpecificationsColumn"],
                    trade_terms=data["tradeTermsColumn"],
                    price=data["priceColumn"]
                )
                weekly_coal_price_requests.append(weekly_coal_price_request)
            return weekly_coal_price_requests
        except Exception as e:
            raise e
    
    # def load_config_json_file(self):
    #     config_file_path = "configfile.json"
    #     with open(config_file_path, "r") as config_file:
    #         config = json.load(config_file)
    #     config = config["fileUploadConfig"]
    #     return config
    
    # def load_header_row_header_table_key(self, service_name: str, header_key: str):
    #     config = self.load_config_json_file();
    #     row_header_table_key = config[service_name][header_key]
    #     return row_header_table_key