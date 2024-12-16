import pytest

from app.models.user import UserCreate


async def test_create_user_name_min_size_is_1() -> None:
    with pytest.raises(ValueError):
        name = ""
        UserCreate(name=name, email="name@domain.com", phone="11 1234 5678")


async def test_create_user_name_max_length_is_255() -> None:
    with pytest.raises(ValueError):
        name = "a" * 256
        UserCreate(name=name, email="name@domain.com", phone="11 1234 5678")
