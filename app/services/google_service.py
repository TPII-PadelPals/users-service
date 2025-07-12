from typing import Any

from fastapi import Request
from jinja2 import Template

from app.core.config import settings
from app.models.user import UserCreate
from app.services.users_service import UsersService
from app.utilities.dependencies import SessionDep


class GoogleService:
    def __init__(self, oauth: Any):
        self.name = "google-service"
        self.oauth = oauth
        self.users_service = UsersService()

    @staticmethod
    def get_auth_callback_msg(telegram_url: str):
        with open("app/templates/welcome.html") as f:
            template = Template(f.read())
        return template.render(telegram_url=telegram_url)

    async def auth(self, request: Request, telegram_id: int) -> Any:
        redirect_uri = request.url_for("google_auth_callback")
        return await self.oauth.google.authorize_redirect(
            request, redirect_uri, state=telegram_id, prompt="select_account"
        )

    async def auth_callback(self, request: Request, session: SessionDep) -> str:
        telegram_id = request.query_params.get("state")
        token = await self.oauth.google.authorize_access_token(request)
        user_info = token["userinfo"]
        user_create = UserCreate(
            name=user_info["name"],
            email=user_info["email"],
            phone="",
            telegram_id=telegram_id,
        )

        await self.users_service.create_user(session, user_create)
        return self.get_auth_callback_msg(settings.TELEGRAM_BOT_URL)
