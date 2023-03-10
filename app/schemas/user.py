
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	full_name: Optional[str] = None
	email: Optional[EmailStr] = None
	is_active: Optional[bool] = False
	is_admin: bool = False


class UserCreate(UserBase):
	email: EmailStr
	password: str
