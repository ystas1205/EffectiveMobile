from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Header, \
    Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_get_mock.schemas import Product, DeletePostResponse, UpdatePost, \
    UpdatePostResponse

from src.api_get_mock.services import MockView

from src.database.database import get_async_session

router_mock_objects = APIRouter(tags=["Mock-View"])


@router_mock_objects.get(
    "/get_product",operation_id="mock_list_product",
    response_model=Dict[int, Product],
    status_code=status.HTTP_200_OK,
    summary="Получить список продуктов",
    description="""
        Эндпоинт для получения списка всех продуктов.

        ### Требуемые права:
        - **list_product** - право на просмотр списка продуктов

        ### Группы пользователей с доступом:
        - admin
        - moderator  
        - guest
        - user
        """

)
async def get_product(

        jwt_token: Annotated[str | None, Header(alias="Jwt-Token")] = None,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Получение продуктов.
    """

    permissions_required = "list_product"

    try:

        service = MockView()
        product = await service.handle_get_product(
            jwt_token=jwt_token,
            permissions_required=permissions_required,
            session=session)
        return product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}"
        )


@router_mock_objects.delete(
    "/delete_post",operation_id="mock_delete_post",
    response_model=DeletePostResponse,
    status_code=status.HTTP_200_OK,
    summary="Удалить пост",
    description="""
            Эндпоинт для удаления поста по ID.

            ### Требуемые права:
            - **delete_post** - право на удаления поста

            ### Группы пользователей с доступом:
            - admin
            - moderator  
            """
)
async def remove_post(
        id_post: int = Query(
            None,
            description="ID поста для удаления",
            alias="id_post"
        ),
        jwt_token: Annotated[str | None, Header(alias="Jwt-Token")] = None,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Удаление постов.
    """

    permissions_required = "delete_post"

    try:

        service = MockView()
        rem_post = await service.handle_remove_post(
            id_post=id_post,
            jwt_token=jwt_token,
            permissions_required=permissions_required,
            session=session)
        return rem_post
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}"
        )


@router_mock_objects.patch(
    "/update_post",operation_id="mock_update_post",
    response_model=UpdatePostResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить пост",
    description="""
                Эндпоинт для обновления поста по ID.

                ### Требуемые права:
                - **update_post** - право на редактирование поста

                ### Группы пользователей с доступом:
                - admin
                - moderator 
                - user 
                """
)
async def update_post(
        post_schema: UpdatePost,
        id_post: int = Query(
            None,
            description="ID поста для обновления",
            alias="id_post"
        ),
        jwt_token: Annotated[str | None, Header(alias="Jwt-Token")] = None,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Обновление постов.
    """

    permissions_required = "update_post"

    try:

        service = MockView()
        update = await service.handle_edit_post(
            post_schema=post_schema,
            id_post=id_post,
            jwt_token=jwt_token,
            permissions_required=permissions_required,
            session=session)
        return update
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка: {e}"
        )
