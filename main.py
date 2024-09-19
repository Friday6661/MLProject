from fastapi import FastAPI
from database import engine
from database import engine1
from models.coal_price_clean_model import CoalPriceClean
from models.coal_price_model import CoalPrice
from models.komtrax_clean_model import KomtraxClean
from models.komtrax_model import Komtrax
from models.monthly_sales_clean_model import MonthlySalesClean
from models.monthly_sales_model import MonthlySales
from models.monthly_stocks_clean_model import MonthlyStocksClean
from models.monthly_stocks_model import MonthlyStocks
from controllers import coal_price_controller, komtrax_controller, login_controller, monthly_sales_controller, monthly_stocks_controller, weekly_coal_price_controller
from models.weekly_coal_price_model import WeeklyCoalPrice

app = FastAPI()

CoalPrice.metadata.create_all(bind=engine)
Komtrax.metadata.create_all(bind=engine)
MonthlySales.metadata.create_all(bind=engine)
MonthlyStocks.metadata.create_all(bind=engine)
WeeklyCoalPrice.metadata.create_all(bind=engine)
CoalPriceClean.metadata.create_all(bind=engine1)
KomtraxClean.metadata.create_all(bind=engine1)
MonthlySalesClean.metadata.create_all(bind=engine1)
MonthlyStocksClean.metadata.create_all(bind=engine1)

app.include_router(komtrax_controller.router, prefix="/komtrax_controllers", tags=["Komtrax"])
app.include_router(coal_price_controller.router, prefix="/coal_price_controllers", tags=["Coal Price"])
app.include_router(monthly_sales_controller.router, prefix="/monthly_sales_controllers", tags=["Monthly Sales"])
app.include_router(monthly_stocks_controller.router, prefix="/monthly_stocks_controllers", tags=["Monthly Stocks"])
app.include_router(login_controller.router, prefix="/login_controllers", tags=["User Authentication"])
app.include_router(weekly_coal_price_controller.router, prefix="/weekly_coal_price_controllers", tags=["Weekly Coal Price"])


