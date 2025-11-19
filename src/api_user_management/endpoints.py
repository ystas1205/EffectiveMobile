from typing import Annotated, List, Union

from fastapi import APIRouter, Depends, HTTPException, status, Header, \
    Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_user_management.schemes import UserWithRole, AddPermission
from src.api_user_management.services import PermissionManager

from src.database.database import get_async_session

router_admin_permissions = APIRouter(tags=["Admin_Permissions"])


@router_admin_permissions.get(
    "/permissions", operation_id="admin_get_permissions",
    response_model=Union[List[UserWithRole], UserWithRole],
    status_code=status.HTTP_200_OK,
    summary="Получить пользователей с ролями и правами",
    description="""
    Получение списка пользователей с информацией о ролях и правах доступа.

    ### Требования доступа:
    - Только для администраторов с действительным JWT токеном

    ### Возвращаемые данные:
    - Полный список пользователей системы
    - Детали ролей и прав каждого пользователя
    """
)
async def get_permission(
        email: str = Query(
            None,
            description="Email пользователя для фильтрации результатов.",

            alias="user_email"
        ),
        jwt_token: Annotated[str | None, Header(alias="Jwt-Token")] = None,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Получение пользователей с их ролями и правами.
    """

    try:
        service = PermissionManager()
        user_permissions = await service.handle_user_permissions(
            email=email,
            jwt_token=jwt_token,
            session=session)
        return user_permissions
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}"
        )


@router_admin_permissions.put(
    "/update/permissions", operation_id="admin_update_permissions",
    response_model=UserWithRole,
    status_code=status.HTTP_200_OK,
    summary="Обновить права пользователя",
    description="""
    Изменение роли пользователя по email.

    **Доступ:**
     - только администраторы  
    **Вход:**
     -email пользователя, новая роль 
     """

)
async def update_user_permissions(
        user: AddPermission,

        email: str = Query(
            None,
            description="Email пользователя для фильтрации результатов.",

            alias="user_email"
        ),
        jwt_token: Annotated[str | None, Header(alias="Jwt-Token")] = None,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        service = PermissionManager()
        updated_user = await service.handle_update_permissions(
            user_schema=user,
            email=email,

            jwt_token=jwt_token,
            session=session
        )
        return updated_user
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}")
