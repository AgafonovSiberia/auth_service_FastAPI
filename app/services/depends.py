from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import get_session_factory
from app.repo.base import Repository


async def get_repo() -> Generator[Repository, None, None]:
	"""
	Create SQLAlchemyRepo
	:return: SQLAlchemyRepo
	"""
	_session: AsyncSession = get_session_factory()()
	try:
		repo: Repository = Repository(_session)
		yield repo
	finally:
		await _session.close()

