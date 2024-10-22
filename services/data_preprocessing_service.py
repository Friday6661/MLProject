import joblib
from sklearn.linear_model import LinearRegression
import pandas as pd
from functools import reduce
from sklearn.model_selection import GridSearchCV
from sqlalchemy.orm import Session
from repositories.v_monthly_sales_repository import VMonthlySalesRepository
from repositories.v_monthly_stocks_repository import VMonthlyStocksRepository
from repositories.v_monthly_working_hours_repository import VMonthlyWorkingHoursRepository
from repositories.monthly_coal_price_m38_repository import MonthlyCoalPriceM38Repository
from services.forecasting_time_series_services import ForecastingTimeSeriesService

class DataPreprocessingService:
    def __init__(self, db: Session):
        self.sales_repo = VMonthlySalesRepository(db)
        self.stocks_repo = VMonthlyStocksRepository(db)
        self.working_hours_repo = VMonthlyWorkingHoursRepository(db)
        self.coal_price_repo = MonthlyCoalPriceM38Repository(db)
        self.forecasting_service = ForecastingTimeSeriesService()

    def create_dataframe_sales(self) -> pd.DataFrame:
        monthly_sales = self.sales_repo.get_all()
        monthly_sales_list = []
        for obj in monthly_sales:
            monthly_sales_dict = {
                "month": obj.month,
                "total_sales": obj.total_sales
            }
            monthly_sales_list.append(monthly_sales_dict)

        df_monthly_sales = self.forecasting_service.create_dataframe_from_list(monthly_sales_list, "month")
        return df_monthly_sales
    
    def create_dataframe_stocks(self) -> pd.DataFrame:
        monthly_stocks = self.stocks_repo.get_all()
        monthly_stocks_list = []
        for obj in monthly_stocks:
            monthly_stocks_dict = {
                "month": obj.month,
                "total_stocks": obj.total_stocks
            }
            monthly_stocks_list.append(monthly_stocks_dict)
        df_monthly_stocks = self.forecasting_service.create_dataframe_from_list(monthly_stocks_list, "month")
        return df_monthly_stocks
    
    def create_dataframe_monthly_working_hours(self) -> pd.DataFrame:
        monthly_working_hours = self.working_hours_repo.get_all()
        monthly_working_hours_list = []
        for obj in monthly_working_hours:
            monthly_working_hours_dict = {
                "month": obj.month,
                "total_monthly_working_hours": obj.total_monthly_working_hours
            }
            monthly_working_hours_list.append(monthly_working_hours_dict)
        df_monthly_working_hours = self.forecasting_service.create_dataframe_from_list(monthly_working_hours_list, "month")
        return df_monthly_working_hours

    def create_dataframe_monthly_coal_price(self) -> pd.DataFrame:
        monthly_coal_price = self.coal_price_repo.get_all()
        monthly_coal_price_list = []
        for obj in monthly_coal_price:
            monthly_coal_price_dict = {
                "month": obj.date,
                "coal_price": obj.coal_price
            }
            monthly_coal_price_list.append(monthly_coal_price_dict)
        df_monthly_coal_price = self.forecasting_service.create_dataframe_from_list(monthly_coal_price_list, "month")
        return df_monthly_coal_price
    
    def combine_all_dataframe(self) -> pd.DataFrame:
        df_monthly_sales = self.create_dataframe_sales()
        df_monthly_stocks = self.create_dataframe_stocks()
        df_monthly_working_hours = self.create_dataframe_monthly_working_hours()
        df_monthly_coal_price = self.create_dataframe_monthly_coal_price()
        dataframes = [df_monthly_sales, df_monthly_stocks, df_monthly_working_hours, df_monthly_coal_price]
        df = reduce(lambda left, right: pd.merge(left, right, on='month', how='outer'), dataframes)
        df.reset_index(inplace=True)
        df = df.sort_index()
        return df
    
    def create_dataframe_predictor_target(self, df: pd.DataFrame):
        target_columns = [col for col in df.columns if '_sales' in col]

        if len(target_columns) == 0:
            raise ValueError("Cannot find columns target")
        elif len(target_columns) > 1:
            # ambil yang indexnya paling besar
            column_target_name = target_columns[-1]
        else:
            column_target_name = target_columns[0]
        
        X = df.drop(columns=[column_target_name])
        y = df[column_target_name]

        return X, y
    
    def train_test_split(self, X: pd.DataFrame, y: pd.Series, test_size=12):
        if len(X) != len(y):
            raise ValueError("Target and predictor data must have the same length")
        
        if test_size >= len(X):
            raise ValueError("Test size must be smaller than the number of samples")

        X_train = X[:-12]
        y_train = y[:-12]
        X_test = X[-12:]
        y_test  = y[-12:]
    
        return X_train, y_train, X_test, y_test
    
    def linear_regresion_parameter_tunning(self, X_train: pd.DataFrame, y_train: pd.Series,
                                           X_test: pd.DataFrame, y_test: pd.Series, version_name: str, 
                                           model_file='_linear_regression_model.pkl'):
        model_lr = LinearRegression()
        param_grid = {'fit_intercept': [True, False]}
        model_file = version_name + model_file

        grid_search = GridSearchCV(model_lr, param_grid, cv=5)
        print(type(X_train))
        print(type(y_train))
        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_
        joblib.dump(best_model, model_file)

        test_score = best_model.score(X_test, y_test)
        best_params = grid_search.best_params_

        return best_model, test_score, best_params

            