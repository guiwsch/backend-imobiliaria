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


class UserProfile(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


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
