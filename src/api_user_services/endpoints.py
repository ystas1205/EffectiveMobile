from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_user_services.schemes import UserCreate, UserCreateResponse, \
    UserLogin, UserLoginResponse, UpdateUser, UpdateUserResponse, \
    LogoutUserResponse
from src.api_user_services.services import AuthService
from src.database.database import get_async_session

router_user = APIRouter(tags=["Auth_Users"])


@router_user.post(
    "/register", operation_id="auth_register_user",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
    description="""
    Эндпоинт для регистрации нового пользователя в системе.
    
    ### Особенности регистрации:
    - Создает новую учетную запись пользователя
    - Хеширует пароль для безопасного хранения
    - Назначает роль "guest" по умолчанию
    - Активирует учетную запись (is_active=True)
    - Генерирует JWT токен для последующей аутентификации
    
    ### Требования к данным:
    - Email должен быть уникальным и валидным
    - Пароль должен должен быть безопасным
    """
)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(get_async_session)):
    """
    Регистрация пользователя.
    """

    try:
        service = AuthService()
        request_register_user = await service.handle_create_user(
            user_schema=user,
            session=session,
        )
        return request_register_user
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}"
        )


@router_user.post(
    "/login",operation_id="auth_login_user",
    response_model=UserLoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Войти в аккаунт (по email и паролю)",
    description="""
    Эндпоинт для входа пользователя в систему.
    
    ### Процесс аутентификации:
    - Проверяет валидность email и пароля
    - Верифицирует хеш пароля в базе данных
    - Проверяет активность учетной записи
    - Генерирует JWT токен для доступа к защищенным эндпоинтам
    - Возвращает сообщение об успешной авторизации и jwt токен доступа сроком
     24 часа 
    """

)
async def login_user(
        user: UserLogin,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Вход в аккаунт пользователя
    """

    try:
        service = AuthService()
        login = await service.handle_user_login(user_schema=user,
                                                session=session)
        return login
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}"
        )


@router_user.post(
    "/update", operation_id="auth_update_user",
                  response_model=UpdateUserResponse,
                  status_code=status.HTTP_200_OK,
                  summary="Редактировать профиль ",

                  description="""
    Эндпоинт для редактирования данных пользовательского профиля.
    
    ### Особенности обновления:
    - Редактировать свой профиль может только авторизованный пользователь
    - Позволяет изменить основные данные профиля
    - Поддерживает частичное обновление (только указанные поля)
   
    """
                  )
async def update_user(user: UpdateUser,

                      jwt_token: Annotated[
                          str | None, Header(alias="Jwt-Token")] = None,

                      session: AsyncSession = Depends(get_async_session)):
    """
    Редактирование профиля пользователя
    """

    try:
        service = AuthService()
        editing_profile = await service.handle_update_user(
            user_schema=user,
            jwt_token=jwt_token,
            session=session
        )
        return editing_profile
    except Exception as e:

        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}")


@router_user.post(
    "/logout",operation_id="auth_logout_user",
                  response_model=LogoutUserResponse,
                  status_code=status.HTTP_200_OK,
                  summary="Удалить аккаунт",

                  description="""
    Эндпоинт для выхода пользователя из системы.
    
    ### Особенности выхода:
    - Деактивирует текущую сессию пользователя
    - Не удаляет учетную запись пользователя
    - Пользователь больше не может залогиниться
  
    """
                  )
async def logout_user(
        jwt_token: Annotated[str | None, Header(alias="Jwt-Token")] = None,
        session: AsyncSession = Depends(get_async_session)):
    """
     Эндпойнт выхода пользователя из системы
     """

    try:
        service = AuthService()
        logout = await service.handle_logout_user(
            jwt_token=jwt_token,
            session=session)
        return logout
    except Exception as e:

        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}")
