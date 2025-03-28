import datetime
import uuid

import jwt

from app.models.token import TokenModel, TokenPayload
from app.utilities.exceptions import (
    InvalidTokenException,
    TokenExpiredSignatureException,
)


class TokenService:
    EXPIRE_TIME: int = 24
    ALGORITHM: str = "RS256"

    def create_token(self, user_public_id: uuid.UUID, private_key: str) -> TokenModel:
        payload = {
            "sub": str(user_public_id),
            "exp": datetime.datetime.now() + datetime.timedelta(hours=self.EXPIRE_TIME),
            "iat": datetime.datetime.now(),
        }
        token = jwt.encode(payload, private_key, algorithm=self.ALGORITHM)
        return TokenModel.from_str(token)

    def _decode_token(self, token: str, public_key: str) -> TokenPayload:
        try:
            decoded = jwt.decode(token, public_key, algorithms=[self.ALGORITHM])
            return TokenPayload(**decoded)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredSignatureException()
        except jwt.InvalidTokenError:
            raise InvalidTokenException()
        except Exception as e:
            raise e

    def validate_token(
        self, token: str, public_key: str, user_public_id: uuid.UUID
    ) -> TokenPayload:
        token_payload = self._decode_token(token, public_key)
        if not token_payload.is_owner_public_id_in_sub(user_public_id):
            raise InvalidTokenException()
        return token_payload
