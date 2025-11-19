from functools import wraps

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.api_user_services.auth import protected_route
from src.database.database_utils import commit_session
from src.models.models import User, Role


class PermissionManager:

    @protected_route
    async def handle_user_permissions(self, email: str,
                                      jwt_token: str,
                                      authenticated_user: User,
                                      session: AsyncSession,
                                      *args, **kwargs):

        """
        Получение прав пользователей
        """

        if authenticated_user.role.name != "admin":
            raise HTTPException(status_code=403,
                                detail="Ресурс не доступен")

        if not email:
            raise HTTPException(
                status_code=400,
                detail="Необходимо указать email.")

        if authenticated_user.role.name != "admin":
            raise HTTPException(status_code=403,
                                detail="Ресурс не доступен")

        stmt = select(User).where(User.email == email).options(
            selectinload(User.role).options(selectinload(Role.permissions)))

        user_exist = await session.scalars(stmt)
        user = user_exist.first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"Пользователь с email {email} не найден")

        return user

    @protected_route
    async def handle_update_permissions(self,
                                        user_schema: str,
                                        email: str,
                                        jwt_token: str,
                                        authenticated_user: User,
                                        session: AsyncSession,
                                        *args, **kwargs):

        """
        Обновление прав пользователя
        """

        if authenticated_user.role.name != "admin":
            raise HTTPException(status_code=403,
                                detail="Ресурс не доступен")

        if not email:
            raise HTTPException(
                status_code=400,
                detail="Необходимо указать email.")

        stmt = select(User).where(User.email == email).options(
            joinedload(User.role).options(joinedload(Role.permissions)))

        user_exist = await session.scalars(stmt)
        user = user_exist.first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"Пользователь с email {email} не найден")

        new_role = user_schema.role

        stmt = select(Role).where(Role.name == new_role)
        exist_role = await session.scalars(stmt)
        role = exist_role.first()

        if not role:
            raise HTTPException(status_code=404,
                                detail=f"Роли {user_schema.role} не существует")

        user.role_id = role.id

        await commit_session(session=session)

        await session.refresh(user)

        return user
