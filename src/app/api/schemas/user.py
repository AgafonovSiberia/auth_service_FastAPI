from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    full_name: Optional[str] = None
    login: EmailStr = None


class UserCreate(UserBase):
    login: EmailStr
    password: str = Field(min_length=8)


class UserFull(UserBase):
    is_active: Optional[bool] = False
    is_admin: Optional[bool] = False


class UserFromDB(UserFull):
    user_id: Optional[UUID] = None

    class Config:
        orm_mode = True
