import hashlib

from app.models.login import LoginRequest, LoginResponse
from app.models.user import User, UserCreate
from app.repository.paswords_repository import PasswordRepository
from app.repository.users_repository import UsersRepository
from app.services.token_service import TokenService
from app.services.users_service import UsersService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import LoginInvalidCredentialsException


class AuthService:
    async def login(
        self,
        session: SessionDep,
        request: LoginRequest,
    ) -> LoginResponse:
        user_repo = UsersRepository(session)
        user = await user_repo.get_user_by_email(request.email)
        passw_repo = PasswordRepository(session)
        passw = await passw_repo.get_password(user.public_id)
        if not passw:
            raise LoginInvalidCredentialsException()
        passw = passw.model_dump()
        password = passw.get("password_hash")
        hashing = hashlib.sha512()
        hashing.update(request.password.encode())
        hash_password = hashing.hexdigest()
        if not password or password != hash_password:
            raise LoginInvalidCredentialsException()
        token_service = TokenService()
        token = token_service.create_token(user.public_id)
        return LoginResponse(uuid=user.public_id, token=token.token)

    async def signup(self, session: SessionDep, user_in: UserCreate) -> User:
        user_service = UsersService()
        return await user_service.create_user(session, user_in)
