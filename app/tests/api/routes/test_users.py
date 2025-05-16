import uuid
from typing import Any

from httpx import AsyncClient, Response

from app.core.config import settings
from app.services.players_service import PlayersService
from app.tests.utils.users import (
    mock_call_player_create,
    mock_call_player_create_raise_exception,
)


async def _create_user(
    async_client: AsyncClient,
    name: str,
    email: str,
    phone: str,
    x_api_key: dict[str, str],
) -> tuple[Response, dict[str, str]]:
    data = {
        "name": name,
        "email": email,
        "phone": phone,
    }

    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key, json=data
    )
    return (response, data)


async def test_create_user(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    data = {"name": "Name Surname", "email": "name@domain.com", "phone": "11 1234 1234"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 201
    content = response.json()
    assert "public_id" in content
    assert content["name"] == data["name"]
    assert content["email"] == data["email"]
    assert content["phone"] == data["phone"]


async def test_create_user_raises_external_service_exception(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(
        PlayersService, "create_player", mock_call_player_create_raise_exception
    )

    data = {"name": "Name Surname", "email": "name@domain.com", "phone": "11 1234 1234"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 500
    content = response.json()
    assert content["detail"] == "EXT_SERVICE:external-service:error"
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] == 0


async def test_create_user_name_min_length_is_1(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    name = ""
    data = {"name": name, "email": "name@domain.com", "phone": "11 1111 1111"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["loc"] == ["body", "name"]
    assert (
        content["detail"][0]["msg"]
        == "Value error, La cadena debe tener al menos 1 caracter"
    )


async def test_create_user_name_max_length_is_255(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    name = "a" * 256
    data = {"name": name, "email": "name@domain.com", "phone": "11 1111 1111"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["loc"] == ["body", "name"]
    assert (
        content["detail"][0]["msg"]
        == "Value error, La cadena debe tener como máximo 255 caracteres"
    )


async def test_create_user_email_already_exists_responds_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    duplicated_email = "name@domain.com"
    data = {"name": "Name Surname", "email": duplicated_email, "phone": "11 1111 1111"}
    await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    data = {"name": "Name Surname", "email": duplicated_email, "phone": "22 2222 2222"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 409
    content = response.json()
    assert content["detail"] == "Email ya existe"


async def test_create_user_phone_already_exists_responds_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    duplicated_phone = "11 1234 1234"
    data = {
        "name": "Name Surname",
        "email": "name-1@domain.com",
        "phone": duplicated_phone,
    }
    await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    data = {
        "name": "Name Surname",
        "email": "name-2@domain.com",
        "phone": duplicated_phone,
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 409
    content = response.json()
    assert content["detail"] == "Teléfono ya existe"


async def test_create_user_with_email_without_at_symbol_returns_error(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    response, _data = await _create_user(
        async_client,
        name="Roberto",
        email="abbondanzierigmail.com",
        phone="1124575700",
        x_api_key=x_api_key_header,
    )

    assert response.status_code == 422
    content = response.json()

    assert content["detail"] == "Formato de email inválido."


async def test_create_user_with_email_without_domain_returns_error(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    response, _data = await _create_user(
        async_client,
        name="Roberto",
        email="abbondanzieri@.com",
        phone="1124575700",
        x_api_key=x_api_key_header,
    )

    assert response.status_code == 422
    content = response.json()

    assert content["detail"] == "Formato de email inválido."


async def test_create_user_with_email_without_extension_returns_error(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    response, _data = await _create_user(
        async_client,
        name="Roberto",
        email="abbondanzieri@domain.",
        phone="1124575700",
        x_api_key=x_api_key_header,
    )

    assert response.status_code == 422
    content = response.json()

    assert content["detail"] == "Formato de email inválido."


async def test_create_user_with_email_with_multiple_extension_on_email(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    response, data = await _create_user(
        async_client,
        name="Roberto",
        email="abbondanzieri@yahoo.com.ar",
        phone="1124575700",
        x_api_key=x_api_key_header,
    )

    assert response.status_code == 201
    content = response.json()

    assert "public_id" in content
    assert content["name"] == data["name"]
    assert content["email"] == data["email"]
    assert content["phone"] == data["phone"]


async def test_read_user(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    data = {"name": "Name Surname", "email": "name@domain.com", "phone": "11 1234 1234"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    content = response.json()
    user_id = content["public_id"]

    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=x_api_key_header
    )
    assert response.status_code == 200
    content = response.json()
    assert content["public_id"] == user_id
    assert content["name"] == data["name"]
    assert content["email"] == data["email"]
    assert content["phone"] == data["phone"]


async def test_read_user_not_found(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_id = uuid.uuid4()
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=x_api_key_header
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "No se encontró el usuario"


async def test_read_user_not_authorized(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    data = {"name": "Name Surname", "email": "name@domain.com", "phone": "11 1234 1234"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    content = response.json()
    user_id = content["public_id"]

    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers={"x-api-key": "wrong-key"},
    )
    assert response.status_code == 401
    content = response.json()
    assert content["detail"] == "No autorizado"


async def test_read_users(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    users_data = []
    for i in range(2):
        data = {
            "name": f"Name {i}",
            "email": f"name-{i}@domain.com",
            "phone": f"{i}{i} {i}{i}{i}{i} {i}{i}{i}{i}",
        }
        response = await async_client.post(
            f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
        )
        users_data.append(response.json())

    response = await async_client.get(
        f"{settings.API_V1_STR}/users/",
        headers=x_api_key_header,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] == 2
    assert len(content["data"]) == 2
    users = sorted(content["data"], key=lambda user: user["name"])
    for user, user_data in zip(users, users_data, strict=False):
        assert user["public_id"] == user_data["public_id"]
        assert user["name"] == user_data["name"]
        assert user["email"] == user_data["email"]
        assert user["phone"] == user_data["phone"]


async def test_read_users_skip_limit(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    users_data = []
    for i in range(4):
        data = {
            "name": f"Name {i}",
            "email": f"name-{i}@domain.com",
            "phone": f"{i}{i} {i}{i}{i}{i} {i}{i}{i}{i}",
        }
        response = await async_client.post(
            f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
        )
        users_data.append(response.json())
    skip = 1
    limit = 2
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/",
        headers=x_api_key_header,
        params={"skip": skip, "limit": limit},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] == limit
    assert len(content["data"]) == limit
    users = sorted(content["data"], key=lambda user: user["name"])
    for user, user_data in zip(users, users_data[skip : skip + limit], strict=False):
        assert user["public_id"] == user_data["public_id"]
        assert user["name"] == user_data["name"]
        assert user["email"] == user_data["email"]
        assert user["phone"] == user_data["phone"]


async def test_read_users_skip_limit_defaults(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    limit = 100
    users_data = []
    for i in range(200):
        data = {
            "name": f"Name {i}",
            "email": f"name-{i}@domain.com",
            "phone": f"11 1111 {i:04}",
        }
        response = await async_client.post(
            f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
        )
        users_data.append(response.json())
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] == limit
    assert len(content["data"]) == limit
    for user in content["data"]:
        assert user in users_data


async def test_read_users_telegram_id(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    users_data = []
    for i in range(4):
        data = {
            "name": f"Name {i}",
            "email": f"name-{i}@domain.com",
            "phone": f"{i}{i} {i}{i}{i}{i} {i}{i}{i}{i}",
            "telegram_id": i,
        }
        response = await async_client.post(
            f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
        )
        users_data.append(response.json())
    telegram_id = 0
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/",
        headers=x_api_key_header,
        params={"telegram_id": telegram_id},
    )
    assert response.status_code == 200

    content = response.json()
    users = content["data"]
    users_count = content["count"]

    assert users_count == 1

    user = users[0]
    user_data = users_data[0]

    assert user["public_id"] == user_data["public_id"]
    assert user["name"] == user_data["name"]
    assert user["email"] == user_data["email"]
    assert user["phone"] == user_data["phone"]
    assert user["telegram_id"] == user_data["telegram_id"]


async def test_create_user_whit_password(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    data = {
        "name": "Name Surname",
        "email": "name@domain.com",
        "phone": "11 1234 1234",
        "password": "<PASSWORD>",
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 201
    content = response.json()
    assert "public_id" in content
    assert content["name"] == data["name"]
    assert content["email"] == data["email"]
    assert content["phone"] == data["phone"]


async def test_create_user_whit_empty_password(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)

    data = {
        "name": "Name Surname",
        "email": "name@domain.com",
        "phone": "11 1234 1234",
        "password": "",
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 201
    content = response.json()
    assert "public_id" in content
    assert content["name"] == data["name"]
    assert content["email"] == data["email"]
    assert content["phone"] == data["phone"]
