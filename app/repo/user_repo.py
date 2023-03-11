from sqlalchemy import select, update

from app.repo.base import BaseSQLAlchemyRepo
from app.db.models import User
from app.schemas.user import UserCreate, UserFromDB
from app.services.security import crypt_password


class UserRepo(BaseSQLAlchemyRepo):
    async def user_add(self, user_data: UserCreate) -> UserFromDB:
        """
        Add user to database
        :param user_data: app.schemas.user.UserCreate
        :return: app.schemas.user.User
        """
        user = await self._session.merge(
            User(full_name=user_data.full_name, email=user_data.email,
                 hashed_password=crypt_password(user_data.password)))

        await self._session.commit()
        return user


    async def activate_account(self, activate_code: str) -> UserFromDB:
        pass




    async def get_by_email(self, email: str) -> UserFromDB:
        """
        Get user from database by email
        :param email:
        :return: app.schemas.user.User
        """
        user = await self._session.execute(select(User).where(User.email == email))
        return user.first()

