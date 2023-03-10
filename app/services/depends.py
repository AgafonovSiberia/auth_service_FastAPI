

from app.db.engine import get_session_factory
from app.repo.base import SQLAlchemyRepo


async def get_repo():
	_session = get_session_factory()()
	try:
		repo: SQLAlchemyRepo = SQLAlchemyRepo(_session)
		yield repo
	finally:
		await _session.close()

