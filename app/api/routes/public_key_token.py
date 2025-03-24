import uuid

from fastapi import APIRouter, status

from app.services.key_manager_service import KeyManagerService
from app.utilities.messages import GET_PUBLIC_KEY_RESPONSES

router = APIRouter()

service = KeyManagerService()


@router.get(
    "/{user_public_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    responses={**GET_PUBLIC_KEY_RESPONSES},
)
async def get_public_key(*, user_public_id: uuid.UUID, user_key: str):
    service.add_public_key(user_public_id, user_key)
    return service.serialize_public_key()


@router.post("/")
async def generate_token():
    return ""
