from app.models.login import LoginRequest, LoginResponse
from app.models.user import UsersPublic
from app.repository.paswords_repository import PasswordRepository
from app.repository.users_repository import UsersRepository
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import LoginInvalidCredentialsException


class AuthService:
    async def login(
        self,
        session: SessionDep,
        request: LoginRequest,
    ) -> UsersPublic:
        user_repo = UsersRepository(session)
        user = await user_repo.get_user_by_email(request.email)
        passw_repo = PasswordRepository(session)
        passw = await passw_repo.get_password(user.public_id)
        if not passw:
            raise LoginInvalidCredentialsException()
        passw = passw.model_dump()
        password = passw.get("password_hash")
        if not password or password != request.password:
            raise LoginInvalidCredentialsException()
        return LoginResponse(uuid=user.public_id)
