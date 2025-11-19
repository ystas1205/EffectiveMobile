import os
from functools import wraps

from jose import jwt, ExpiredSignatureError
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.models import User, Role

JWT_SECRET = os.getenv('JWT__SECRET')
JWT_ALGORITHM = os.getenv('JWT__ALGORITHM')


async def query_user_by_email(email: str, session: AsyncSession) -> User:
    """
    Получение пользователя по email с проверкой активации.
    """

    stmt = select(User).where(User.email == email).options(
        selectinload(User.role))
    user_exists = await session.scalars(stmt)
    user = user_exists.first()
    return user


async def validation_user(user_id: str, user_email: str,
                          session: AsyncSession):
    """
    Проверка есть ли пользователь с переданным токеном.
    """

    stmt = select(User).where(User.email == user_email,
                              User.id == user_id).options(
        selectinload(User.role).options(selectinload(Role.permissions)))
    user_exist = await  session.scalars(stmt)
    user = user_exist.first()
    if not user:
        raise HTTPException(status_code=401,
                            detail="Вы не авторизованы")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Учетная запись неактивна")

    return user


async def validation_role(role: str, session: AsyncSession):
    """
    Проверка есть ли роль для пользователя.
    """

    stmt = select(Role).where(Role.name == role)
    role_exist = await session.scalars(stmt)
    role = role_exist.first()
    if not role:
        if not role:
            raise HTTPException(status_code=500,
                                detail="Роль 'guest' не найдена в БД.")
    return role


def protected_route(func):
    """
    Аутентификация пользователя по jwt-token.
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):

        user_schema = kwargs.get("user", None)
        jwt_token = kwargs.get("jwt_token", None)
        permissions_required = kwargs.get("permissions_required", None)
        session = kwargs.get("session", None)

        if not jwt_token:
            raise HTTPException(status_code=401,
                                detail="Вы не авторизованы")
        try:
            payload = jwt.decode(jwt_token, JWT_SECRET,
                                 algorithms=[JWT_ALGORITHM])

        except ExpiredSignatureError:
            raise HTTPException(status_code=401,
                                detail="Срок действия токена истек")

        user_id = payload.get("sub", None)
        user_email = payload.get("email", None)

        # Запрос получения пользователя по данным jwt токен
        user = await validation_user(user_id=user_id,
                                     user_email=user_email,
                                     session=session)

        # Роль пользователя
        user_role = user.role.name
        # Список прав пользователя
        list_permissions = [permission.code for permission in
                            user.role.permissions]

        if permissions_required:

            if permissions_required not in list_permissions:
                raise HTTPException(status_code=403,
                                    detail="Ресурс не доступен")

        result = await  func(self, authenticated_user=user, *args, **kwargs)

        return result

    return wrapper
