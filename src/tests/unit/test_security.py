import asyncio
import datetime
import uuid
from calendar import timegm

import jwt.exceptions
import pytest
from utils.security.hashed import check_password, crypt_password
from utils.security.jwt import check_token, create_token

from tests.utils import generate_random_password


def test_password_hashed():
    some_password = generate_random_password()
    hashed_password = crypt_password(some_password)
    assert check_password(some_password, hashed_password) is True


def test_valid_token():
    user_id = uuid.uuid4()
    token, exp = create_token(user_id, "access")
    check = check_token(token)
    assert check.get("status") == "ok"


@pytest.mark.asyncio
async def test_expire_token():
    user_id = uuid.uuid4()
    test_exp = timegm(
        (
            datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=1)
        ).utctimetuple()
    )
    token, exp = create_token(user_id, "access", exp=test_exp)
    print(token)
    await asyncio.sleep(1)
    check = check_token(token, leeway=0)
    assert check.get("status") == "error"
    assert check.get("message") == "token has expired"


def test_value_error_token():
    with pytest.raises(jwt.exceptions.DecodeError):
        check_token(bytes("some_token", "utf-8"))


def test_invalid_token():
    user_id = uuid.uuid4()
    token, exp = create_token(user_id, "access", secret_key="some_invalid_key")
    check = check_token(token)
    assert check.get("status") == "error"
    assert check.get("message") == "invalid token"
