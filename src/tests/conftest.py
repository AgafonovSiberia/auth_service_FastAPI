from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
import asyncio
from app.api.schemas.user import UserFromDB, UserCreate
from app.infrastructure.repo.user_repo import UserRepo
import os
from app.utils.security import crypt_password
from app.api.setup import setup
from app.infrastructure.repo.base import SQLALchemyRepo

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from uuid import UUID

DB_TEST_URL = "postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(DB_TEST_URL, pool_pre_ping=True, echo=True)
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )

    yield pool


@pytest.fixture(scope="session")
async def get_test_repo():
    engine = create_async_engine(DB_TEST_URL, pool_pre_ping=True, echo=True)
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )
    async with pool() as _session:
        yield SQLALchemyRepo(_session)


@pytest.fixture(scope="session")
def test_app(pool: async_sessionmaker[AsyncSession]) -> FastAPI:
    app = FastAPI
    setup(app=app, pool=pool)
    return app



@pytest.mark.anyio
@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
async def get_user_from_database(get_test_repo):
    async def get_user_from_database_by_uuid(user_id: UUID):
        user: UserFromDB = await get_test_repo.get_repo(UserRepo).get_user_by_id()
        return user

    return get_user_from_database_by_uuid()


@pytest.fixture
async def create_user_in_database(get_test_repo):
    async def create_user_in_database(
        full_name: str,
        login: str,
        password: str,
    ):
        user: UserFromDB = await get_test_repo.get_repo(UserRepo).add_user(
            UserCreate(full_name=full_name, login=login, password=crypt_password(password))
        )

    return create_user_in_database

