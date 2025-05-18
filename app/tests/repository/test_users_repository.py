import uuid

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import UserCreate
from app.repository.users_repository import UsersRepository
from app.services.players_service import PlayersService
from app.tests.utils.users import mock_call_player_create
from app.utilities.exceptions import NotFoundException, NotUniqueException


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


async def test_create_user_may_contain_telegram_id(session: AsyncSession) -> None:
    repo = UsersRepository(session)
    user_create = UserCreate(
        name="Name Surname", email="name-1@domain.com", phone="11 1111 1111"
    )
    user = await repo.create_user(user_create)
    assert user.telegram_id is None

    user_create = UserCreate(
        name="Name Surname",
        email="name-2@domain.com",
        phone="11 1111 2222",
        telegram_id=123456789,
    )
    user = await repo.create_user(user_create)
    assert user.telegram_id == user_create.telegram_id


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

    assert e.value.detail == "Email ya existe"


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

    assert e.value.detail == "Teléfono ya existe"


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
    with pytest.raises(NotFoundException):
        await repo.get_user(uuid.uuid4())


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
    users_got, users_count = await repo.get_users(skip=skip, limit=limit)
    users_got = sorted(users_got, key=lambda user: user.name)
    assert users_count == limit
    assert len(users_got) == limit
    for user_got, user_created in zip(
        users_got, users_created[skip : skip + limit], strict=False
    ):
        assert user_got.id == user_created.id
        assert user_got.public_id == user_created.public_id


async def test_get_user_by_email_found(session, monkeypatch):
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)
    user_data = {
        "email": "repo-test@example.com",
        "password": "testpass",
        "name": "Repo Test",
        "phone": "1234567899",
        "telegram_id": "1234567899",
    }
    from app.services.users_service import UsersService

    user_create = UserCreate(**user_data)
    user = await UsersService().create_user(session, user_create)
    repo = UsersRepository(session)
    found_user = await repo.get_user_by_email(user_data["email"])
    assert found_user.email == user_data["email"]
    assert found_user.public_id == user.public_id


async def test_get_user_by_email_not_found(session):
    repo = UsersRepository(session)
    with pytest.raises(Exception) as excinfo:
        await repo.get_user_by_email("notfound@example.com")
    assert "404: No se encontró el usuario" in str(excinfo.value)
