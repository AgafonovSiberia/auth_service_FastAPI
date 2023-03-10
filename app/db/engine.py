
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.config_reader import config


def get_session_factory():
	"""
	Create SQLAlchemy async engine
	:return: sqlalchemy.ext.asyncio.AsyncSession
	"""
	engine = create_async_engine(config.POSTGRES_URL, pool_pre_ping=True, echo=True)
	return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
