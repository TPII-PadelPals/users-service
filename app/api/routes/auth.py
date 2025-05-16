from typing import Any

from fastapi import APIRouter, status

from app.models.login import LoginRequest, LoginResponse
from app.models.user import UserCreate, UserPublic
from app.services.auth_service import AuthService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import (
    LOGIN_RESPONSES,
    POST_USERS_RESPONSES,
)

router = APIRouter()
auth_service = AuthService()


@router.post(
    "/signup",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**POST_USERS_RESPONSES},  # type: ignore[dict-item]
)
async def user_signup(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    User signup.
    """
    return await auth_service.signup(session, user_in)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses={**LOGIN_RESPONSES},  # type: ignore[dict-item]
)
async def user_login(*, request: LoginRequest, session: SessionDep) -> Any:
    """
    User login.
    """
    return await auth_service.login(session, request)
