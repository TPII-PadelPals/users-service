import pytest

from app.models.user import UserCreate


async def test_create_user_name_min_size_is_one() -> None:
    with pytest.raises(ValueError):
        UserCreate(name="", email="name@domain.com", phone="11 1234 5678")
