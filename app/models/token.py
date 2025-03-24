from sqlmodel import SQLModel


class PublicKeyModel(SQLModel):
    key: str

    @classmethod
    def from_str(cls, key: str) -> "PublicKeyModel":
        return cls(key=key)


class TokenModel(SQLModel):
    token: str

    @classmethod
    def from_str(cls, key: str) -> "TokenModel":
        return cls(token=key)
