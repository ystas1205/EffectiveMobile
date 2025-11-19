from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def commit_session(session: AsyncSession):
    """
    Сохраняет изменения в базе данных
    """
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка базы данных: {e}"
        )


async def add_to_session(session: AsyncSession, object_to_add):
    """
    Добавляет объект в сессию SQLAlchemy
    """

    try:
        session.add(object_to_add)

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка базы данных: {e}"
        )
