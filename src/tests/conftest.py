from typing import AsyncGenerator
from typing import Generator
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import close_all_sessions
import asyncio

from app.api.setup import setup
from app.infrastructure.repo.base import SQLALchemyRepo

pytest_plugins = ('pytest_asyncio',)

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import sessionmaker
from uuid import UUID
from app.config_reader import config

DB_TEST_URL = "postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


#
# @pytest.fixture(scope="session", autouse=True)
# async def run_migrations():
#     os.system("alembic init migrations")
#     os.system('alembic revision --autogenerate -m "test running migrations"')
#     os.system("alembic upgrade heads")


@pytest_asyncio.fixture
async def session(async_pool: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_pool() as session_:
        yield session_


@pytest.fixture(scope="session")
def async_pool() -> Generator[sessionmaker, None, None]:
    engine = create_async_engine(url=config.POSTGRES_URL)
    pool_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    yield pool_
    close_all_sessions()


@pytest_asyncio.fixture(scope="session")
async def repo(async_pool: Generator[sessionmaker, None, None]) -> SQLALchemyRepo:
    async with async_pool() as _session:
        yield SQLALchemyRepo(_session)


@pytest.fixture(scope="session")
def test_app(async_pool: async_sessionmaker[AsyncSession]) -> FastAPI:
    app = FastAPI()
    setup(app=app, pool=async_pool)
    return app


@pytest.mark.asyncio
@pytest_asyncio.fixture(scope="session")
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=test_app, base_url="http://test") as test_client:
        yield test_client
