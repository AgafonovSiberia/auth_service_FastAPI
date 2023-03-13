from calendar import timegm
import datetime

from fastapi import (APIRouter, Depends,
                     HTTPException)
from fastapi.responses import JSONResponse
from app.repo.base import Repository
from app.repo.user_repo import UserRepo
from app.schemas.user import UserCreate, UserFromDB
from app.schemas.activate_code import ActivateCode, CodeBase
from app.services.depends import get_repo
from app.utils.activate_code import generate_activate_code


from app.config_reader import config
router = APIRouter()


@router.post("/signup/", response_model=UserFromDB)
async def signup_account(user_data: UserCreate, repo: Repository = Depends(get_repo)):
    """
    The signup_account function creates a new user in the database.

    :param user_data: UserCreate: Specify the type of data that will be passed to the function
    :param repo: Repository: Repository object
    :return:  app.schemas.user.UserFromDB
    """
    user: UserFromDB = await repo.get_repo(UserRepo).get_by_email(login=user_data.login)
    if user:
        raise HTTPException(status_code=400, detail="The user with this login already exists")

    user: UserFromDB = await repo.get_repo(UserRepo).user_add(user_data=user_data)
    return user


@router.post("/activate/{user_id}/{activate_code}")
async def activate_account(user_id: int, activate_code: int):
    print(activate_code)


@router.get("/activate/get_code/{user_id}")
async def get_activate_code(user_id: int, repo: Repository = Depends(get_repo)):
    code: ActivateCode = await repo.get_repo(UserRepo).check_activate_code(user_id)
    if code:
        raise HTTPException(status_code=400, detail="This user has a valid activation code")

    activate_code = generate_activate_code()
    exp_time = (datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(seconds=config.TTL_CODE_ACTIVATE)).timestamp()
    print(type(exp_time))


    code: ActivateCode = await repo.get_repo(UserRepo).add_code_activate(user_id=user_id,
                                                                         code_activate=activate_code,
                                                                         expire=exp_time)
    return JSONResponse(content={"code": code.code, "code_expire": code.expire})

