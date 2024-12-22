from app.models.user import User, UserCreate
from app.repository.users_repository import UsersRepository
from app.utilities.dependencies import SessionDep


class UsersService:
    async def create_user(self, session: SessionDep, user_in: UserCreate) -> User:
        repo = UsersRepository(session)
        user = await repo.create_user(user_in)
        return user
