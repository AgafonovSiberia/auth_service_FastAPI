import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic.command import upgrade
from alembic.config import Config
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import close_all_sessions, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.api.setup import setup
from app.config_reader import config
from app.infrastructure.repo.base import SQLALchemyRepo

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer("postgres:15.1")

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
    alembic_cfg = Config("./alembic.ini")
    alembic_cfg.set_main_option("script_location", "./migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    config.POSTGRES_URL = postgres_url
    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(alembic_config: Config):
    upgrade(alembic_config, "head")


@pytest.fixture(scope="session")
def async_pool(postgres_url: str) -> Generator[sessionmaker, None, None]:
    engine = create_async_engine(url=postgres_url)
    pool_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    yield pool_
    close_all_sessions()


@pytest_asyncio.fixture(scope="session")
async def session(async_pool: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_pool() as _session:
        yield _session
        await _session.rollback()
        _session.close


@pytest_asyncio.fixture(scope="session")
async def repo(session: AsyncGenerator[AsyncSession, None]) -> SQLALchemyRepo:
    yield SQLALchemyRepo(session)


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
