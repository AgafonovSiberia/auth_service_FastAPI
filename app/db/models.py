from sqlalchemy import Column, BigInteger, Text, DateTime, Integer, Boolean, LargeBinary
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
	__tablename__ = "users"

	id = Column(BigInteger, primary_key=True)
	full_name = Column(Text, index=True)
	email = Column(Text, index=True, nullable=False, unique=True)
	hashed_password = Column(LargeBinary, nullable=False)
	is_active = Column(Boolean, default=False)
	is_admin = Column(Boolean, default=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(BigInteger, primary_key=True)
    token = Column(Text, nullable=False)
    exp = Column(BigInteger, nullable=False)

