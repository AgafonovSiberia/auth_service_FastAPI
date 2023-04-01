from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.api.depends.db import get_repo
from app.api.schemas.activate_code import ActivateCode, ActivateUser
from app.api.schemas.user import UserCreate, UserFromDB
from app.config_reader import config
from app.infrastructure.repo.base import SQLALchemyRepo
from app.infrastructure.repo.user_repo import UserRepo
from app.infrastructure.workflow.tasks import send_message_with_code
from app.infrastructure.workflow.tasks.periodic import clean_expire_code_activate
from app.utils.activate_code import generate_activate_code, get_expire_timestamp

router = APIRouter(prefix="/user")


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


@router.get("/activate/{user_id}")
async def get_activate_code(user_id: UUID, repo: SQLALchemyRepo = Depends(get_repo)):
    """
    Получение кода активации для подтверждения аккаунта
    :param user_id: ID пользователя
    :param repo: объект Репозитория
    """
    user: UserFromDB = await repo.get_repo(UserRepo).get_user_by_id(user_id)
    code: ActivateCode = await repo.get_repo(UserRepo).check_activate_code_by_user_id(user_id)

    if not user or user.is_active or code:
        raise HTTPException(
            status_code=400, detail="This user is currently" "unable to receive an activation code"
        )

    code: ActivateCode = await repo.get_repo(UserRepo).add_code_activate(
        user_id=user_id,
        code_activate=generate_activate_code(),
        expire=get_expire_timestamp(config.TTL_CODE_ACTIVATE),
    )

    send_message_with_code.delay(subject="activate", address_to=user.login, code=code.code)

    return JSONResponse(status_code=200, content={"message": "Activation code sent successfully"})


# @router.get("/check/{user_id}")
# async def get_activate_code(user_id: UUID, repo: SQLALchemyRepo = Depends(get_repo)):
#     code = await repo.get_repo(UserRepo).check_activate_code_by_user_id(user_id)
#     print(code)
#     print(type(code))
#     return code


@router.put("/activate/", response_model=UserFromDB)
async def activate_user(activate_data: ActivateUser, repo: SQLALchemyRepo = Depends(get_repo)):
    """
    Активация пользователя
    :param activate_data: модель (id, activate_code)
    :param repo: объект Репозитория
    :return: schemas.user.UserFromDB
    """
    check_code: ActivateCode = await repo.get_repo(UserRepo).check_activate_code_by_code(
        activate_data.code
    )
    user: UserFromDB = await repo.get_repo(UserRepo).get_user_by_id(activate_data.user_id)
    if not check_code:
        raise HTTPException(status_code=400, detail="This code has expired")

    if not user:
        raise HTTPException(status_code=400, detail="This user not found")

    user: UserFromDB = await repo.get_repo(UserRepo).activate_user(user_id=activate_data.user_id)

    return user


@router.delete("/delete", response_model=UserFromDB)
async def delete_user(user_id: UUID, repo: SQLALchemyRepo = Depends(get_repo)):
    user = await repo.get_repo(UserRepo).delete_user(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="This user not found")

    return user


@router.get("/delete")
async def delete_expire_codes():
    """Только для тестирования"""
    clean_expire_code_activate.delay()
