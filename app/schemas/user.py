
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	full_name: Optional[str] = None
	email: Optional[EmailStr] = None


class UserCreate(UserBase):
	email: EmailStr
	password: str


class UserFull(UserBase):
	is_active: Optional[bool] = False
	is_admin: Optional[bool] = False


class UserFromDB(UserFull):
	id: Optional[int] = None

	class Config:
		orm_mode = True


class User(UserFromDB):
	pass



