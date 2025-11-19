import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class Permission(BaseModel):
    id: uuid.UUID
    name: str
    code: str
    description: str


class Role(BaseModel):
    id: uuid.UUID
    name: str
    permissions: List[Permission]


class UserWithRole(BaseModel):
    """
    Схема ответа получения прав пользователя
    """
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    patronymic: str
    hashed_password: str
    is_active: bool
    registered_at: datetime
    role_id: uuid.UUID
    role: Role


class AddPermission(BaseModel):
    """
    Схема изменения роли пользователя
    """
    role: str

    model_config = ConfigDict(from_attributes=True)
