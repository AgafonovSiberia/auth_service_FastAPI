from fastapi import APIRouter, Depends, HTTPException
from utils.security.activate_code import generate_activate_code, get_expire_timestamp

from app.api.depends.db import get_repo
from app.api.schemas.activate_code import ActivateCode
from app.api.schemas.user import UserCreate, UserFromDB
from app.config_reader import config
from app.infrastructure.repo.base import SQLALchemyRepo
from app.infrastructure.repo.user_repo import UserRepo
from app.infrastructure.workflow.tasks import send_message_with_code

router = APIRouter(prefix="/login")


@router.post("/", response_model=UserFromDB)
async def create_user(user_data: UserCreate, repo: SQLALchemyRepo = Depends(get_repo)):
    """
    Регистрация нового пользователя

    :param user_data: UserCreate: модель регистрационных данных пользователя
    :param repo: объект Репозитория
    :return: schemas.user.UserFromDB
    """
    user: UserFromDB = await repo.get_repo(UserRepo).get_user_by_email(login=user_data.login)
    if user:
        raise HTTPException(status_code=400, detail="The user with this login already exists")

    user: UserFromDB = await repo.get_repo(UserRepo).add_user(user_data=user_data)

    code: ActivateCode = await repo.get_repo(UserRepo).add_code_activate(
        user_id=user.user_id,
        code_activate=generate_activate_code(),
        expire=get_expire_timestamp(config.TTL_CODE_ACTIVATE),
    )

    send_message_with_code.delay(subject="activate", address_to=user.login, code=code.code)

    return user
