import hashlib
from typing import Any

from app.models.password import Password
from app.models.user import User


class UserFranco:
    public_id = "1d0c717c-f0ec-4d96-b201-dab75e2b83fe"
    password_raw = "123456879"
    _user: User | None = None

    @classmethod
    def records(cls) -> list[Any]:
        return cls.user() + cls.password()

    @classmethod
    def user(cls) -> list[Any]:
        if cls._user:
            return [cls._user]
        return [
            User(
                name="Jorge",
                email="jorge@fi.uba.ar",
                phone="",
                telegram_id=None,
                public_id=cls.public_id,
            )
        ]

    @classmethod
    def password(cls) -> list[Any]:
        hashing = hashlib.sha512()
        hashing.update(cls.password_raw.encode())
        password_hash = hashing.hexdigest()
        return [Password(user_public_id=cls.public_id, password_hash=password_hash)]


RECORDS: list[Any] = []

RECORDS += UserFranco.records()
