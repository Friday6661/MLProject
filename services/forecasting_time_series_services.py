from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from difflib import SequenceMatcher
from io import BytesIO
import io
import json
import pandas as pd
from sqlalchemy.orm import Session
import xlsxwriter
from statsmodels.tsa.statespace.sarimax import SARIMAX

class ForecastingTimeSeriesService:
    def __init__(self):
        pass

    def create_dataframe_from_json(self, json_data: str, index_column: str) -> pd.DataFrame:
        df = pd.read_json(json_data)
        df.rename(columns={index_column: 'month'}, inplace=True)
        df.set_index('month', inplace=True)
        df = df.sort_index().asfreq('MS')
        return df
    
    def run_sarimax_model(self, y: pd.Series, order=(1,1,1), seasonal_order=(1,1,1,12), steps=24) -> pd.Series:
        model = SARIMAX(y, order=order, seasonal_order=seasonal_order)
        results = model.fit(disp=False)
        prediction = results.get_forecast(steps=steps)
        return prediction.predicted_mean
    
    def create_dataframe_from_list(self, list_data: list, index_column: str) -> pd.DataFrame:
        df = pd.DataFrame(list_data)
        df.rename(columns={index_column: 'month'}, inplace=True)
        df['month'] = pd.to_datetime(df['month'], format='%Y-%m')
        df.set_index('month', inplace=True)
        df = df.sort_index().asfreq('MS')
        return df
    
    def change_index_to_column(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.reset_index(inplace=True)
        return df



