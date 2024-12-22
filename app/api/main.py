from fastapi import APIRouter, Depends

from app.api.routes import google, items, items_service, users
from app.utilities.dependencies import get_token_header

api_router_without_api_key = APIRouter()
api_router_without_api_key.include_router(
    google.router, prefix="/google", tags=["google"]
)

api_router_with_api_key = APIRouter(
    dependencies=[Depends(get_token_header)],
)
api_router_with_api_key.include_router(users.router, prefix="/users", tags=["users"])
api_router_with_api_key.include_router(items.router, prefix="/items", tags=["items"])
api_router_with_api_key.include_router(
    items_service.router, prefix="/items-service", tags=["items-service"]
)
