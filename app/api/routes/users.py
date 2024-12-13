import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.user import UserCreate, UserPublic, UsersPublic
from app.repository.users_repository import UsersRepository
from app.utilities.dependencies import SessionDep
from app.utilities.messages import USER_RESPONSES

router = APIRouter()


@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**USER_RESPONSES},  # type: ignore[dict-item]
)
async def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new item.
    """
    repo = UsersRepository(session)
    user = await repo.create_user(user_in)
    return user


@router.get(
    "/",
    response_model=UsersPublic,
    status_code=status.HTTP_200_OK,
    responses={**USER_RESPONSES},  # type: ignore[dict-item]
)
async def read_users(session: SessionDep) -> Any:  # , skip: int = 0, limit: int = 100
    """
    Retrieve items.
    """
    repo = UsersRepository(session)
    users, count = await repo.get_users()  # , skip, limit
    return UsersPublic(data=users, count=count)


@router.get(
    "/{id}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    responses={**USER_RESPONSES},  # type: ignore[dict-item]
)
async def read_user(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get item by ID.
    """
    repo = UsersRepository(session)
    user = await repo.get_user(id)
    return user
