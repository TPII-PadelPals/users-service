import datetime
import uuid

import jwt

from app.models.token import TokenModel, TokenPayload
from app.utilities.exceptions import TokenException


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

    def decode_token(self, token: str, public_key: str) -> TokenPayload:
        try:
            decoded = jwt.decode(token, public_key, algorithms=[self.ALGORITHM])
            return TokenPayload(**decoded)
        except jwt.ExpiredSignatureError:
            raise TokenException(False)
        except jwt.InvalidTokenError:
            raise TokenException(True)
        except Exception as e:
            raise e
