from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import UserCreate, UserUpdate, UserResponse
from .models import User
from database import get_db
from typing import Annotated
from .service import create_user as create_user_scv, get_current_user, check_user_exists, authenticate_user, create_access_token, update_user as update_user_scv, change_password as change_password_srv
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel, Field

class PasswordRequest(BaseModel):
    old_password : str
    new_password : str


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/",status_code=status.HTTP_200_OK, response_model=UserResponse)
async def create_user(db : db_dependency, user_model : UserCreate):
    try:
        user = await create_user_scv(db, user_model)
        return user
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)  

@router.post("/token", status_code=status.HTTP_200_OK)
async def verify_user_model(db : db_dependency, request_form : Annotated[OAuth2PasswordRequestForm, Depends()]):
    await check_user_exists(db,request_form.username)
    user = await authenticate_user(db, request_form.username, request_form.password)
    token = await create_access_token(user.email, user.username, user.id, user.role)
    return token

@router.get("/me", response_model=UserResponse)
async def get_user(db : db_dependency, token : str):
    user = await get_current_user(token, db)
    return user

@router.put("/update", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(db : db_dependency, user_model : UserUpdate, token : str):
    user_db = await get_current_user(token, db)
    print(user_db.email)
    user = await update_user_scv(db, user_model, user_db.email)
    return user

@router.put("/change-password", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def change_password(db : db_dependency,  token : str, form_model : PasswordRequest):
    user_db = await get_current_user(token, db)
    user = await change_password_srv(db, form_model.old_password, form_model.new_password, user_db.email)
    return user
    