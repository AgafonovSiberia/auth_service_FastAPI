import bcrypt


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
