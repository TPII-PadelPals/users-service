from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.sessions import SessionMiddleware

from app.api.main import api_router_with_api_key, api_router_without_api_key
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


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = []
    for err in errors:
        msg = err.get("msg", "")
        if msg.lower().startswith("value error,"):
            msg = msg[len("value error,"):].strip()
        custom_errors.append({
            "loc": err.get("loc")[-1],
            "msg": msg,
            "input": err.get("input"),
        })
    return JSONResponse(
        status_code=422,
        content={"detail": custom_errors}
    )

# Add the SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.MIDDLEWARE_KEY)

# Register routes
app.include_router(api_router_without_api_key, prefix=settings.API_V1_STR)
app.include_router(api_router_with_api_key, prefix=settings.API_V1_STR)
