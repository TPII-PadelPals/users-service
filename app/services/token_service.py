from datetime import datetime, timedelta
import uuid

import jwt

from app.core.config import settings
from app.models.token import Token, TokenPublic
from app.utilities.exceptions import (
    InvalidTokenException,
    TokenExpiredSignatureException,
)


class TokenService:
    EXPIRE_TIME: int = settings.TOKEN_EXPIRE_TIME
    ALGORITHM: str = settings.TOKEN_ALGORITHM
    SECRET_KEY: str = settings.TOKEN_SECRET_KEY

    def create_token(self, user_public_id: uuid.UUID, secret_key: str = SECRET_KEY) -> Token:
        payload = {
            "sub": str(user_public_id),
            "exp": datetime.now() + timedelta(hours=self.EXPIRE_TIME),
            "iat": datetime.now(),
        }
        token = jwt.encode(payload, secret_key, algorithm=self.ALGORITHM)
        return Token.from_str(token)

    def _decode_token(self, token: str, public_key: str = SECRET_KEY) -> TokenPublic:
        try:
            decoded = jwt.decode(token, public_key, algorithms=[self.ALGORITHM])
            return TokenPublic(**decoded)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredSignatureException()
        except jwt.InvalidTokenError:
            raise InvalidTokenException()
        except Exception as e:
            raise e

    def validate_token(
        self, token: str, public_key: str, user_public_id: uuid.UUID
    ) -> TokenPublic:
        token_payload = self._decode_token(token, public_key)
        if not token_payload.is_in_sub(user_public_id):
            raise InvalidTokenException()
        return token_payload