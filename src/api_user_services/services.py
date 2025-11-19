import datetime

import uuid
import os

import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_user_services.auth import query_user_by_email, \
    protected_route, validation_role
from src.api_user_services.hashing import hash_password, check_password
from src.api_user_services.schemes import UserCreate, UserCreateResponse, \
    UserLogin, UserLoginResponse, UpdateUser, UpdateUserResponse, \
    LogoutUserResponse
from src.database.database_utils import add_to_session, commit_session
from src.models.models import User

load_dotenv()

JWT_SECRET = os.getenv('JWT__SECRET')
JWT_ALGORITHM = os.getenv('JWT__ALGORITHM')


class AuthService:

    async def handle_create_user(self,
                                 user_schema: UserCreate,
                                 session: AsyncSession,
                                 ):
        """
        Регистрация пользователя

        """

        user = await query_user_by_email(email=user_schema.email,
                                         session=session)

        if user:
            raise HTTPException(
                status_code=409,
                detail="Пользователь с таким email уже зарегистрирован.")

        # Проверка наличие роли в БД, при регистрации присваивается роль guest.
        role = await validation_role(role="guest", session=session)

        hashed_password = await hash_password(password=user_schema.password)

        new_user_id = uuid.uuid4()
        new_user = User(
            id=new_user_id,
            first_name=user_schema.first_name,
            last_name=user_schema.last_name,
            patronymic=user_schema.patronymic,
            email=user_schema.email,
            hashed_password=hashed_password,
            is_active=True,
            role_id=role.id

        )

        await add_to_session(session=session, object_to_add=new_user)
        await commit_session(session=session)

        response = UserCreateResponse(
            message="Регистрация прошла успешно!",
            id=new_user_id,
            email=user_schema.email
        )
        return response

    async def handle_user_login(self,
                                user_schema: UserLogin,
                                session: AsyncSession):

        """
        Вход пользователя в аккаунт
        """
        user = await query_user_by_email(email=user_schema.email,
                                         session=session)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Неверные учетные данные.")

        if not user.is_active:
            raise HTTPException(status_code=401,
                                detail="Учетная запись неактивна")

            # Получение хэшированного пароля из базы данных.
        hashed_password = user.hashed_password
        is_valid = await check_password(password=user_schema.password,
                                        hashed_password=hashed_password)
        if not is_valid:
            raise HTTPException(
                status_code=401, detail="Неверные учетные данные")

        # Формирование JWT-токена.
        payload = {
            'sub': str(user.id) if user else None,
            'email': user_schema.email,
            'iat': int(datetime.now(timezone.utc).timestamp()),
            'jti': str(uuid.uuid4()),
            'exp': int(
                (datetime.now(timezone.utc) + timedelta(days=1)).timestamp())
        }

        jwt_token = jwt.encode(payload, JWT_SECRET,
                               algorithm=JWT_ALGORITHM)

        # При авторизации присваивается роль user.
        if user:
            role = await validation_role(role="user", session=session)
            user.role_id = role.id

        await commit_session(session=session)

        response = UserLoginResponse(
            message="Вы вошли в аккаунт!",
            token=jwt_token

        )
        return response

    @protected_route
    async def handle_update_user(self,
                                 user_schema: UpdateUser,
                                 authenticated_user: User,
                                 jwt_token: str,
                                 session: AsyncSession,
                                 *args, **kwargs
                                 ):

        """
        Редактирование профиля.

        """

        if user_schema.password:

            # Получаем хэшированный пароль из базы данных.
            hashed_password = authenticated_user.hashed_password

            # Проверяем введенный пароль с хэш.паролем из базы данных.
            is_valid = await check_password(password=user_schema.password,
                                            hashed_password=hashed_password)

            if not is_valid:
                raise HTTPException(status_code=401, detail="Неверный пароль")

        for field, value in user_schema:
            if value:
                setattr(authenticated_user, field, value)

        await commit_session(session=session)

        response = UpdateUserResponse(
            message="Обновление профиля прошло успешно!",
            first_name=authenticated_user.first_name,
            last_name=authenticated_user.last_name,
            patronymic=authenticated_user.patronymic,
            email=authenticated_user.email

        )

        return response

    @protected_route
    async def handle_logout_user(self,
                                 authenticated_user: User,
                                 jwt_token: str,
                                 session: AsyncSession,
                                 *args, **kwargs):

        """ Выход из системы"""

        if authenticated_user:
            # Учетную запись оставляем.
            authenticated_user.is_active = False
            # Присваивается роль quest.
            role = await validation_role(role="guest", session=session)
            authenticated_user.role_id = role.id

            await commit_session(session=session)

            response = LogoutUserResponse(
                message="Аккаунт успешно удален!"
            )
            return response
        return None
