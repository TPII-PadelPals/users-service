import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.user import UserCreate, UserPublic
from app.repository.users_repository import UsersRepository
from app.utilities.dependencies import SessionDep
from app.utilities.messages import NOT_ENOUGH_PERMISSIONS

router = APIRouter()


@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
)
async def create_item(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new item.
    """
    repo = UsersRepository(session)
    user = await repo.create_user(user_in)
    return user


@router.get(
    "/{id}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
)
async def read_user(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get item by ID.
    """
    repo = UsersRepository(session)
    user = await repo.get_user(id)
    return user
