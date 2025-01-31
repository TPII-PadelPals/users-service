import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.user import UserCreate, UserPublic, UsersPublic
from app.services.players_service import PlayersService
from app.services.users_service import UsersService
from app.utilities.context_managers import (
    service_and_repository_error_handler,
)
from app.utilities.dependencies import SessionDep
from app.utilities.messages import (
    GET_USER_RESPONSES,
    GET_USERS_RESPONSES,
    POST_USERS_RESPONSES,
)

router = APIRouter()

service = UsersService()


@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**POST_USERS_RESPONSES},  # type: ignore[dict-item]
)
async def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    async with service_and_repository_error_handler(session):
        created_user = await service.create_user(session, user_in)
        created_user_dict = created_user.model_dump()
        await PlayersService().create_player(
            user_public_id=created_user_dict.get("public_id"),
            telegram_id=created_user_dict.get("telegram_id"),
        )
        return created_user


@router.get(
    "/",
    response_model=UsersPublic,
    status_code=status.HTTP_200_OK,
    responses={**GET_USERS_RESPONSES},  # type: ignore[dict-item]
)
async def read_users(
    session: SessionDep, telegram_id: str | None = None, skip: int = 0, limit: int = 100
) -> Any:  #
    """
    Retrieve users.
    """
    return await service.read_users(session, telegram_id, skip, limit)


@router.get(
    "/{id}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    responses={**GET_USER_RESPONSES},  # type: ignore[dict-item]
)
async def read_user(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get user by public ID.
    """
    return await service.read_user(session, id)
