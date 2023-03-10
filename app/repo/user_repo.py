from app.repo.base import BaseSQLAlchemyRepo
from app.db.models import User
from app.schemas.user import UserCreate, UserFull

from sqlalchemy import select


class UserRepo(BaseSQLAlchemyRepo):
    async def user_registration(self, user_data: UserCreate) -> UserFull:
        user = await self._session.merge(User(full_name=user_data.name,
                                              email=user_data.email,
                                              hashed_password=bytes(user_data.password, 'utf-8')))

        await self._session.commit()
        return user

    async def get_by_email(self, email: str):
        user = await self._session.execute(select(User).where(User.email == email))
        return user.first()

