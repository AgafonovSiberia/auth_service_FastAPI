from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config_reader import config


def create_pool() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(config.POSTGRES_URL, pool_pre_ping=True, echo=True)
    return create_session_maker(engine)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    return pool
