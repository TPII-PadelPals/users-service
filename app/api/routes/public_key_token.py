import uuid

from fastapi import APIRouter, status

from app.models.token import PublicKeyModel
from app.services.key_manager_service import KeyManagerService
from app.utilities.messages import CREATE_TOKEN_RESPONSES, GET_PUBLIC_KEY_RESPONSES

router = APIRouter()

service = KeyManagerService()


@router.get(
    "/public_key/{user_public_id}",
    response_model=PublicKeyModel,
    status_code=status.HTTP_200_OK,
    responses={**GET_PUBLIC_KEY_RESPONSES},
)
async def get_public_key(*, user_public_id: uuid.UUID, user_key: PublicKeyModel):
    service.add_public_key(user_public_id, user_key.key)
    response_key = service.serialize_public_key()
    return PublicKeyModel.from_str(response_key)


@router.post(
    "/token/",
    response_model=PublicKeyModel,
    status_code=status.HTTP_201_CREATED,
    responses={**CREATE_TOKEN_RESPONSES},
)
async def generate_token():
    return ""
