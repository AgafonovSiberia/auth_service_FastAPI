
from typing import Optional, Union
from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserBase(BaseModel):
	full_name: Optional[str] = None
	login: Union[EmailStr, None] = None


class UserCreate(UserBase):
	login: Union[EmailStr, None]
	password: str


class UserFull(UserBase):
	is_active: Optional[bool] = False
	is_admin: Optional[bool] = False


class UserFromDB(UserFull):
	user_id: Optional[UUID] = None

	class Config:
		orm_mode = True

