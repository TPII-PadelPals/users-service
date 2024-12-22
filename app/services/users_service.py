import uuid

from app.models.user import User, UserCreate, UsersPublic
from app.repository.users_repository import UsersRepository
from app.utilities.dependencies import SessionDep


class UsersService:
    async def create_user(self, session: SessionDep, user_in: UserCreate) -> User:
        repo = UsersRepository(session)
        user = await repo.create_user(user_in)
        return user

    async def read_users(
        self,
        session: SessionDep,
        telegram_id: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> UsersPublic:
        repo = UsersRepository(session)
        users, count = await repo.get_users(telegram_id, skip, limit)
        return UsersPublic(data=users, count=count)

    async def read_user(self, session: SessionDep, id: uuid.UUID) -> User:
        repo = UsersRepository(session)
        user = await repo.get_user(id)
        return user
