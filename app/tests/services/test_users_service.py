from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.password import Password
from app.models.user import UserCreate
from app.services.players_service import PlayersService
from app.services.users_service import UsersService
from app.tests.utils.users import mock_call_player_create


async def test_save_password(session: AsyncSession, monkeypatch: Any) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)
    data_user = {
        "email": "hola@gmail.com.ar",
        "password": "<PASSWORD>",
        "name": "<NAME>",
        "phone": "1234567890",
        "telegram_id": "1234567890",
    }
    user_create = UserCreate(**data_user)
    service = UsersService()
    user = await service.create_user(session, user_create)
    user_public_id = user.public_id

    statement = select(Password).where(Password.user_public_id == user_public_id)
    result = await session.exec(statement)
    password = result.first()
    assert password is not None
    assert password.password_hash == "<PASSWORD>"
    assert password.user_public_id == user_public_id


async def test_not_save_empty_password(session: AsyncSession, monkeypatch: Any) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)
    data_user = {
        "email": "hola@gmail.com.ar",
        "password": "",
        "name": "<NAME>",
        "phone": "1234567890",
        "telegram_id": "1234567890",
    }
    user_create = UserCreate(**data_user)
    service = UsersService()
    user = await service.create_user(session, user_create)
    user_public_id = user.public_id

    statement = select(Password).where(Password.user_public_id == user_public_id)
    result = await session.exec(statement)
    password = result.first()
    assert password is None
