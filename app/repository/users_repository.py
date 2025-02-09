import uuid
from collections.abc import Sequence
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User, UserCreate
from app.utilities.exceptions import NotFoundException, NotUniqueException


class UsersRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _check_unique_attr(self, attr: Any, value: Any) -> None:
        user_attr = getattr(User, attr)
        statement = select(user_attr).where(user_attr == value)
        attr_exist = (await self.session.exec(statement)).first()
        if attr_exist:
            raise NotUniqueException(item=attr.capitalize())

    async def create_user(self, user_in: UserCreate) -> User:
        user = User.model_validate(user_in)
        await self._check_unique_attr("email", user.email)
        await self._check_unique_attr("phone", user.phone)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_users(
        self, telegram_id: str | None = None, skip: int = 0, limit: int = 100
    ) -> tuple[Sequence[User], int]:
        statement = select(User).offset(skip).limit(limit)
        if telegram_id:
            statement = statement.where(User.telegram_id == telegram_id)
        items = (await self.session.exec(statement)).all()
        count = len(items)
        return items, count

    async def get_user(self, public_id: uuid.UUID) -> User:
        statement = select(User).where(User.public_id == public_id)
        result = await self.session.exec(statement)
        user = result.first()
        if not user:
            raise NotFoundException(item="User")
        return user
