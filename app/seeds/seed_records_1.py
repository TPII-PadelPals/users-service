import hashlib
import uuid
from typing import Any

from app.models.password import Password
from app.models.user import User

OWNER_UUID = "1d0c717c-f0ec-4d96-b201-dab75e2b83fe"


class UserSeed:
    password_raw = "123456879"
    _user: User | None = None

    def __init__(self, name: str, public_id: str | None = None) -> None:
        if public_id is None:
            public_id = str(uuid.uuid4())
        self.user = self._init_user(name, public_id)
        self.password = self._init_password(public_id)

    def records(self) -> list[Any]:
        return [self.user, self.password]

    def _init_user(self, name: str, public_id: str) -> "User":
        return User(
            name=name,
            email=f"{name}@fi.uba.ar",
            phone=None,
            telegram_id=None,
            public_id=public_id,
        )

    def _init_password(self, public_id: str) -> "Password":
        hashing = hashlib.sha512()
        hashing.update(self.password_raw.encode())
        password_hash = hashing.hexdigest()
        return Password(user_public_id=public_id, password_hash=password_hash)


RECORDS: list[Any] = []

RECORDS += UserSeed("jorge", OWNER_UUID).records()
RECORDS += UserSeed("adolfo").records()
