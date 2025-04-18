import uuid

from fastapi import APIRouter, status

from app.models.public_key import PublicKey
from app.models.token import Token, TokenPublic
from app.services.key_manager_service import KeyManagerService
from app.services.token_service import TokenService
from app.utilities.messages import (
    GET_VALIDATE_TOKEN_RESPONSES,
    POST_PUBLIC_KEY_RESPONSES,
    POST_TOKEN_RESPONSES,
)

router = APIRouter()

key_service = KeyManagerService()
token_service = TokenService()


@router.post(
    "/users/{user_email}/public_key",
    response_model=PublicKey,
    status_code=status.HTTP_201_CREATED,
    responses={**POST_PUBLIC_KEY_RESPONSES},  # type: ignore[dict-item]
)
async def handshake_public_key(*, user_email: str, user_key: PublicKey) -> PublicKey:
    key_service.add_public_key(user_email, user_key.key)
    response_key = key_service.serialize_public_key()
    return PublicKey.from_str(response_key)


@router.post(
    "/users/{user_public_id}/token",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    responses={**POST_TOKEN_RESPONSES},  # type: ignore[dict-item]
)
async def generate_token(*, user_public_id: uuid.UUID) -> Token:
    new_token = token_service.create_token(
        user_public_id, key_service.serialize_private_key()
    )
    return new_token


@router.get(
    "/users/{user_public_id}/token/{token}/validate",
    response_model=TokenPublic,
    status_code=status.HTTP_200_OK,
    responses={**GET_VALIDATE_TOKEN_RESPONSES},  # type: ignore[dict-item]
)
async def validate_token(*, user_public_id: uuid.UUID, token: str) -> TokenPublic:
    public_key = key_service.serialize_public_key()
    token_payload = token_service.validate_token(token, public_key, user_public_id)
    return token_payload
