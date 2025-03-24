import uuid
from datetime import datetime

from sqlmodel import SQLModel


class TokenModel(SQLModel):
    token: str

    @classmethod
    def from_str(cls, key: str) -> "TokenModel":
        return cls(token=key)


class TokenPayload(SQLModel):
    sub: str
    exp: datetime
    iat: datetime

    def is_owner_public_id_in_sub(self, owner_public_id: uuid.UUID) -> bool:
        return self.sub == str(owner_public_id)
