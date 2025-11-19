import uuid
from typing import  List

from sqlalchemy import UUID, ForeignKey, String, MetaData, func, Boolean, \
    DateTime, Table, Column

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

metadata = MetaData()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                     default=uuid.uuid4)

    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True,
                                       nullable=False, index=True)

    hashed_password: Mapped[str] = mapped_column(String(60), nullable=True)

    registered_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.current_timestamp())

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=False)
    role: Mapped["Role"] = relationship(back_populates="users")

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"))


role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                     default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[List[User]] = relationship(back_populates="role")

    permissions: Mapped[List["Permission"]] = relationship(
        secondary=role_permission,
        back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                     default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    roles: Mapped[List[Role]] = relationship(secondary=role_permission,
                                             back_populates="permissions")
