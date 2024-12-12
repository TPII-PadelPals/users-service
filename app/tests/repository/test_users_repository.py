from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import UserCreate
from app.repository.users_repository import UsersRepository


async def test_create_business(session: AsyncSession) -> None:
    repo = UsersRepository(session)
    user_create = UserCreate(
        name="Name Surname", email="name@domain.com", phone="11 1234 5678"
    )

    user = await repo.create_user(user_create)

    assert user.name == user_create.name
    assert user.email == user_create.email
    assert user.phone == user_create.phone
