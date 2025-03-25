import uuid

from app.services.key_manager_service import KeyManagerService
from app.services.token_service import TokenService


def test_token_service() -> None:
    owner_id = uuid.uuid4()
    key_service = KeyManagerService()
    token_service = TokenService()

    token = token_service.create_token(owner_id, key_service.serialize_private_key())
    assert token is not None
    payload = token_service.validation_token(
        token.token, key_service.serialize_public_key(), owner_id
    )
    assert payload is not None
    assert payload.is_owner_public_id_in_sub(owner_id)
    assert payload.sub == str(owner_id)
