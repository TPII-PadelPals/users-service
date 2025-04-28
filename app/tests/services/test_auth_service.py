import pytest

from app.models.login import LoginRequest
from app.services.auth_service import AuthService
from app.services.players_service import PlayersService
from app.tests.utils.users import mock_call_player_create


async def test_login_success(session, monkeypatch):
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)
    user_data = {
        "email": "testuser@example.com",
        "password": "testpass",
        "name": "Test User",
        "phone": "1234567890",
        "telegram_id": "1234567890",
    }
    from app.models.user import UserCreate
    from app.services.users_service import UsersService

    user_create = UserCreate(**user_data)
    await UsersService().create_user(session, user_create)
    # Try login
    service = AuthService()
    request = LoginRequest(email=user_data["email"], password=user_data["password"])
    response = await service.login(session, request)
    assert response.uuid is not None


async def test_login_invalid_password(session, monkeypatch):
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)
    user_data = {
        "email": "testuser2@example.com",
        "password": "testpass",
        "name": "Test User2",
        "phone": "1234567891",
        "telegram_id": "1234567891",
    }
    from app.models.user import UserCreate
    from app.services.users_service import UsersService

    user_create = UserCreate(**user_data)
    await UsersService().create_user(session, user_create)
    service = AuthService()
    request = LoginRequest(email=user_data["email"], password="wrongpass")
    with pytest.raises(Exception) as excinfo:
        await service.login(session, request)
    assert "Invalid credentials" in str(excinfo.value)
