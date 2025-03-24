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
