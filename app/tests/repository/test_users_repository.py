import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import UserCreate
from app.repository.users_repository import UsersRepository


async def test_create_user(session: AsyncSession) -> None:
    repo = UsersRepository(session)
    user_create = UserCreate(
        name="Name Surname", email="name@domain.com", phone="11 1234 5678"
    )

    user = await repo.create_user(user_create)

    assert len(str(user.public_id)) == len(str(uuid.uuid4()))
    assert user.name == user_create.name
    assert user.email == user_create.email
    assert user.phone == user_create.phone


async def test_create_user_id_autoincremental(session: AsyncSession) -> None:
    repo = UsersRepository(session)
    last_user_id = 0
    for _ in range(3):
        user_create = UserCreate(
            name="Name Surname", email="name@domain.com", phone="11 1234 5678"
        )
        user = await repo.create_user(user_create)
        assert user.id > last_user_id  # type: ignore[operator]
        last_user_id = user.id  # type: ignore[assignment]
