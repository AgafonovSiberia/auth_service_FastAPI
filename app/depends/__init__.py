from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.depends.db import DBGateway
from app.api.api import api_router
from app.depends.db import get_repo


def setup(app: FastAPI, pool: async_sessionmaker[AsyncSession]):
    app.dependency_overrides[get_repo] = DBGateway(pool=pool).repo
    app.include_router(api_router)
