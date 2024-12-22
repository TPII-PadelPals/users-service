from typing import Any

from authlib.integrations.starlette_client import OAuth  # type: ignore
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.services.google_service import GoogleService
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

service = GoogleService(oauth)


@router.get("/auth", status_code=status.HTTP_200_OK)
async def google_auth(request: Request, telegram_id: str) -> Any:
    return await service.auth(request, telegram_id)


@router.get("/auth/callback", response_class=HTMLResponse, name="google_auth_callback")
async def google_auth_callback(request: Request, session: SessionDep) -> Any:
    return await service.auth_callback(request, session)
