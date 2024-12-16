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


async def test_create_user_name_min_length_is_1(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    name = ""
    data = {"name": name, "email": "name@domain.com", "phone": "11 1111 1111"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["loc"] == ["body", "name"]
    assert content["detail"][0]["msg"] == "String should have at least 1 character"


async def test_create_user_name_max_length_is_255(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    name = "a" * 256
    data = {"name": name, "email": "name@domain.com", "phone": "11 1111 1111"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/users/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["loc"] == ["body", "name"]
    assert content["detail"][0]["msg"] == "String should have at most 255 characters"


async def test_create_user_email_already_exists_responds_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
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
    assert content["detail"] == "Email already exists"


async def test_create_user_phone_already_exists_responds_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
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
    assert content["detail"] == "Phone already exists"


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
        assert user["name"] == user_data["name"]
        assert user["email"] == user_data["email"]
        assert user["phone"] == user_data["phone"]


async def test_read_users_skip_limit(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
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
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    skip = 0
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
    users = sorted(content["data"], key=lambda user: user["name"])
    assert users[0]["public_id"] == users_data[skip]["public_id"]
    assert users[-1]["public_id"] == users_data[limit - 1]["public_id"]
