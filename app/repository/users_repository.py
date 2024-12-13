import uuid
from collections.abc import Sequence
from typing import Any

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User, UserCreate
from app.utilities.exceptions import NotFoundException, NotUniqueError


class UsersRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _check_unique_attr(self, attr: Any, value: Any) -> None:
        statement = select(getattr(User, attr)).where(getattr(User, attr) == value)
        exists = (await self.session.exec(statement)).first() is not None
        if exists:
            raise NotUniqueError(item=attr.capitalize())

    async def create_user(self, user_in: UserCreate) -> User:
        user = User.model_validate(user_in)
        await self._check_unique_attr("email", user.email)
        await self._check_unique_attr("phone", user.phone)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_users(
        self,
    ) -> tuple[Sequence[User], int]:  # , skip: int = 0, limit: int = 100
        count_statement = select(func.count()).select_from(User)
        count = (await self.session.exec(count_statement)).one()
        statement = select(User)  # .offset(skip).limit(limit)
        items = (await self.session.exec(statement)).all()
        return items, count

    async def get_user(self, public_id: uuid.UUID) -> User:
        statement = select(User).where(User.public_id == public_id)
        result = await self.session.exec(statement)
        user = result.first()
        if not user:
            raise NotFoundException(item="User")
        return user
