import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from src.mixins.validation_mixins import PasswordConfirmationValidator, \
    PasswordValidationMixin


class UserCreate(PasswordConfirmationValidator, PasswordValidationMixin,
                 BaseModel):
    """
     Схема регистрации пользователя
     """

    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    password: str
    password_confirm: str

    model_config = ConfigDict(from_attributes=True)


class UserCreateResponse(BaseModel):
    """
     Схема ответа регистрации пользователя
     """
    message: str
    id: uuid.UUID
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Регистрация прошла успешно!",
                "id": "dfb59daf-0960-40b8-96f3-7c57d7f535ba",
                "email": "anything@example.com",

            }
        }
    )


class UserLogin(PasswordValidationMixin, BaseModel):
    """
    Схема входа пользователя в систему
    """

    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserLoginResponse(BaseModel):
    """
    Схема ответа входа пользователя в систему
    """

    message: str
    token: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Вы вошли в аккаунт!",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoi"
                         "NGZmMzFjNDQtZTEwZi00NTNjLTg2ZTAtNDBmNjAzOTMwODIzIiwi"
                         "ZXhwIjoxNzM5NTQ2NjgzLjAyNzM1MX0YO8WM0et49imCluzOJt91"
                         "JIZfey9ROWeKT_IVBTlo"

            }
        }
    )


class UpdateUser(PasswordConfirmationValidator,
                 PasswordValidationMixin,
                 BaseModel):
    """
    Схема редактирования профиля
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    password: Optional[str] = None
    password_confirm: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserResponse(BaseModel):
    """
    Схема ответа редактирования профиля
    """
    message: str
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Обновление профиля прошло успешно!",
                "first_name": "Иван",
                "last_name": "Иванов",
                "patronymic": "Иванович",
                "email": "ivan.ivanov@example.com"
            }
        }
    )


class LogoutUserResponse(BaseModel):
    """
    Схема ответа удаления аккаунта
    """
    message: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Аккаунт успешно удален!",

            }
        }
    )
