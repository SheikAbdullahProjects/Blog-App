from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from .enums import Role
from typing import Optional


class User(BaseModel):
    email : EmailStr
    username : str = Field(min_length=5)
    role : Role
    
class UserCreate(User):
    password : str = Field(min_length=8)
    
class UserUpdate(BaseModel):
    email : EmailStr  = None
    username : Optional[str] =  Field(min_length=5, default=None)
    
class UserResponse(User):
    id : int
    role : Role
    created_at : datetime
    updated_at : datetime
    
    
    model_config = ConfigDict(from_attributes=True)