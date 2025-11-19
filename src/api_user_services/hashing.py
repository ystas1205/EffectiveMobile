
import bcrypt


async def hash_password(password: str) -> str:
    """
     Хеширование пароля.
     """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


async def check_password(password: str, hashed_password: str) -> bool:
    """
    Проверка хэшированного пароля.
    """
    return bcrypt.checkpw(password.encode('utf-8'),
                          hashed_password.encode('utf-8'))


