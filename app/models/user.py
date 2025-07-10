import re
import uuid

from pydantic import field_validator
from sqlalchemy import BigInteger
from sqlmodel import Field, Index, SQLModel

from app.utilities.exceptions import InvalidEmailHttpException

EMAIL_VALIDATOR = r"^[\w.-]+@\w+\.\w+(\.\w+)?$"
USER_TABLE_NAME = "users"


# Shared properties
class UserBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    email: str = Field(unique=True)
    phone: str = Field()
    telegram_id: int | None = Field(default=None, sa_type=BigInteger)

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if not re.match(EMAIL_VALIDATOR, value):
            raise InvalidEmailHttpException()
        return value


# Properties to receive on item creation
class UserCreate(UserBase):
    password: str | None = Field(default=None)

    @field_validator("name", mode="before")
    @classmethod
    def name_length(cls, v):
        if not isinstance(v, str) or len(v) < 1:
            raise ValueError("El nombre debe tener al menos 1 caracter")
        if len(v) > 255:
            raise ValueError("El nombre debe tener como máximo 255 caracteres")
        return v

    @field_validator("phone", mode="before")
    @classmethod
    def phone_length(cls, v):
        if len(v) > 32:
            raise ValueError("El teléfono debe tener como máximo 32 caracteres")
        return v

    def get_password(self) -> str | None:
        return self.password


# Database model, database table inferred from class name
class User(UserBase, table=True):
    __tablename__ = USER_TABLE_NAME
    id: int | None = Field(default=None, primary_key=True)
    public_id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)

    __table_args__ = (Index("id", "public_id"),)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    public_id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
