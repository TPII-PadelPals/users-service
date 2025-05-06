from typing import Any

from fastapi import Request

from app.core.config import settings
from app.models.user import UserCreate
from app.services.users_service import UsersService
from app.utilities.dependencies import SessionDep


class GoogleService:
    AUTH_CALLBACK_MSG = f"""
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

    def __init__(self, oauth: Any):
        self.name = "google-service"
        self.oauth = oauth
        self.users_service = UsersService()

    async def auth(self, request: Request, telegram_id: int) -> Any:
        redirect_uri = request.url_for("google_auth_callback")
        return await self.oauth.google.authorize_redirect(
            request, redirect_uri, state=telegram_id
        )

    async def auth_callback(self, request: Request, session: SessionDep) -> str:
        telegram_id = request.query_params.get("state")
        token = await self.oauth.google.authorize_access_token(request)
        user_info = token["userinfo"]
        user_create = UserCreate(
            name=user_info["name"],
            email=user_info["email"],
            phone=None,
            telegram_id=telegram_id,
        )

        await self.users_service.create_user(session, user_create)
        return self.AUTH_CALLBACK_MSG
