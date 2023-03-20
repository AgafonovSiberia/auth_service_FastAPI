import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.repo.base.repository import SQLALchemyRepo
from app.repo.user_repo import UserRepo
from app.schemas.user import UserCreate, UserFromDB
from app.schemas.activate_code import ActivateCode, ActivateUser
from app.depends.db import get_repo
from app.utils.activate_code import generate_activate_code
from app.services.workflow.tasks.send_tasks import send_message_with_code


from app.config_reader import config

router = APIRouter(prefix="/signup")


@router.post("/", response_model=UserFromDB)
async def signup_account(
    user_data: UserCreate, repo: SQLALchemyRepo = Depends(get_repo)
):
    """
    The signup_account function creates a new user in the database.

    :param user_data: UserCreate: Specify the type of data that
     will be passed to the function
    :param repo: Repository: Repository object
    :return:  app.schemas.user.UserFromDB
    """
    user: UserFromDB = await repo.get_repo(UserRepo).get_by_email(login=user_data.login)
    if user:
        raise HTTPException(
            status_code=400, detail="The user with this login already exists"
        )

    user: UserFromDB = await repo.get_repo(UserRepo).add_user(user_data=user_data)
    return user


@router.post("/activate/", response_model=UserFromDB)
async def activate_account(
    activate_data: ActivateUser, repo: SQLALchemyRepo = Depends(get_repo)
):
    code: ActivateCode = await repo.get_repo(UserRepo).check_activate_code_by_code(
        activate_data.code
    )
    if not code:
        raise HTTPException(status_code=400, detail="This code has expired")
    user: UserFromDB = await repo.get_repo(UserRepo).activate_user(
        user_id=activate_data.id
    )

    return user


@router.get("/activate/get_code/{user_id}")
async def get_activate_code(user_id: int, repo: SQLALchemyRepo = Depends(get_repo)):
    user: UserFromDB = await repo.get_repo(UserRepo).get_by_id(user_id)
    code: ActivateCode = await repo.get_repo(UserRepo).check_activate_code_by_user_id(
        user_id
    )
    if not user or code:
        raise HTTPException(
            status_code=400,
            detail="This user is currently unable to receive an activation code",
        )

    activate_code = generate_activate_code()
    exp_time = (
        datetime.datetime.now(tz=datetime.timezone.utc)
        + datetime.timedelta(seconds=config.TTL_CODE_ACTIVATE)
    ).timestamp()

    code: ActivateCode = await repo.get_repo(UserRepo).add_code_activate(
        user_id=user_id, code_activate=activate_code, expire=exp_time
    )

    send_message_with_code.delay(
        subject="activate", address_to=user.login, code=code.code
    )
    return JSONResponse(
        status_code=200, content={"message": "User account successfully activated"}
    )
