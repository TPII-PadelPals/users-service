import uuid

from sqlmodel import Field, SQLModel


# Shared properties
class UserBase(SQLModel):
    name: str = Field()
    email: str = Field(unique=True)
    phone: str = Field()


# Properties to receive on item creation
class UserCreate(UserBase):
    pass


# Database model, database table inferred from class name
class User(UserBase, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    public_id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    public_id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
