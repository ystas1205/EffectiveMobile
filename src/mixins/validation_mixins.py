
import re
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo




class PasswordConfirmationValidator:
    """ Валидация пароля на подтверждение"""

    @field_validator('password_confirm', mode="after")
    def validate_password_match(cls, value, values: ValidationInfo):
        if value != values.data.get('password'):
            raise ValueError("Пароль не подтвержден.")
        return value


class PasswordValidationMixin:

    @field_validator('password')
    def validate_password(cls, password):
        """ Валидация пароля"""

        # Проверка на длину пароля
        if len(password) < 5 or len(password) > 64:
            raise ValueError(
                "Неверная длина пароля: Пароль должен содержать от 5 до 64 символов.")

        # Проверка на наличие хотя бы одной латинской буквы
        if not re.search(r'[a-zA-Z]', password):
            raise ValueError(
                "Нет букв в пароле: Пароль должен содержать хотя бы одну латинскую букву.")
        # Проверка на наличие хотя бы одной цифры
        if not re.search(r'[0-9]', password):
            raise ValueError(
                "Нет цифр в пароле: Пароль должен содержать хотя бы одну цифру.")
        # Пароль не должен содержать кириллицу
        if not re.match(r'^[^а-яА-ЯёЁ]+$', password):
            raise ValueError(
                "Смешение языков: Пароль не должен содержать символы из разных алфавитов.")
        return password
