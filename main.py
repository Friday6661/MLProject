from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text
from database import engine
from database import engine1
from database import engine2
from models.coal_price_clean_model import CoalPriceClean
from models.coal_price_model import CoalPrice
from models.coefisien_config_model import CoefisienConfigModel
from models.forecast_monthly_coal_price import ForecastMonthlyCoalPrice
from models.komtrax_clean_model import KomtraxClean
from models.komtrax_model import Komtrax
from models.monthly_coal_price_model import MonthlyCoalPrice
from models.monthly_sales_clean_model import MonthlySalesClean
from models.monthly_sales_model import MonthlySales
from models.monthly_stocks_clean_model import MonthlyStocksClean
from models.monthly_stocks_model import MonthlyStocks
from models.forecast_total_monthly_stocks_model import ForecastTotalMonthlyStocks
from models.linear_regression_result_model import LinearRegressionResultModel
from models.data_filling_model import DataFillingModel
from controllers import coal_price_controller, coefisien_config_controller, komtrax_controller, login_controller, monthly_coal_price_controller, monthly_sales_controller, monthly_stocks_controller, weekly_coal_price_controller, train_ml_model_controller, handle_data_prediction_controller, data_preprocessing_controller
from models.weekly_coal_price_model import WeeklyCoalPrice
from helper.json_helper import JsonHelper


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

json_helper = JsonHelper()

CoalPrice.metadata.create_all(bind=engine)
Komtrax.metadata.create_all(bind=engine)
MonthlySales.metadata.create_all(bind=engine)
MonthlyStocks.metadata.create_all(bind=engine)
WeeklyCoalPrice.metadata.create_all(bind=engine)
MonthlyCoalPrice.metadata.create_all(bind=engine)
CoalPriceClean.metadata.create_all(bind=engine1)
KomtraxClean.metadata.create_all(bind=engine1)
MonthlySalesClean.metadata.create_all(bind=engine1)
MonthlyStocksClean.metadata.create_all(bind=engine1)
ForecastTotalMonthlyStocks.metadata.create_all(bind=engine1)
DataFillingModel.metadata.create_all(bind=engine1)
ForecastMonthlyCoalPrice.metadata.create_all(bind=engine1)
LinearRegressionResultModel.metadata.create_all(bind=engine2)
CoefisienConfigModel.metadata.create_all(bind=engine2)

@app.on_event("startup")
async def startup_event():
    # Memuat query dari file JSON untuk engine pertama
    queries_engine_1 = json_helper.load_view_queries_from_json('sql_queries/views/view_queries_engine.json')
    with engine.connect() as connection:
        for view_name, query in queries_engine_1.items():
            connection.execute(text(query))
        connection.commit()

    # Memuat query dari file JSON untuk engine kedua
    queries_engine_2 = json_helper.load_view_queries_from_json('sql_queries/views/view_queries_engine_2.json')
    with engine2.connect() as connection:
        for view_name, query in queries_engine_2.items():
            connection.execute(text(query))
        connection.commit()
    

app.include_router(komtrax_controller.router, prefix="/komtrax_controllers", tags=["Komtrax"])
# app.include_router(coal_price_controller.router, prefix="/coal_price_controllers", tags=["Coal Price"])
app.include_router(monthly_sales_controller.router, prefix="/monthly_sales_controllers", tags=["Monthly Sales"])
app.include_router(monthly_stocks_controller.router, prefix="/monthly_stocks_controllers", tags=["Monthly Stocks"])
app.include_router(login_controller.router, prefix="/login_controllers", tags=["User Authentication"])
# app.include_router(weekly_coal_price_controller.router, prefix="/weekly_coal_price_controllers", tags=["Weekly Coal Price"])
app.include_router(monthly_coal_price_controller.router, prefix="/monthly_coal_price_controllers", tags=["Monthly Coal Price"])
app.include_router(train_ml_model_controller.router, prefix="/train_ml_model_controllers", tags=["Generate Machine Learning"])
app.include_router(handle_data_prediction_controller.router, prefix="/handle_data_prediction_controllers", tags=["Handle Data Prediction"])
app.include_router(coefisien_config_controller.router, prefix="/coefisien_config", tags=["Coefisien Config"])
app.include_router(data_preprocessing_controller.router, prefix="/data_preprocessing_result", tags=["Data Preprocessing Result"])