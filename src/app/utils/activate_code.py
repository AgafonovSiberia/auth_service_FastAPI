import random
import datetime


def generate_activate_code() -> int:
    code = random.randint(100000, 1000000)
    return code


def get_expire_timestamp(timeout: int):
    return (datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(seconds=timeout)).timestamp()
