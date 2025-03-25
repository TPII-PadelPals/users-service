import uuid

from httpx import AsyncClient

from app.core.config import settings


async def test_handshake_public_key(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = uuid.uuid4()
    public_user_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w...24vbBqIm0bf/oM\nZGVcyI6SERqpW39G33c87KX+CyhtlM+k/Fez+elo9nQiHDDjcfcYMZ6GrN5u/kgW\nnQIDAQAB\n-----END PUBLIC KEY-----\n"
    header = {
        "user_public_id": str(user_public_id),
        **x_api_key_header,
        "user_key": public_user_key,
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/authentication/public_key/{user_public_id}/",
        headers=header,
        json={"key": public_user_key},
    )
    assert response.status_code == 201
    content = response.json()
    assert content.get("key") is not None


async def test_new_token(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = uuid.uuid4()
    header = {"user_public_id": str(user_public_id), **x_api_key_header}
    response = await async_client.post(
        f"{settings.API_V1_STR}/authentication/token/{user_public_id}",
        headers=header,
        json={"token": "<PASSWORD>"},
    )
    assert response.status_code == 201
    content = response.json()
    assert content.get("token") is not None


async def test_validate_token(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = uuid.uuid4()
    public_user_key = "<PUBLIC USER KEY>"
    header_get = {
        "user_public_id": str(user_public_id),
        **x_api_key_header,
        "user_key": public_user_key,
    }
    response_get_1 = await async_client.post(
        f"{settings.API_V1_STR}/authentication/public_key/{user_public_id}/",
        headers=header_get,
        json={"key": public_user_key},
    )
    assert response_get_1.status_code == 201
    public_key = response_get_1.json().get("key")
    assert public_key is not None

    user_public_id_2 = uuid.uuid4()
    header_get_2 = {
        "user_public_id": str(user_public_id_2),
        **x_api_key_header,
        "user_key": public_key,
    }
    response_get_2 = await async_client.post(
        f"{settings.API_V1_STR}/authentication/public_key/{user_public_id_2}/",
        headers=header_get_2,
        json={"key": public_key},
    )
    assert response_get_2.status_code == 201

    header_post = {"user_public_id": str(user_public_id_2), **x_api_key_header}
    response_post = await async_client.post(
        f"{settings.API_V1_STR}/authentication/token/{user_public_id_2}",
        headers=header_post,
        json={"token": "<PASSWORD>"},
    )
    assert response_post.status_code == 201
    token = response_post.json().get("token")
    assert token is not None

    header_validate = {
        "user_public_id": str(user_public_id_2),
        **x_api_key_header,
        "token": token,
    }
    response = await async_client.get(
        f"{settings.API_V1_STR}/authentication/token/{user_public_id_2}/validate/{token}",
        headers=header_validate,
    )
    print(response.json())
    assert response.status_code == 200
    content = response.json()
    assert content.get("sub") is not None
    assert content.get("exp") is not None
    assert content.get("iat") is not None
