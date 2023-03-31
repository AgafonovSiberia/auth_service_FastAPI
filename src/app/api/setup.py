from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.api.depends.db import DBGateway
from app.api.api import api_router

from app.api.depends.db import get_repo


def setup(app: FastAPI, pool: async_sessionmaker[AsyncSession]):
    setup_routers(app)
    setup_dependency(app, pool)


def setup_routers(app: FastAPI):
    app.include_router(api_router)


def setup_dependency(app: FastAPI, pool: async_sessionmaker[AsyncSession]):
    app.dependency_overrides[get_repo] = DBGateway(pool=pool).repo
