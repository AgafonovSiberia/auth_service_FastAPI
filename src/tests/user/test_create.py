import json
import pytest
from app.infrastructure.repo.user_repo import UserRepo
from app.api.schemas.user import UserFromDB, UserCreate
from app.api.schemas.activate_code import ActivateCode, ActivateUser
from tests.utils import generate_random_email, generate_random_password
from app.infrastructure.repo.base import SQLALchemyRepo
from httpx import AsyncClient
from fastapi.exception_handlers import HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, repo: SQLALchemyRepo):
    user = UserCreate(full_name="Ivan",
                      login=generate_random_email(),
                      password=generate_random_password())

    resp = await client.post("/user/", data=json.dumps(user.dict()))

    user_response: UserFromDB = UserFromDB.parse_obj(resp.json())
    assert resp.status_code == 200
    assert user.full_name == user_response.full_name
    assert user.login == user_response.login
    assert user_response.is_active is False
    assert user_response.is_admin is False

    user_from_db: UserFromDB = await repo.get_repo(UserRepo).get_user_by_id(user_response.user_id)
    assert user_from_db.full_name == user.full_name
    assert user_from_db.login == user.login
    assert user_from_db.is_active is False
    assert user_from_db.is_active is False


@pytest.mark.asyncio
async def test_activate_user(client: AsyncClient, repo: SQLALchemyRepo):
    user = UserCreate(full_name="Ivan",
                      login=generate_random_email(),
                      password=generate_random_password())

    resp = await client.post("/user/", data=json.dumps(user.dict()))
    user_response: UserFromDB = UserFromDB.parse_obj(resp.json())
    assert resp.status_code == 200

    code: ActivateCode = await repo.get_repo(UserRepo).check_activate_code_by_user_id(user_response.user_id)
    activate_user: ActivateUser = ActivateUser(user_id=code.user_id, code=code.code)
    resp = await client.put("/user/activate/", data=activate_user.json())
    user: UserFromDB = UserFromDB.parse_obj(resp.json())
    assert user.full_name == user_response.full_name
    assert user.login == user_response.login
    assert user.is_admin is False
    assert user.is_active is True


@pytest.mark.asyncio
async def test_user_already_exists(client: AsyncClient):
    user = UserCreate(full_name="Ivan",
                      login=generate_random_email(),
                      password=generate_random_password())

    await client.post("/user/", data=json.dumps(user.dict()))
    resp = await client.post("/user/", data=json.dumps(user.dict()))
    assert resp.status_code == 400
    assert resp.json() == {"detail": "The user with this login already exists"}


@pytest.mark.asyncio
async def test_not_valid_password(client: AsyncClient):
    user = {"full_name": "Ivan",
            "login": "user@mail.ru",
            "password": "short"}

    resp = await client.post("/user/", data=json.dumps(user))
    assert resp.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_not_valid_email(client: AsyncClient):
    user = {"full_name": "Ivan",
            "login": "some_not_valid_email",
            "password": generate_random_password()}

    resp = await client.post("/user/", data=json.dumps(user))
    assert resp.status_code == HTTP_422_UNPROCESSABLE_ENTITY

























