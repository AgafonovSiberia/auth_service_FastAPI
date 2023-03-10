
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	name: Optional[str] = None
	email: Optional[EmailStr] = None


class UserCreate(UserBase):
	email: EmailStr
	password: str


class UserFull(BaseModel):
	is_active: Optional[bool] = False
	is_admin: Optional[bool] = False



