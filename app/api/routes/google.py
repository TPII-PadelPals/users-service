from typing import Any

from authlib.integrations.starlette_client import OAuth  # type: ignore
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

from app.api.routes.users import create_user_inner
from app.core.config import settings
from app.models.user import UserCreate
from app.utilities.dependencies import SessionDep
from app.utilities.messages import GOOGLE_RESPONSES

router = APIRouter()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get(
    "/auth",
    status_code=status.HTTP_200_OK,
    responses={**GOOGLE_RESPONSES},  # type: ignore[dict-item]
)
async def google_auth(request: Request, chat_id: str) -> Any:
    return await google_auth_inner(request, chat_id, oauth)


async def google_auth_inner(request: Any, chat_id: str, oauth: Any) -> Any:
    redirect_uri = request.url_for("google_auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri, state=chat_id)


@router.get("/auth/callback", response_class=HTMLResponse, name="google_auth_callback")
async def google_auth_callback(request: Request, session: SessionDep) -> Any:
    return await google_auth_callback_inner(request, session, oauth)


async def google_auth_callback_inner(
    request: Any, session: SessionDep, oauth: Any
) -> Any:
    chat_id = request.query_params.get("state")
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]
    user_create = UserCreate(
        name=user_info["name"],
        email=user_info["email"],
        phone="",
        telegram_id=chat_id,
    )
    await create_user_inner(session, user_create)
    button_onclick = f"window.location.href='{settings.TELEGRAM_PATH}'"
    return f"""
    <html>
        <head>
            <title>Registro exitoso</title>
        </head>
        <body>
            <h1>Registro exitoso!</h1>
            <button onclick="{button_onclick}">Volver a telegram</button>
        </body>
    </html>
    """
