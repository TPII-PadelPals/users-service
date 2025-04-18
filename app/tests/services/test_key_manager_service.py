from app.services.key_manager_service import KeyManagerService


async def test_new_key_manager() -> None:
    key_manager = KeyManagerService()
    assert key_manager is not None
    assert key_manager.serialize_public_key() is not None


async def test_key_manager_add_public_key() -> None:
    key_manager = KeyManagerService()
    user_email = "usuario@email.com"
    new_key = key_manager.serialize_public_key()
    assert new_key is not None
    key_manager.add_public_key(user_email, new_key)
    key = key_manager.get_public_key(user_email)
    assert key is not None
    assert key == new_key
