# import os
from typing import Any

from authlib.integrations.starlette_client import OAuth  # type: ignore
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

# from starlette.config import Config
from app.api.routes.users import _create_user
from app.core.config import settings
from app.models.user import UserCreate
from app.utilities.dependencies import SessionDep

router = APIRouter()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


async def google_auth_inner(request: Any, oauth: Any) -> Any:
    chat_id = request.query_params.get("chat_id")
    if not chat_id:
        raise HTTPException(status_code=400, detail="Chat ID is required")
    redirect_uri = request.url_for("google_auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri, state=chat_id)


@router.get("/auth")
async def google_auth(request: Request) -> Any:
    return await google_auth_inner(request, oauth)


@router.get("/auth/callback", response_class=HTMLResponse, name="google_auth_callback")
async def google_auth_callback(request: Request, session: SessionDep) -> Any:
    # chat_id = request.query_params.get("state")
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]
    user_create = UserCreate(
        # chat_id=chat_id,
        name=user_info["name"],
        email=user_info["email"],
        phone="",
    )
    try:
        await _create_user(session, user_create)
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
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
