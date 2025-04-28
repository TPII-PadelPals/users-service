import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.models.user import UserCreate
from app.services.players_service import PlayersService
from app.tests.utils.users import mock_call_player_create

async def test_login_success(async_client: AsyncClient, session, monkeypatch):
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    user_data = {
        "email": "testuser@example.com",
        "password": "testpass",
        "name": "Test User",
        "phone": "1234567890",
        "telegram_id": "1234567890",
    }
    await async_client.post(
        f"{settings.API_V1_STR}/users/",
        json=user_data,
        headers={"x-api-key": settings.API_KEY},
    )
    login_data = {"email": user_data["email"], "password": user_data["password"]}
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        json=login_data,
        headers={"x-api-key": settings.API_KEY},
    )
    assert response.status_code == 200
    content = response.json()
    assert "uuid" in content

async def test_login_invalid_credentials(async_client: AsyncClient, session, monkeypatch):
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    user_data = {
        "email": "testuser2@example.com",
        "password": "testpass",
        "name": "Test User2",
        "phone": "1234567891",
        "telegram_id": "1234567891",
    }
    await async_client.post(
        f"{settings.API_V1_STR}/users/",
        json=user_data,
        headers={"x-api-key": settings.API_KEY},
    )
    # Login with wrong password
    login_data = {"email": user_data["email"], "password": "wrongpass"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        json=login_data,
        headers={"x-api-key": settings.API_KEY},
    )
    assert response.status_code == 401
    content = response.json()
    assert content["detail"] == "Invalid credentials"
