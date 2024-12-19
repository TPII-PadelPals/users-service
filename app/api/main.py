from fastapi import APIRouter

from app.api.routes import google, items, items_service, users

api_router = APIRouter()
api_router.include_router(google.router, prefix="/google", tags=["google"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(
    items_service.router, prefix="/items-service", tags=["items-service"]
)
