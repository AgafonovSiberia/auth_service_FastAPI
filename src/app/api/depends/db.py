from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.infrastructure.repo.base import SQLALchemyRepo


def get_repo() -> SQLALchemyRepo:
    NotImplementedError


class DBGateway:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def repo(self) -> SQLALchemyRepo:
        async with self.pool() as session:
            yield SQLALchemyRepo(session)
