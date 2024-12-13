import uuid
from collections.abc import Sequence

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User, UserCreate
from app.utilities.exceptions import NotFoundException


class UsersRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user_in: UserCreate) -> User:
        user = User.model_validate(user_in)
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

    async def get_user(self, id: uuid.UUID) -> User:
        user = await self.session.get(User, id)
        if not user:
            raise NotFoundException(item="User")
        return user
