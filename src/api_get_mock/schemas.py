from typing import Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class Product(BaseModel):
    """ Схема получения продуктов """
    id: int
    name: str
    price: float
    category: str


class DeletePostResponse(BaseModel):
    """
    Схема ответа получения продуктов
    """
    message: str
    deleted_post: dict[str, Any]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Пост успешно удален",
                "deleted_post": {"id": 1, "title": "First Post",
                                 "content": "This is a sample post.",
                                 "author": "user1"}
            }
        }
    )


class UpdatePost(BaseModel):
    """
    Схема редактирования поста
    """
    title: str
    content: str
    author: str

    model_config = ConfigDict(from_attributes=True)


class UpdatePostResponse(BaseModel):
    """
    Схема ответа редактирования поста
    """
    message: str
    edited_post: dict[str, Any]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Пост успешно отредактирован",
                "edited_post": {"id": 1, "title": "First Post",
                                "content": "This is a sample post.",
                                "author": "user1"}
            }
        }
    )
