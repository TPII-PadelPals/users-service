import uuid

from httpx import AsyncClient

from app.core.config import settings


async def test_get_key(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = uuid.uuid4()
    public_user_key = "<PUBLIC USER KEY>"
    header = {"user_public_id": str(user_public_id), **x_api_key_header}
    response = await async_client.get(
        f"{settings.API_V1_STR}/authentication/public_key/{user_public_id}/{public_user_key}",
        headers=header,
    )
    assert response.status_code == 200


# async def test_new_token(
#         async_client: AsyncClient, x_api_key_header: dict[str, str]
# ) -> None:
#     user_public_id = uuid.uuid4()
#     public_user_key = "<PUBLIC USER KEY>"
#     header = {"user_public_id": str(user_public_id), **x_api_key_header}
#     response = await async_client.get(
#         f"{settings.API_V1_STR}/authentication/public_key/{user_public_id}/{public_user_key}",
#         headers=header,
#     )
#     assert response.status_code == 200


# async def test_new_token_not_found_key_404(
#         async_client: AsyncClient, x_api_key_header: dict[str, str]
# ) -> None:
#     token =
#
#
#     user_public_id = uuid.uuid4()
#     data = {
#         "token": "string"
#     }
#     header = {"user_public_id": str(user_public_id), **x_api_key_header}
#     response = await async_client.post(
#         f"{settings.API_V1_STR}/authentication/token/{user_public_id}",
#         headers=header,
#         json=data,
#     )
#     assert response.status_code == 404

#
# async def test_validate_token(
#         async_client: AsyncClient, x_api_key_header: dict[str, str]
# ) -> None:
#     user_public_id = uuid.uuid4()
#     public_user_key = "<PUBLIC USER KEY>"
#     header = {"user_public_id": str(user_public_id), **x_api_key_header}
#     response = await async_client.get(
#         f"{settings.API_V1_STR}/authentication/public_key/{user_public_id}/{public_user_key}",
#         headers=header,
#     )
#     assert response.status_code == 200
