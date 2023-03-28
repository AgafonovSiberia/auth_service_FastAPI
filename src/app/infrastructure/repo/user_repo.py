import datetime

from sqlalchemy import select, update

from app.infrastructure.db.models import User, ActivateCode
from app.api.schemas.user import UserCreate, UserFromDB
from app.utils.security import crypt_password
from app.infrastructure.repo.base.base import BaseSQLAlchemyRepo


class UserRepo(BaseSQLAlchemyRepo):
    async def add_user(self, user_data: UserCreate) -> UserFromDB:
        """
        Add user to database
        :param user_data: src.schemas.user.UserCreate
        :return: src.schemas.user.User
        """
        user = await self._session.merge(
            User(
                full_name=user_data.full_name,
                login=user_data.login,
                hashed_password=crypt_password(user_data.password),
            )
        )

        await self._session.commit()
        return user

    async def activate_user(self, user_id: int) -> UserFromDB:
        query = (
            update(User)
            .where(User.id == user_id)
            .values(is_active=True)
            .returning(User)
        )
        user = (
            select(User).from_statement(query).execution_options(populate_existing=True)
        )
        await self._session.commit()
        return user

    async def get_by_email(self, login: str) -> UserFromDB:
        """
        Get user from database by email
        :param login: логин пользователя (email / номер телефона)
        :return: src.schemas.user.User
        """
        user = await self._session.execute(select(User).where(User.login == login))
        return user.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> UserFromDB:
        user = await self._session.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()

    async def add_code_activate(self, user_id: int, code_activate: int, expire: int):
        code = await self._session.merge(
            ActivateCode(user_id=user_id, code=code_activate, expire=expire)
        )
        await self._session.commit()
        return code

    async def check_activate_code_by_user_id(self, user_id: int):
        code = await self._session.execute(
            select(ActivateCode)
            .where(
                ActivateCode.expire
                > datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
            )
            .where(ActivateCode.user_id == user_id)
        )
        return code.first()

    async def check_activate_code_by_code(self, code: int):
        code = await self._session.execute(
            select(ActivateCode)
            .where(ActivateCode.expire > datetime.datetime.now().timestamp())
            .where(ActivateCode.code == code)
        )
        return code.first()
