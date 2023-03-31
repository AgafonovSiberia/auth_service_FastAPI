from typing import AsyncGenerator
from typing import Generator
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import close_all_sessions
import asyncio
import os
from testcontainers.postgres import PostgresContainer
from app.api.setup import setup
from app.infrastructure.repo.base import SQLALchemyRepo


from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import sessionmaker
from app.config_reader import config

from alembic.config import Config
from alembic.command import upgrade


pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer("postgres:15.1", password="civiclaeu3")
    if os.name == "nt":
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        yield postgres_url_
    finally:
        postgres.stop()


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> Config:
    print(postgres_url)
    alembic_cfg = Config("./alembic.ini")
    alembic_cfg.set_main_option("script_location", "./migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(alembic_config: Config):
    upgrade(alembic_config, "head")


@pytest.fixture(scope="session")
def async_pool() -> Generator[sessionmaker, None, None]:
    engine = create_async_engine(url=config.POSTGRES_URL)
    pool_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    yield pool_
    close_all_sessions()


@pytest_asyncio.fixture(scope="session")
async def session(async_pool: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_pool() as _session:
        yield _session
        _session.rollback()

    _session.close()


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
