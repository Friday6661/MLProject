import json
from datetime import datetime, timedelta, timezone
from typing  import Optional, Union
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import httpx
from jwt import PyJWTError
import jwt
from helper.json_helper import JsonHelper
from passlib.context import CryptContext

from models.user_model import User

json_helper = JsonHelper()
config = json_helper.load_config('config.json', 'r')
jwt_settings = config["jwt_settings"]
ess_user = config["ess_user_configs"]

secret_key = jwt_settings['secret_key']
algorithm = jwt_settings['algorithm']
access_token_expire_minutes = jwt_settings['access_token_expire_minutes']

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class JWTAuthHelper:

    @staticmethod
    async def authenticate_user(email: str, password: str):
        url = ess_user["url"]
        device_id = ess_user["device_id"]
        payload = {
            "email": email,
            "password": password,
            "DeviceId": device_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data = payload)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Invalid ess user")
            
            user_response = response.json()
            return user_response
        
    @staticmethod
    def create_access_token(user_response: dict, expires_delta: Union[timedelta, None] = None):
        user_data = user_response["data"]
        to_encode = {
            "id": user_data["Id"],
            "email": user_data["Email"],
            "nrp": user_data["NRP"],
            "first_name": user_data["FirstName"],
            "middle_name": user_data["MiddleName"],
            "last_name": user_data["LastName"],
            "full_name": user_data["FullName"],
            "address": user_data["Address"],
            "phone": user_data["Phone"],
            "working_location_id": user_data["WorkingLocationId"],
            "role_id": user_data["RoleId"]
        }
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=1)
        to_encode.update({"exp": expire})
        encoded_jwt =jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            username: str = payload.get("nrp")
            if username is None:
                raise credentials_exception
            return payload
        except PyJWTError:
            raise credentials_exception
        
    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)):
        payload = JWTAuthHelper.verify_token(token)

        username: str = payload.get("nrp")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = User(
            username = payload.get("nrp"),
            email = payload.get("email"),
            full_name = payload.get("full_name"),
            disabled = payload.get("disabled", False)
        )

        if user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

