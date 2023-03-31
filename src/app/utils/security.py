import datetime
from calendar import timegm

import bcrypt
import jwt

from app.config_reader import config

TTL_AT = config.TTL_ACCESS_TOKEN
TTL_RT = config.TTL_REFRESH_TOKEN


def crypt_password(password: str) -> str:
    """
    Password crypt
    :param password: row password
    :return: hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hash_password: str) -> bool:
    """
    Password validator
    :param password: row password string
    :param hash_password: hashed password string
    :return: True if password is valid else False
    """
    return bcrypt.checkpw(password.encode(), hash_password)


def create_token(user_id: int, type_token: str):
    """
    Create JWT-token
    :param user_id:
    :param type_token: "access" | "refresh"
    :return: (jwt-token string, datetime it token expires)
    """
    exp = timegm(
        (
            datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(minutes=TTL_AT if type_token == "access" else TTL_RT)
        ).utctimetuple()
    )
    token = jwt.encode(
        payload={"user_id": user_id, "exp": exp},
        key=config.SECRET_KEY,
        headers={"type": "JWT", "type_token": type_token, "alg": "HS256"},
        algorithm="HS256",
    )
    return token, exp


# async def check_token(token: str):
#     """Проверка валидности jwt-токена, созданного сервером"""
#     try:
#         if token is None:
#             raise InvalidSignatureError
#         payload = jwt.decode(
#             jwt=token,
#             key=config.SECRET_KEY,
#             algorithms="HS256",
#             verify_signature=True,
#             leeway=10,
#         )
#     except InvalidSignatureError:
#         return {"status": "error", "message": "invalid token"}
#     except ExpiredSignatureError:
#         return {"status": "error", "message": "token has expired"}
#     else:
#         return {"status": "ok", "message": "correct token", "payload": payload}
