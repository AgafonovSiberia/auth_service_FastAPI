from app.utils.security import check_password, crypt_password
from tests.utils import generate_random_password


def test_password_hashed():
    some_password = generate_random_password()
    hashed_password = crypt_password(some_password)
    assert check_password(some_password, hashed_password) is True
