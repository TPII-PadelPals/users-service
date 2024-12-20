from typing import Any

from app.api.routes.google import google_auth_inner


async def test_google_auth_inner(mocker: Any) -> None:
    chat_id = 123456789
    redirect_uri = "/google/auth/callback"
    request_mock = mocker.Mock()
    request_mock.query_params = mocker.Mock()
    request_mock.query_params.get = lambda key: chat_id if key == "chat_id" else None
    request_mock.url_for = (
        lambda key: redirect_uri if key == "google_auth_callback" else None
    )
    oauth_mock = mocker.Mock()
    oauth_mock.google = mocker.Mock()
    oauth_mock.google.authorize_redirect = mocker.AsyncMock()

    await google_auth_inner(request_mock, oauth_mock)

    oauth_mock.google.authorize_redirect.assert_called_once_with(
        request_mock, redirect_uri, state=chat_id
    )
