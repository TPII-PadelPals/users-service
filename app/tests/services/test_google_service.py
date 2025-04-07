from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from app.repository.users_repository import UsersRepository
from app.services.google_service import GoogleService
from app.services.players_service import PlayersService
from app.tests.utils.users import mock_call_player_create


async def test_google_service_auth(mocker: Any) -> None:
    telegram_id = 123456789
    redirect_uri = "/google/auth/callback"
    request_mock = mocker.Mock()
    request_mock.url_for = (
        lambda key: redirect_uri if key == "google_auth_callback" else None
    )
    oauth_mock = mocker.Mock()
    oauth_mock.google = mocker.Mock()
    oauth_mock.google.authorize_redirect = mocker.AsyncMock()

    service = GoogleService(oauth_mock)
    await service.auth(request_mock, telegram_id)

    oauth_mock.google.authorize_redirect.assert_called_once_with(
        request_mock, redirect_uri, state=telegram_id
    )


async def test_google_service_auth_callback(
    session: AsyncSession, mocker: Any, monkeypatch
) -> None:
    monkeypatch.setattr(PlayersService, "create_player", mock_call_player_create)
    telegram_id = 123456789
    user_info = {
        "name": "Name Surname",
        "email": "name@domain.com",
    }
    token = {"userinfo": user_info}
    request_mock = mocker.Mock()
    request_mock.query_params = mocker.Mock()
    request_mock.query_params.get = lambda key: telegram_id if key == "state" else None

    oauth_mock = mocker.Mock()
    oauth_mock.google = mocker.Mock()
    oauth_mock.google.authorize_access_token = mocker.AsyncMock(
        side_effect=lambda request: token if request == request_mock else None
    )

    service = GoogleService(oauth_mock)
    result_html = await service.auth_callback(request_mock, session)

    expected_html = GoogleService.AUTH_CALLBACK_MSG
    assert result_html == expected_html

    users_repo = UsersRepository(session)
    users, _ = await users_repo.get_users()
    user = users[0]

    assert user.name == user_info["name"]
    assert user.email == user_info["email"]
    assert user.phone == ""
    assert user.telegram_id == telegram_id
