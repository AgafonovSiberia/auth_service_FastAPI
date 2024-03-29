from functools import lru_cache
from typing import Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repo.base.base import BaseSQLAlchemyRepo

T = TypeVar("T", bound=BaseSQLAlchemyRepo)


class SQLALchemyRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    @lru_cache()
    def get_repo(self, repo: Type[T]) -> T:
        return repo(self._session)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
