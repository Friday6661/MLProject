from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

import scipy.stats as stats
import numpy as np
import pandas as pd
from models.dto.data_filling_request import DataFillingRequest
from repositories.data_filling_repositories import DataFillingRepository
from models.data_filling_model import DataFillingModel
from helper.enum_helper import MLModelsEnum, FillingMethodEnum

class FillingMissingValue:
    def __init__(self, db: Session):
        self.data_filling_repo = DataFillingRepository(db)

    def change_cols_indicates_nan(self, df: pd.DataFrame):
        df_columns = df.columns
        for column_name in df_columns:
            df[column_name] = df[column_name].replace([-1.0, '-', 0, '', ' '], np.nan)
        return df
    
    def check_count_nan_in_column(self, df: pd.DataFrame) -> pd.Series:
        count_nan = df.isna().sum()
        return count_nan
    
    def check_column_contain_isna(self, df: pd.DataFrame):
        columns_with_nan = df.columns[df.isna().any()].tolist()
        return columns_with_nan

    def check_mean_imputation_suitability(self, df: pd.DataFrame, column_name: str):
        # 1. mengecheck apakah kolom numerik
        if not pd.api.types.is_numeric_dtype(df[column_name]):
            return False
        
        # 2. menghilangkan nan untuk check outliers
        col_without_nan = df[column_name].dropna()

        # 3. mengecheck distribusi normal menggunakan D'Agostino's K-Squared Test
        stat, p_value = stats.normaltest(col_without_nan)
        if p_value < 0.05:
            return False
        
        # 4. mengecheck apakah ada outlier yang signifika menggunakan metode IQR
        threshold_outliers = 1.5
        Q1 = col_without_nan.quantile(0.25)
        Q3 = col_without_nan.quantile(0.75)
        IQR = Q3 - Q1

        # outlier threshold
        lower_bound = Q1 - threshold_outliers * IQR
        upper_bound = Q3 + threshold_outliers * IQR

        outliers = col_without_nan[(col_without_nan < lower_bound) | (col_without_nan > upper_bound)]
        if not outliers.empty:
            return False
        
        return True

    def check_median_imputation_suitability(self, df: pd.DataFrame, column_name: str):
        # 1. mengecheck apakah kolom numeric
        if not pd.api.types.is_numeric_dtype(df[column_name]):
            return False
        
        # 2. menghilangkan nan untuk check outliers
        col_without_nan = df[column_name].dropna()

        # 3. mengecheck distribusi normal menggunakan D'Agostino's K-squared Test
        stat, p_value = stats.normaltest(col_without_nan)
        if p_value < 0.05:
            return True
        
        # 4. mengecheck apakah ada outlier yang signifikan menggunakan metode IQR
        threshold_outliers = 1.5
        Q1 = col_without_nan.quantile(0.25)
        Q3 = col_without_nan.quantile(0.75)
        IQR = Q3 - Q1

        # Outlier thresshold
        lower_bound = Q1 - threshold_outliers * IQR
        upper_bound = Q3 + threshold_outliers * IQR

        outliers = col_without_nan[(col_without_nan < lower_bound) | ( col_without_nan > upper_bound)]
        if not outliers.empty:
            return True
        return False

    def check_most_frequent_imputation_suitability(self, df: pd.DataFrame, column_name: str):
        # 1. mengecheck apakah kolom numerik atau kategorikal
        if not pd.api.types.is_object_dtype(df[column_name]) and not pd.api.types.is_numeric_dtype(df[column_name]):
            return False
        
        # 2. menghitung frekuensi missing value
        threshold_missing=0.2
        missing_ratio = df[column_name].isnull().mean()
        if missing_ratio > threshold_missing:
            return True
        
        # 3. menghitung frekuensi nilai
        value_counts = df[column_name].value_counts(normalize=True)
        most_frequent = value_counts.idxmax()
        most_frequent_count = value_counts.max()

        # 4. check apakah frekuensi nilai yang paling sering muncul cukup tinggi
        if most_frequent_count > 0.5:
            return True
        
        return False

    def check_most_fill_constant_suitability(self, df: pd.DataFrame, column_name: str):
        # Hitung jumlah nan dalam kolom
        count_nan = df[column_name].isna().sum()
        total_rows = len(df)

        #proporsi nilai nan dalam kolom
        nan_ratio = count_nan / total_rows

        # Kriteria penggunaan konstanta:
        # 1. Jika kolom memiliki proporsi nan yang kecil kurang dari 5 %
        # 2. Jika kolom berisi data kategorikal atau numeric dengan nilai ordinal

        if nan_ratio > 0 and nan_ratio <= 0.05:
            # check kolom berisi nilai numerik dengan nilai ordinal atau data kategorikal
            if pd.api.types.is_numeric_dtype(df[column_name]):
                if df[column_name].min() == -1 or df[column_name].min() == 0:
                    return True
            elif pd.api.types.is_string_dtype(df[column_name]):
                if "Unknown" in df[column_name].unique():
                    return True
            return False
    
    def handling_missing_value_recomendation(self, df: pd.DataFrame, columns_with_nan: list):
        for column in columns_with_nan:
            if self.check_mean_imputation_suitability(df, column):
                df = self.fill_column_with_mean(df, column)
            elif self.check_median_imputation_suitability(df, column):
                df = self.fill_column_with_median(df, column)
            elif self.check_most_frequent_imputation_suitability(df, column):
                df = self.fill_column_with_mode(df, column)
            elif self.check_most_fill_constant_suitability(df, column):
                df = self.fill_column_with_unknown(df, column)
            else:
                df = self.fill_column_with_min(df, column)
        return df
    
    def handling_missing_value_using_mean(self, df: pd.DataFrame, columns_with_nan: list):
        for column in columns_with_nan:
            df = self.fill_column_with_mean(df, column)
        return df
    
    def handling_missing_value_using_median(self, df: pd.DataFrame, columns_with_nan: list):
        for column in columns_with_nan:
            df = self.fill_column_with_median(df, column)
        return df
    
    def handling_missing_value_using_mode(self, df: pd.DataFrame, columns_with_nan: list):
        for column in columns_with_nan:
            df = self.fill_column_with_mode(df, column)
        return df

    def handling_missing_value_using_min_value(self, df: pd.DataFrame, columns_with_nan: list):
        for column in columns_with_nan:
            df = self.fill_column_with_min(df, column)
        return df
    
    def handling_missing_value_using_max_value(self, df: pd.DataFrame, columns_with_nan: list):
        for column in columns_with_nan:
            df = self.fill_column_with_max(df, column)
        return df

    def fill_column_with_mode(self, df: pd.DataFrame, column_name: str):
        mode_value = df[column_name].mean()
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna(mode_value, inplace=True)
        return df

    def fill_column_with_mean(self, df: pd.DataFrame, column_name: str):
        mean_value = df[column_name].mean()
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna(mean_value, inplace=True)
        return df
    
    def fill_column_with_median(self, df: pd.DataFrame, column_name: str):
        median_value = df[column_name].median()
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna(median_value, inplace=True)
        return df

    def fill_column_with_unknown(self, df: pd.DataFrame, column_name: str):
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna("Unknown", inplace=True)
        return df
    
    def fill_column_with_min(self, df: pd.DataFrame, column_name: str):
        min_value = df[column_name].min()
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna(min_value, inplace=True)
        return df

    def fill_column_with_max(self, df: pd.DataFrame, column_name: str):
        max_value = df[column_name].max()
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna(max_value, inplace=True)
        return df
    
    def save_df_filling_into_db(self, df: pd.DataFrame, ml_model, filling_method):
        request_list = []
        for _, row in df.iterrows():
            request_model = DataFillingRequest(
                ml_models=MLModelsEnum(ml_model),  # Inisialisasi enum berdasarkan nilai
                filling_method=FillingMethodEnum(filling_method), 
                month=int(row.get('month')) if not pd.isnull(row.get('month')) else None,
                total_sales=int(row.get('total_sales')) if not pd.isnull(row.get('total_sales')) else None,
                total_stocks=int(row.get('total_stocks')) if not pd.isnull(row.get('total_stocks')) else None,
                total_monthly_working_hours=row.get('total_monthly_working_hours'),
                coal_price=row.get('coal_price'),
                year=int(row.get('year')) if not pd.isnull(row.get('year')) else None
            )
            
            request_list.append(request_model)
        
        model_list = []
        for request in request_list:
            model_instance = DataFillingModel(
                ml_model=request.ml_models,
                filling_method=request.filling_method,
                month=request.month,
                total_stocks=request.total_stocks,
                total_sales =request.total_sales,
                total_monthly_working_hours=request.total_monthly_working_hours,
                coal_price=request.coal_price,
                year=request.year
            )
            model_list.append(model_instance)

        created_data_filling_response = self.data_filling_repo.bulk_create(model_list)
        return created_data_filling_response
    
    def get_all_data_filling(self):
        response = self.data_filling_repo.get_all()
        return response
    
    def get_all_data_by_ml_model(self, ml_model: MLModelsEnum):
        response = self.data_filling_repo.get_by_ml_model(ml_model)
        return response
    
    def get_all_data_by_filling_method(self, filling_method: FillingMethodEnum):
        response = self.data_filling_repo.get_by_filling_method(filling_method)
        return response
    
    def get_all_data_by_filling_method_and_ml_model(self, filling_method: FillingMethodEnum, ml_model: MLModelsEnum):
        response = self.data_filling_repo.get_by_filling_method_and_ml_model(filling_method, ml_model)
        return response

    
