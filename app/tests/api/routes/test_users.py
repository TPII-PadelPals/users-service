import uuid

from httpx import AsyncClient

from app.core.config import settings


async def test_create_user(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
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


async def test_read_user(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
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
    assert content["detail"] == "User not found"


async def test_read_user_not_authorized(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
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
    assert content["detail"] == "Not Authorized"


async def test_read_users(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
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
