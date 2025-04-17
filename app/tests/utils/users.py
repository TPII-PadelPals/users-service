from app.utilities.exceptions import ExternalServiceException


async def mock_call_player_create(_self, user_public_id):  # noqa: ARG001
    return None


async def mock_call_player_create_raise_exception(_self, user_public_id):  # noqa: ARG001
    raise ExternalServiceException("external-service", "error")
