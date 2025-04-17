import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.password import Password, PasswordCreate


class PasswordRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_password(self, user: uuid.UUID, password: str) -> Password:
        password_create = PasswordCreate(user_public_id=user, password_hash=password)
        new_password = Password.model_validate(password_create)
        self.session.add(new_password)
        await self.session.flush()
        return new_password
