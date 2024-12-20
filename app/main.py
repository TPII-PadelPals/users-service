from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.sessions import SessionMiddleware

from app.api.main import api_router_open, api_router_token
from app.core.config import settings
from app.core.db import init_db


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(_: FastAPI):  # type:ignore[no-untyped-def]
    # await restart_db()
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Add the SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.MIDDLEWARE_KEY)

# Register routes
app.include_router(api_router_open, prefix=settings.API_V1_STR)
app.include_router(api_router_token, prefix=settings.API_V1_STR)
