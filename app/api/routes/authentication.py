import uuid

from fastapi import APIRouter, status

from app.models.public_key import PublicKeyModel
from app.models.token import TokenModel, TokenPayload
from app.services.key_manager_service import KeyManagerService
from app.services.token_service import TokenService
from app.utilities.messages import (
    CREATE_TOKEN_RESPONSES,
    GET_PUBLIC_KEY_RESPONSES,
    GET_VALIDATE_TOKEN,
)

router = APIRouter()

key_service = KeyManagerService()
token_service = TokenService()


@router.post(
    "/public_key/{user_public_id}/",
    response_model=PublicKeyModel,
    status_code=status.HTTP_201_CREATED,
    responses={**GET_PUBLIC_KEY_RESPONSES},  # type: ignore[dict-item]
)
async def handshake_public_key(
    *, user_public_id: uuid.UUID, user_key: PublicKeyModel
) -> PublicKeyModel:
    key_service.add_public_key(user_public_id, user_key.key)
    response_key = key_service.serialize_public_key()
    return PublicKeyModel.from_str(response_key)


@router.post(
    "/token/{user_public_id}",
    response_model=TokenModel,
    status_code=status.HTTP_201_CREATED,
    responses={**CREATE_TOKEN_RESPONSES},  # type: ignore[dict-item]
)
async def generate_token(*, user_public_id: uuid.UUID) -> TokenModel:
    new_token = token_service.create_token(
        user_public_id, key_service.serialize_private_key()
    )
    return new_token


@router.get(
    "/token/{user_public_id}/validate/{token}",
    response_model=TokenPayload,
    status_code=status.HTTP_200_OK,
    responses={**GET_VALIDATE_TOKEN},  # type: ignore[dict-item]
)
async def validate_token(*, user_public_id: uuid.UUID, token: str) -> TokenPayload:
    public_key = key_service.get_public_key(user_public_id)
    token_payload = token_service.validation_token(token, public_key, user_public_id)
    return token_payload
