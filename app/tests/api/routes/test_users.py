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
    assert content["name"] == data["name"]
    assert content["email"] == data["email"]
    assert content["phone"] == data["phone"]
    assert "id" in content
