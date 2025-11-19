import json
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, text
from contextlib import asynccontextmanager

from src.database.database import Session

from src.models.models import Role, Permission, role_permission, User

file_path = Path(__file__).parent / "role_permissions.json"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем сессию один раз
    async with Session() as session:
        try:

            # await session.execute(delete(User))
            await session.execute(delete(role_permission))
            await session.execute(delete(Permission))
            await session.execute(delete(Role))
            await session.commit()

            with open(file_path, 'r') as file:
                data = json.load(file)

            roles_dict = {}
            permissions_dict = {}

            if "roles" in data:
                for role_data in data["roles"]:
                    role = Role(id=role_data["id"], name=role_data["name"])
                    roles_dict[role_data["id"]] = role
                    session.add(role)

            if "permissions" in data:
                for perm_data in data["permissions"]:
                    perm = Permission(
                        id=perm_data["id"],
                        name=perm_data["name"],
                        code=perm_data["code"],
                        description=perm_data.get("description", "")
                    )
                    permissions_dict[perm_data["id"]] = perm
                    session.add(perm)

            if "role_permissions" in data:
                for rp_data in data["role_permissions"]:
                    role_id = rp_data["role_id"]
                    perm_id = rp_data["permission_id"]
                    role = roles_dict.get(role_id)
                    permission = permissions_dict.get(perm_id)
                    if role and permission:
                        role.permissions.append(permission)

            await session.commit()

        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            await session.rollback()

    yield

    try:
        # await session.execute(delete(User))
        await session.execute(delete(role_permission))
        await session.execute(delete(Permission))
        await session.execute(delete(Role))
        await session.commit()
    except Exception as e:
        print(f"Ошибка при очистке: {e}")
        await session.rollback().rollback()
