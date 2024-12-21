import uuid

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import UserCreate
from app.repository.users_repository import UsersRepository
from app.utilities.exceptions import (
    NotFoundException,
    NotUniqueException,
)


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
    for i in range(3):
        user_create = UserCreate(
            name="Name Surname", email=f"name-{i}@domain.com", phone=f"11 1111 111{i}"
        )
        user = await repo.create_user(user_create)
        assert user.id > last_user_id  # type: ignore[operator]
        last_user_id = user.id  # type: ignore[assignment]


async def test_create_user_email_already_exists_raises_exception(
    session: AsyncSession,
) -> None:
    repo = UsersRepository(session)

    email = "name@domain.com"

    user_create = UserCreate(name="Name Surname", email=email, phone="11 1111 1111")
    await repo.create_user(user_create)

    with pytest.raises(NotUniqueException) as e:
        user_create = UserCreate(name="Name Surname", email=email, phone="11 2222 2222")
        await repo.create_user(user_create)

    assert e.value.detail == "Email already exists"


async def test_create_user_phone_already_exists_raises_exception(
    session: AsyncSession,
) -> None:
    repo = UsersRepository(session)

    phone = "11 1111 1111"

    user_create = UserCreate(
        name="Name Surname", email="name-1@domain.com", phone=phone
    )
    await repo.create_user(user_create)

    with pytest.raises(NotUniqueException) as e:
        user_create = UserCreate(
            name="Name Surname", email="name-2@domain.com", phone=phone
        )
        await repo.create_user(user_create)

    assert e.value.detail == "Phone already exists"


async def test_get_user(session: AsyncSession) -> None:
    repo = UsersRepository(session)
    user_create = UserCreate(
        name="Name Surname", email="name@domain.com", phone="11 1234 5678"
    )

    user_created = await repo.create_user(user_create)
    user_got = await repo.get_user(user_created.public_id)

    assert user_got.id == user_created.id
    assert user_got.public_id == user_created.public_id
    assert user_got.name == user_create.name
    assert user_got.email == user_create.email
    assert user_got.phone == user_create.phone


async def test_get_user_not_found(session: AsyncSession) -> None:
    repo = UsersRepository(session)
    try:
        await repo.get_user(uuid.uuid4())
        raise ArithmeticError()
    except NotFoundException:
        assert True


async def test_get_users(session: AsyncSession) -> None:
    repo = UsersRepository(session)
    skip = 1
    limit = 2
    users_created = []
    for i in range(4):
        user_create = UserCreate(
            name=f"Name {i}", email=f"name-{i}@domain.com", phone=f"11 1111 {i:03}"
        )
        user_created = await repo.create_user(user_create)
        users_created.append(user_created)
    users_got, users_count = await repo.get_users(skip, limit)
    users_got = sorted(users_got, key=lambda user: user.name)
    assert users_count == limit
    assert len(users_got) == limit
    for user_got, user_created in zip(
        users_got, users_created[skip : skip + limit], strict=False
    ):
        assert user_got.id == user_created.id
        assert user_got.public_id == user_created.public_id
