import hashlib
import uuid
from typing import Any

from app.core.config import settings
from app.models.password import Password
from app.models.user import User

ASSIGNED_UUID = "db08d286-58cf-4542-8501-efa273e38be4"

SIMILAR_NAMES = ["Benedicto", "Francisco", "Leon"]
SIMILAR_UUIDS = [
    "3cbccfa2-65d7-4d49-b801-b7f30daae857",
    "96ff36d6-bd6e-49c3-a666-cda2d2865be0",
    "a80a64fb-9672-450c-a98e-bcf366ea6ac8",
]


class UserSeed:
    password_raw = "123456879"

    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        chat_id: int,
        public_id: str | None = None,
    ) -> None:
        if public_id is None:
            public_id = str(uuid.uuid4())
        self.user = self._init_user(name, email, phone, chat_id, public_id)
        self.password = self._init_password(public_id)

    def records(self) -> list[Any]:
        return [self.user, self.password]

    def _init_user(
        self, name: str, email: str, phone: str, chat_id: int, public_id: str
    ) -> "User":
        return User(
            name=name,
            email=email,
            phone=phone,
            telegram_id=chat_id,
            public_id=public_id,
        )

    def _init_password(self, public_id: str) -> "Password":
        hashing = hashlib.sha512()
        hashing.update(self.password_raw.encode())
        password_hash = hashing.hexdigest()
        return Password(user_public_id=public_id, password_hash=password_hash)


RECORDS: list[Any] = []

RECORDS += UserSeed(
    settings.USER_NAME,
    settings.USER_MAIL,
    settings.USER_PHONE,
    settings.USER_TELEGRAM_ID,
    ASSIGNED_UUID,
).records()

for i, (similar_name, similar_uuid) in enumerate(
    zip(SIMILAR_NAMES, SIMILAR_UUIDS, strict=False)
):
    RECORDS += UserSeed(
        similar_name,
        f"{similar_name.lower()}@notamail.com",
        f"Not a phone number {i}",
        100 + i,
        similar_uuid,
    ).records()
