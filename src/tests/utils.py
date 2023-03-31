import random
import string


def generate_random_email() -> str:
    login = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    return f"{login}@yandex.ru"


def generate_random_password() -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(random.randint(8, 12)))
