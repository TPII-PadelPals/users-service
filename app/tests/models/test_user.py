import pytest

from app.models.user import UserCreate
from app.utilities.exceptions import InvalidEmailHttpException


async def test_create_user_name_min_size_is_1() -> None:
    with pytest.raises(ValueError):
        name = ""
        UserCreate(name=name, email="name@domain.com", phone="11 1234 5678")


async def test_create_user_name_max_length_is_255() -> None:
    with pytest.raises(ValueError):
        name = "a" * 256
        UserCreate(name=name, email="name@domain.com", phone="11 1234 5678")


async def test_create_user_without_at_symbol_on_email_raises_error() -> None:
    with pytest.raises(InvalidEmailHttpException) as e:
        UserCreate(name="Robert", email="name_without_at.com", phone="11 1234 5678")

    assert e.value.detail == "Invalid email format."


async def test_create_user_without_domain_on_email_raises_error() -> None:
    with pytest.raises(InvalidEmailHttpException) as e:
        UserCreate(name="Robert", email="abbondanzieri@.com", phone="11 1234 5678")

    assert e.value.detail == "Invalid email format."
