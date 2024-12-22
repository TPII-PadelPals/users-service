from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.routes.google import google_auth_callback_inner, google_auth_inner
from app.core.config import settings
from app.repository.users_repository import UsersRepository


async def test_google_auth_inner(mocker: Any) -> None:
    chat_id = "123456789"
    redirect_uri = "/google/auth/callback"
    request_mock = mocker.Mock()
    request_mock.url_for = (
        lambda key: redirect_uri if key == "google_auth_callback" else None
    )
    oauth_mock = mocker.Mock()
    oauth_mock.google = mocker.Mock()
    oauth_mock.google.authorize_redirect = mocker.AsyncMock()

    await google_auth_inner(request_mock, chat_id, oauth_mock)

    oauth_mock.google.authorize_redirect.assert_called_once_with(
        request_mock, redirect_uri, state=chat_id
    )


async def test_google_auth_callback_inner(session: AsyncSession, mocker: Any) -> None:
    chat_id = "123456789"
    user_info = {
        "name": "Name Surname",
        "email": "name@domain.com",
    }
    token = {"userinfo": user_info}
    request_mock = mocker.Mock()
    request_mock.query_params = mocker.Mock()
    request_mock.query_params.get = lambda key: chat_id if key == "state" else None

    oauth_mock = mocker.Mock()
    oauth_mock.google = mocker.Mock()
    oauth_mock.google.authorize_access_token = mocker.AsyncMock(
        side_effect=lambda request: token if request == request_mock else None
    )

    result_html = await google_auth_callback_inner(request_mock, session, oauth_mock)

    expected_html = f"""
    <html>
        <head>
            <title>Registro exitoso</title>
        </head>
        <body>
            <h1>Registro exitoso!</h1>
            <button onclick="window.location.href='{settings.TELEGRAM_PATH}'">Volver a telegram</button>
        </body>
    </html>
    """

    assert result_html == expected_html

    users_repo = UsersRepository(session)
    users, _ = await users_repo.get_users()
    user = users[0]

    assert user.name == user_info["name"]
    assert user.email == user_info["email"]
    assert user.phone == ""
    assert user.telegram_id == chat_id
