from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_user_services.auth import protected_route
from src.mockobjects.mock import products_db, posts_db
from src.models.models import User


class MockView:

    @protected_route
    async def handle_get_product(self,

                                 jwt_token: str,
                                 authenticated_user: User,
                                 permissions_required: str,
                                 session: AsyncSession,
                                 *args, **kwargs):

        if not products_db:
            raise HTTPException(
                status_code=404,
                detail="Продукты  не найдены"
            )

        product_data = products_db
        return product_data

    @protected_route
    async def handle_remove_post(self,
                                 id_post: int,
                                 authenticated_user: User,
                                 jwt_token: str,
                                 permissions_required: str,
                                 session: AsyncSession,
                                 *args, **kwargs):
        """
        Удаление поста с проверкой прав
        """

        if id_post not in posts_db:
            raise HTTPException(
                status_code=404,
                detail=f"Пост с ID {id_post} не найден"
            )

        deleted_post = posts_db.pop(id_post)

        return {
            "message": "Пост успешно удален",
            "deleted_post": deleted_post
        }

    @protected_route
    async def handle_edit_post(self,
                               id_post: int,
                               post_schema: str,
                               authenticated_user: User,
                               jwt_token: str,
                               permissions_required: str,
                               session: AsyncSession,
                               *args, **kwargs):

        if id_post not in posts_db:
            raise HTTPException(
                status_code=404,
                detail=f"Пост с ID {id_post} не найден"
            )

        edit_post = posts_db.get(id_post, None)

        for field, name in post_schema:
            if field in edit_post:
                edit_post[field] = name

        return {"message": "Пост успешно отредактирован",
                "edited_post": edit_post}
