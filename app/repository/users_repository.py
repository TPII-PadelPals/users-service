import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User, UserCreate


class UsersRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user_in: UserCreate) -> User:
        user = User.model_validate(user_in)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user(self, id: uuid.UUID) -> User:
        user = await self.session.get(User, id)
        if not user:
            raise IndexError()
            # raise NotFoundException(item="Item")
        return user
