from typing import Any
from app.models.login import LoginRequest, LoginResponse
from app.services.auth_service import AuthService
from app.utilities.dependencies import SessionDep
from fastapi import APIRouter, status
from app.utilities.messages import LOGIN_RESPONSES

router = APIRouter()
service = AuthService()

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses={**LOGIN_RESPONSES},  # type: ignore[dict-item]
)
async def create_user(*, request: LoginRequest, session: SessionDep) -> Any:
    """
    User login.
    """
    return await service.login(session, request)