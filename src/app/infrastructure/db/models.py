from sqlalchemy import Column, BigInteger, Text, Float, Integer, Boolean, LargeBinary
from app.infrastructure.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(Base):
	__tablename__ = "users"

	user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	full_name = Column(Text, index=True, default=None)
	login = Column(Text, index=True, nullable=False, unique=True)
	hashed_password = Column(LargeBinary, nullable=False)
	is_active = Column(Boolean, default=False)
	is_admin = Column(Boolean, default=False)

	@property
	def user_is_admin(self) -> bool:
		return User.is_admin


class ActivateCode(Base):
	__tablename__ = "activate_codes"

	id = Column(Integer, primary_key=True)
	user_id = Column(UUID(as_uuid=True), nullable=False)
	code = Column(Text, nullable=False)
	expire = Column(Float, nullable=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(BigInteger, primary_key=True)
    token = Column(Text, nullable=False)
    exp = Column(Float, nullable=False)

