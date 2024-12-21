import re
import uuid

from pydantic import field_validator
from sqlmodel import Field, Index, SQLModel

from app.utilities.exceptions import InvalidEmailHttpException

EMAIL_VALIDATION = r"^[\w.-]+@\w+\.\w+(\.\w+)?$"


# Shared properties
class UserBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    email: str = Field(unique=True)
    phone: str = Field(unique=True)

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if not re.match(EMAIL_VALIDATION, value):
            raise InvalidEmailHttpException()
        return value


# Properties to receive on item creation
class UserCreate(UserBase):
    pass


# Database model, database table inferred from class name
class User(UserBase, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    public_id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)

    __table_args__ = (Index("id", "public_id"),)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    public_id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
