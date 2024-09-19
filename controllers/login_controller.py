from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import SessionLocal
from helper.jwt_helper import JWTAuthHelper
from models.dto.login_request import LoginRequest
from models.token_model import Token
from models.user_model import User

router = APIRouter()
def get_db_user():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db_user)]

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_response = await JWTAuthHelper.authenticate_user(form_data.username, form_data.password)
    if not user_response:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = JWTAuthHelper.create_access_token(user_response=user_response)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(JWTAuthHelper.get_current_user)):
    return current_user
