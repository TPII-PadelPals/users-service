from fastapi import APIRouter, Depends

from app.api.routes import google, items, items_service, users
from app.utilities.dependencies import get_token_header

api_router_open = APIRouter()
api_router_open.include_router(google.router, prefix="/google", tags=["google"])

api_router_token = APIRouter(
    dependencies=[Depends(get_token_header)],
)
api_router_token.include_router(users.router, prefix="/users", tags=["users"])
api_router_token.include_router(items.router, prefix="/items", tags=["items"])
api_router_token.include_router(
    items_service.router, prefix="/items-service", tags=["items-service"]
)
