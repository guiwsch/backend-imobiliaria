from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access: str
    refresh: str


class TokenRefresh(BaseModel):
    refresh: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
