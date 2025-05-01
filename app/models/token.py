import uuid
from datetime import datetime

from sqlmodel import SQLModel


class Token(SQLModel):
    token: str

    @classmethod
    def from_str(cls, key: str) -> "Token":
        return cls(token=key)


class TokenPublic(SQLModel):
    sub: str  # Contenido del token (en este caso el uuID)
    exp: datetime  # Fecha de expiracion del token
    iat: datetime  # Fecha de creacion del token

    def is_in_sub(self, owner_public_id: uuid.UUID) -> bool:
        return self.sub == str(owner_public_id)
