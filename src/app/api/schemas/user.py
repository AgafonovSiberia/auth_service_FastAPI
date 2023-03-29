
from typing import Optional, Union
from pydantic import BaseModel, EmailStr
from app.api.schemas.validator import PhoneNumber
from uuid import UUID


class UserBase(BaseModel):
	full_name: Optional[str] = None
	login: Union[EmailStr, PhoneNumber, None] = None


class UserCreate(UserBase):
	login: Union[EmailStr, PhoneNumber, None]
	password: str


class UserFull(UserBase):
	is_active: Optional[bool] = False
	is_admin: Optional[bool] = False


class UserFromDB(UserFull):
	user_id: Optional[UUID] = None

	class Config:
		orm_mode = True

