import datetime
import random


def generate_activate_code() -> int:
    code = random.randint(100000, 1000000)
    return str(code)


def get_expire_timestamp(timeout: int):
    return (
        datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=timeout)
    ).timestamp()
