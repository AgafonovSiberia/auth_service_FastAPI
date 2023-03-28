from sqlalchemy import Column, BigInteger, Text, Float, Integer, Boolean, LargeBinary
from app.infrastructure.db.base import Base


class User(Base):
	__tablename__ = "users"

	id = Column(BigInteger, primary_key=True)
	full_name = Column(Text, index=True, default=None)
	login = Column(Text, index=True, nullable=False, unique=True)
	hashed_password = Column(LargeBinary, nullable=False)
	is_active = Column(Boolean, default=False)
	is_admin = Column(Boolean, default=False)


class ActivateCode(Base):
	__tablename__ = "activate_codes"
	id = Column(Integer, primary_key=True)
	user_id = Column(BigInteger, nullable=False)
	code = Column(Integer, nullable=False)
	expire = Column(Float, nullable=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(BigInteger, primary_key=True)
    token = Column(Text, nullable=False)
    exp = Column(Float, nullable=False)

