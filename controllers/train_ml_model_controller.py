from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from starlette import status
from sqlalchemy.orm import Session

from database import SessionLocal, SessionLocal1
from helper.jwt_helper import JWTAuthHelper
from helper.response_message_helper import ResponseMessageHelper
from services.filling_missing_value_services import FillingMissingValue
from services.data_preprocessing_service import DataPreprocessingService
from helper.enum_helper import MLModelsEnum, FillingMethodEnum


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_controllers/token")
def get_db_raw():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_db_clean():
    db = SessionLocal1()
    try:
        yield db
    finally:
        db.close()

@router.post("/linear-regression-model/", status_code=status.HTTP_200_OK)
async def create_linear_regression_model(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_raw), db1: Session = Depends(get_db_clean)):
    current_user = JWTAuthHelper.get_current_user(token)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessageHelper.error_message_jwt_authentication())

    preprocessing_service = DataPreprocessingService(db)
    filling_missing_value_service = FillingMissingValue(db1)

    # Menggabungkan semua dataframe dan melakukan preprocessing
    df = preprocessing_service.combine_all_dataframe()
    df['month'] = pd.to_datetime(df['month'])
    df['year'] = df['month'].dt.year
    df['month'] = df["month"].dt.month
    df = filling_missing_value_service.change_cols_indicates_nan(df)
    columns_with_nan = filling_missing_value_service.check_column_contain_isna(df)

    # Mengisi missing value menggunakan berbagai metode
    df_versions = {
        "Recomendation": filling_missing_value_service.handling_missing_value_recomendation(df.copy(), columns_with_nan),
        "Mean": filling_missing_value_service.handling_missing_value_using_mean(df.copy(), columns_with_nan),
        "Median": filling_missing_value_service.handling_missing_value_using_median(df.copy(), columns_with_nan),
        "Mode": filling_missing_value_service.handling_missing_value_using_mode(df.copy(), columns_with_nan),
        "Min": filling_missing_value_service.handling_missing_value_using_min_value(df.copy(), columns_with_nan),
        "Max": filling_missing_value_service.handling_missing_value_using_max_value(df.copy(), columns_with_nan)
    }

    #save df_versions into db
    ml_model = MLModelsEnum.LINEAR_REGRESSION.value
    filling_responses = []
    for version_name, df_version in df_versions.items():
        if version_name == "Recomendation":
            filling_method = FillingMethodEnum.RECOMENDATION.value
        elif version_name == "Mean":
            filling_method = FillingMethodEnum.MEAN.value
        elif version_name == "Median":
            filling_method = FillingMethodEnum.MEDIAN.value
        elif version_name == "Mode":
            filling_method = FillingMethodEnum.MODE.value
        elif version_name == "Min":
            filling_method = FillingMethodEnum.MIN.value
        elif version_name == "Max":
            filling_method = FillingMethodEnum.MAX.value

        filling_response = filling_missing_value_service.save_df_filling_into_db(df_version, ml_model, filling_method)
        filling_responses.append(filling_response)

    # Untuk menyimpan hasil
    results = {}

    # Melatih model untuk setiap versi dataframe yang dihasilkan
    for version_name, df_version in df_versions.items():
        # Pisahkan fitur (X) dan target (y)
        X, y = preprocessing_service.create_dataframe_predictor_target(df_version)
        X_train, y_train, X_test, y_test = preprocessing_service.train_test_split(X, y)

        # Latih model dengan tuning parameter
        best_model, test_score, best_params = preprocessing_service.linear_regresion_parameter_tunning(X_train, y_train, X_test, y_test, version_name)

        # Simpan hasil untuk versi dataframe ini
        results[version_name] = {
            "Test Score": test_score,
            "Best Params": best_params
        }

    # Mengembalikan hasil dari semua versi model
    return {"Training Results": results}
