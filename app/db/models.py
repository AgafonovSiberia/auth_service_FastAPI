from sqlalchemy import Column, BigInteger, Text, DateTime, Integer, Boolean, LargeBinary
from sqlalchemy.sql import func
from app.schemas.user import UserCreate
from app.db.base import Base


class User(Base):
	__tablename__ = "users"

	id = Column(BigInteger, primary_key=True)
	full_name = Column(Text, index=True, default=None)
	email = Column(Text, index=True, nullable=False, unique=True)
	hashed_password = Column(LargeBinary, nullable=False)
	is_active = Column(Boolean, default=False)
	is_admin = Column(Boolean, default=False)

	def __init__(self, user_data: UserCreate):
		self.full_name = user_data.name
		self.email = user_data.email
		self.hashed_password = bytes(user_data.password, 'utf-8')



class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(BigInteger, primary_key=True)
    token = Column(Text, nullable=False)
    exp = Column(BigInteger, nullable=False)

