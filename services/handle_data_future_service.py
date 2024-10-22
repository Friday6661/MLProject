from functools import reduce
import joblib
import pandas as pd
from sqlalchemy.orm import Session
from models.dto.linear_regression_result_request import LinearRegressionResultRequest
from models.linear_regression_result_model import LinearRegressionResultModel
from repositories.forecast_monthly_coal_price_repository import ForecastMonthlyCoalPriceRepository
from repositories.forecast_monthly_working_hours_repository import ForecastMonthlyWorkingHoursRepository
from repositories.forecast_total_monthly_stocks_repository import ForecastTotalMonthlyStocksRepository
from services.forecasting_time_series_services import ForecastingTimeSeriesService
from repositories.linear_regression_result_repository import LinearRegressionResultRepository
from repositories.v_linear_regression_with_coef_repository import VLinearReegressionWithCoefRepository

class HandleDataFutureService:
    def __init__(self, db: Session):
        self.monthly_coal_price_repo = ForecastMonthlyCoalPriceRepository(db)
        self.monthly_working_hours_repo = ForecastMonthlyWorkingHoursRepository(db)
        self.total_monthly_stocks_repo = ForecastTotalMonthlyStocksRepository(db)
        self.linear_regression_result_repo = LinearRegressionResultRepository(db)
        self.v_linear_regression_result_with_coef_repo = VLinearReegressionWithCoefRepository(db)
        self.forecasting_service = ForecastingTimeSeriesService()

    def create_dataframe_future_monthly_coal_price(self):
        monthly_coal_price = self.monthly_coal_price_repo.get_all()
        monthly_coal_price_list = []
        for obj in monthly_coal_price:
            monthly_coal_price_dict = {
                "month": obj.month,
                "coal_price": obj.coal_price
            }
            monthly_coal_price_list.append(monthly_coal_price_dict)
        df_monthly_coal_price = self.forecasting_service.create_dataframe_from_list(monthly_coal_price_list, "month")
        return df_monthly_coal_price
    
    def create_dataframe_future_monthly_working_hours(self):
        monthly_working_hours = self.monthly_working_hours_repo.get_all()
        monthly_working_hours_list = []
        for obj in monthly_working_hours:
            monthly_working_hours_dict = {
                "month": obj.month,
                "total_monthly_working_hours": obj.total_monthly_working_hours
            }
            monthly_working_hours_list.append(monthly_working_hours_dict)
        df_monthly_working_hours = self.forecasting_service.create_dataframe_from_list(monthly_working_hours_list, "month")
        return df_monthly_working_hours
    
    def create_dataframe_future_total_monthly_stocks(self):
        monthly_stocks = self.total_monthly_stocks_repo.get_all()
        monthly_stocks_list = []
        for obj in monthly_stocks:
            monthly_stocks_dict = {
                "month": obj.month,
                "total_stocks": obj.total_stocks
            }
            monthly_stocks_list.append(monthly_stocks_dict)
        df_monthly_stocks = self.forecasting_service.create_dataframe_from_list(monthly_stocks_list, "month")
        return df_monthly_stocks
        
    
    def combine_all_dataframe(self) -> pd.DataFrame:
        df_monthly_coal_price = self.create_dataframe_future_monthly_coal_price()
        df_monthly_working_hours = self.create_dataframe_future_monthly_working_hours()
        df_monthly_monthly_stocks = self.create_dataframe_future_total_monthly_stocks()
        dataframes = [df_monthly_monthly_stocks, df_monthly_working_hours, df_monthly_coal_price]
        df = reduce(lambda left, right: pd.merge(left, right, on='month', how='outer'), dataframes)
        df.reset_index(inplace=True)
        df = df.sort_index()
        return df
    
    def load_model_linear_regression(self, version_name: str, model_file='_linear_regression_model.pkl'):
        model_file = version_name + model_file
        return joblib.load(model_file)
    
    def predict_using_linear_regression(self, df: pd.DataFrame, version_name: str) -> pd.DataFrame:
        model_lr = self.load_model_linear_regression(version_name)
        df['predicted_sales_' + version_name] = model_lr.predict(df).round().astype(int)
        return df
    
    def save_linear_regression_result_to_db(self, list_linear_regression_result_request: list[LinearRegressionResultRequest]):
        linear_regression_result_models = [
            LinearRegressionResultModel(
                month=request.month,
                total_stocks=request.total_stocks,
                total_monthly_working_hours=request.total_monthly_working_hours,
                coal_price=request.coal_price,
                year=request.year,
                predicted_sales_Recomendation=request.predicted_sales_Recomendation,
                predicted_sales_Mean=request.predicted_sales_Mean,
                predicted_sales_Median=request.predicted_sales_Median,
                predicted_sales_Mode=request.predicted_sales_Mode,
                predicted_sales_Min=request.predicted_sales_Min,
                predicted_sales_Max=request.predicted_sales_Max
            )
            for request in list_linear_regression_result_request
        ]
        return self.linear_regression_result_repo.bulk_create(linear_regression_result_models)
    
    def get_prediction_result_linear_regression(self):
        return self.linear_regression_result_repo.get_all()
    
    def get_predict_result_linear_regression_with_coef(self):
        return self.v_linear_regression_result_with_coef_repo.get_all()

    
