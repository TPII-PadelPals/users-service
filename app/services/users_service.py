import uuid

from app.models.user import User, UserCreate, UsersPublic
from app.repository.users_repository import UsersRepository
from app.services.players_service import PlayersService
from app.utilities.context_managers import service_and_repository_error_handler
from app.utilities.dependencies import SessionDep


class UsersService:
    async def create_user(self, session: SessionDep, user_in: UserCreate) -> User:
        async with service_and_repository_error_handler(session):
            repo = UsersRepository(session)
            user = await repo.create_user(user_in)
            user_dict = user.model_dump()
            await PlayersService().create_player(
                user_public_id=user_dict.get("public_id"),
                telegram_id=user_dict.get("telegram_id"),
            )
            await session.refresh(user)
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
