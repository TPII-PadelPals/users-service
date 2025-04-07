import uuid

from sqlmodel import Field, SQLModel

PASSWORD_TABLE_NAME = "passwords"


class PasswordBase(SQLModel):
    user_public_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        unique=True,
    )
    password_hash: str = Field(default=None)


class PasswordCreate(PasswordBase):
    pass


class PasswordUpdate(PasswordBase):
    pass


class Password(PasswordBase, table=True):
    __tablename__ = PASSWORD_TABLE_NAME
    id: int = Field(default=None, primary_key=True)
