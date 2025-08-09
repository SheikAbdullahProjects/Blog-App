
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from .schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from .models import User
from starlette import status
from typing import Annotated
from pydantic import EmailStr


SECRET_KEY = "283d81fc37e41909f8952e591a48603efdcca1d421dd1c0bb799f854449cbae8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def check_user_exists(db : Session, email : str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
async def check_user_exists_for_create(db : Session, email : str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    return user
    
async def create_access_token(email : EmailStr, username : str, id : int, role : str):
    encode = {
        "sub" : email,
        "username" : username,
        "id" : id,
        "role" : role
    }
    expires = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp" : expires})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token" : token,
        "token_type" : "bearer"
    }
    
    
async def get_current_user(token : Annotated[str, Depends(auth2_bearer)], db : Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : EmailStr = payload.get("sub")
        username : str = payload.get("username")
        id : int = payload.get("id")
        role : str = payload.get("role")
        if not email or not username or not id or not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Error {e}")

async def authenticate_user(db : Session, username : str, password : str):
    user = await check_user_exists(db, username)
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

async def create_user(db : Session, model_user : UserCreate):
    user = await check_user_exists_for_create(db, model_user.email)
    print(user)
    user = User(hashed_password = bcrypt_context.hash(model_user.password), **model_user.model_dump(exclude={"password"}))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def update_user(db : Session, form_model : UserUpdate, email: str):
    user = await check_user_exists(db, email)
    user.email = form_model.email
    user.username = form_model.username
    user.role = form_model.role
    db.commit()
    db.refresh(user)
    return user

async def change_password(db : Session, old_password: str, new_password: str, email : str):
    user = await authenticate_user(db, email, old_password)
    user.hashed_password = bcrypt_context.hash(new_password)
    db.commit()
    db.refresh(user)
    return user
    
