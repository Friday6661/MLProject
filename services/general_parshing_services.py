from datetime import date
import json
from typing import Any, Dict, List, Optional, Type
from decimal import Decimal, InvalidOperation
from io import BytesIO
import pandas as pd
from difflib import SequenceMatcher

class GeneralParshing:
    def __init__(self):
        config_file_path = "configfile.json"
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
        self.config = config["fileUploadConfig"]

    def find_sheet_name(self, file_stream: BytesIO, service_name: str) -> str:
        # Membaca file Excel
        file = pd.ExcelFile(file_stream)
        
        # Mendapatkan nama sheet dari konfigurasi
        sheet_name = self.config[service_name]["sheetName"].lower()

        for file_sheet in file.sheet_names:
            if sheet_name in file_sheet.lower():
                return file_sheet
        
        raise ValueError(f"Sheet '{sheet_name}' tidak ditemukan dalam file.")
    
    def find_table_header_row_index(self, df: pd.DataFrame, service_name: str) -> int:
        header_key = self.config[service_name]["rowHeaderTableKey"].lower()
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

    def find_table_header(self, df: pd.DataFrame, service_name: str, header_row_index: int) -> List[str]:
        parsing_settings = self.config[service_name]["parshingFileSettings"]
        # header_row_index = self.find_table_header_row_index(df, service_name)
        df.columns = df.iloc[header_row_index]
        df = df[header_row_index:]
        df = df.reset_index(drop=True)
        df_columns = df.columns
        table_header = []

        for column_key, column_settings in parsing_settings.items():
            possible_names = column_settings["possibleFileColumnName"]
            found = False
            for name in possible_names:
                if name in df_columns:
                    table_header.append(name)  # Tambahkan nama kolom yang ditemukan
                    found = True
                    break
            if not found:
                table_header.append(None)  # Tambahkan None jika tidak ditemukan

        return table_header
    
    def check_column_data_types(self, df: pd.DataFrame, service_name: str) -> Dict[str, Dict[str, str]]:
        """Memeriksa tipe data dari setiap kolom dalam DataFrame dan membandingkannya dengan tipe data yang diharapkan."""
        parsing_settings = self.config[service_name]["parshingFileSettings"]
        column_data_types = {}

        for column_key, settings in parsing_settings.items():
            possible_names = settings["possibleFileColumnName"]
            found = False
            for name in possible_names:
                if name in df.columns:
                    inferred_type = df[name].dtype
                    expected_type = settings["typeValueDb"]
                    column_data_types[column_key] = {
                        "inferred": str(inferred_type),
                        "expected": expected_type
                    }
                    found = True
                    break
            if not found:
                column_data_types[column_key] = {
                    "inferred": None,
                    "expected": settings["typeValueDb"]
                }

        return column_data_types
    
    def trim_dataframe(self, df: pd.DataFrame, service_name: str) -> pd.DataFrame:
        # Ambil konfigurasi kolom dan tipe data dari configFile.json
        config_columns = self.config[service_name]["parshingFileSettings"]
        config_columns_length = len(config_columns)  # Menghitung jumlah kolom dalam config
        
        # Potong x kolom pertama dari DataFrame
        trimmed_df = df.iloc[:, :config_columns_length]
        
        return trimmed_df

    def convert_value_type(self, value: Any, column_name: str, service_name) -> Any:
        """Melakukan konversi tipe data dari value yang diparsing berdasarkan tipe data yang sesuai dengan database."""
        if pd.isnull(value):
            # Mengembalikan nilai default berdasarkan tipe data yang diharapkan
            column_types = self.check_column_data_types(pd.DataFrame(), service_name)
            expected_type = column_types.get(column_name, {}).get("expected", "object")
            
            if expected_type == "int":
                return -1  # Nilai default untuk integer
            elif expected_type == "str":
                return ""  # Nilai default untuk string
            elif expected_type == "decimal":
                return Decimal('-1.0')  # Nilai default untuk Decimal
            elif expected_type == "date":
                return date.min  # Nilai default untuk date
            else:
                return None

        column_types = self.check_column_data_types(pd.DataFrame(), service_name)
        inferred_type = column_types.get(column_name, {}).get("inferred", "object")
        expected_type = column_types.get(column_name, {}).get("expected", "object")

        try:
            if expected_type == "int":
                # Konversi ke integer
                return int(float(value)) if inferred_type in ['float64', 'object', 'int64'] else int(value)
            elif expected_type == "str":
                # Konversi ke string
                return str(value)
            elif expected_type == "decimal":
                # Konversi ke Decimal
                return Decimal(value) if inferred_type in ['float64', 'int64', 'object'] else Decimal(value)
            elif expected_type == "date":
                # Konversi ke date
                return pd.to_datetime(value).date() if inferred_type in ['object', 'datetime64[ns]'] else value
            else:
                return value
        except (ValueError, TypeError):
            return None
    
    def load_excel_to_dataframe(self, file_stream: BytesIO, sheet_name: str):
        df = pd.read_excel(file_stream, sheet_name=sheet_name)
        return df
    
    def load_header_row_header_table_key(self, service_name: str):
        row_header_table_key = self.config[service_name]["rowHeaderTableKey"]
        return row_header_table_key
        
    def parse_file(self, file_stream: BytesIO, service_name: str) -> list:
        # Reset stream ke awal
        file_stream.seek(0)
        
        sheet_name = self.find_sheet_name(file_stream, service_name)
        df = pd.read_excel(file_stream, sheet_name=sheet_name)

        header_row_index = self.find_table_header_row_index(df, service_name)
        table_header = self.find_table_header(df, service_name, header_row_index)

        df.columns = df.iloc[header_row_index]
        df = df[header_row_index + 1:]
        df = df.reset_index(drop=True)
        df = self.trim_dataframe(df, service_name)

        parsed_data = []
        for _, row in df.iterrows():
            row_data = {}
            for db_column, file_column in zip(self.config[service_name]["parshingFileSettings"].keys(), table_header):
                if file_column:
                    value = row[file_column] if file_column in df.columns else None
                    row_data[db_column] = self.convert_value_type(value, db_column, service_name)
                else:
                    row_data[db_column] = None
            
            parsed_data.append(row_data)
        
        return parsed_data




        
