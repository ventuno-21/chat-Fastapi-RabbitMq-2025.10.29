from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=32)
    email: EmailStr
    password: constr(min_length=8, max_length=64)


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    is_admin: bool
    profile_image: Optional[str] = None
    created_at: datetime

    # class Config:
    #     orm_mode = True
