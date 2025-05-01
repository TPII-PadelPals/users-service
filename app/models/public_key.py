from sqlmodel import SQLModel


class PublicKey(SQLModel):
    key: str

    @classmethod
    def from_str(cls, key: str) -> "PublicKey":
        return cls(key=key)
