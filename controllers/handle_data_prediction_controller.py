from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from starlette import status
from sqlalchemy.orm import Session

from database import SessionLocal1
from database import SessionLocal2
from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from services.handle_data_future_service import HandleDataFutureService
from models.dto.linear_regression_result_request import LinearRegressionResultRequest


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_controllers/token")
def get_db_clean():
    db = SessionLocal1()
    try:
        yield db
    finally:
        db.close()

def get_db_warehouse():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-prediction-linear-regression/", status_code=status.HTTP_201_CREATED)
async def save_data_prediction_linear_regresion(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_clean), db1: Session = Depends(get_db_warehouse)):
    # Memvalidasi token pengguna
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())

    # Menggabungkan seluruh dataframe dan memproses data
    handle_data_future_service = HandleDataFutureService(db)
    handle_data_future_service1 = HandleDataFutureService(db1)

    # Menggabungkan semua data frame
    df = handle_data_future_service.combine_all_dataframe()
    df['month'] = pd.to_datetime(df['month'])
    df['year'] = df['month'].dt.year
    df['month'] = df["month"].dt.month

    # Memproses kolom yang berisi nilai NaN
    # df = filling_missing_value_service.change_cols_indicates_nan(df)
    # columns_with_nan = filling_missing_value_service.check_column_contain_isna(df)

    df = df.dropna()

    df_versions = {
        "Recomendation": df.copy(),
        "Mean": df.copy(),
        "Median": df.copy(),
        "Mode": df.copy(),
        "Min": df.copy(),
        "Max": df.copy()
    }

    for version_name, df_version in df_versions.items():
        df_version_predict = handle_data_future_service.predict_using_linear_regression(df_version, version_name)
        df['predicted_sales_' + version_name] = df_version_predict['predicted_sales_' + version_name]
    
    df = df.dropna()
    list_linear_regression_result_request = [
        LinearRegressionResultRequest(
            month=row['month'],
            total_stocks=row['total_stocks'],
            total_monthly_working_hours=row['total_monthly_working_hours'],
            coal_price=row['coal_price'],
            year=row['year'],
            predicted_sales_Recomendation=row['predicted_sales_Recomendation'],
            predicted_sales_Mean=row['predicted_sales_Mean'],
            predicted_sales_Median=row['predicted_sales_Median'],
            predicted_sales_Mode=row['predicted_sales_Mode'],
            predicted_sales_Min=row['predicted_sales_Min'],
            predicted_sales_Max=row['predicted_sales_Max']
        )
        for index, row in df.iterrows()
    ]

    response_save = handle_data_future_service1.save_linear_regression_result_to_db(list_linear_regression_result_request)
    if response_save is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessageHelper.error_message_create())
    response = {"message": ResponseMessageHelper.success_message_create()}
    return response

@router.get("/get-result-prediction-linear-regression/", status_code=status.HTTP_200_OK)
async def get_result_prediction_linear_regression(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_clean)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    handle_data_future_service = HandleDataFutureService(db)
    service_response = handle_data_future_service.get_prediction_result_linear_regression()
    if service_response is None:
        return []
    return service_response

@router.get("/get-prediction-result-lr-with-coef/", status_code=status.HTTP_200_OK)
async def get_result_prediction_linear_regression_with_coef(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_warehouse)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())
    
    handle_data_future_service = HandleDataFutureService(db)
    service_response = handle_data_future_service.get_predict_result_linear_regression_with_coef()
    if service_response is None:
        return []
    return service_response