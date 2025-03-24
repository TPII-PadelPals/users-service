import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.utilities.exceptions import NotFoundException


class KeyManagerService:
    PUBLIC_EXPONENT = 65537
    KEY_SIZE = 2048

    def __init__(self) -> None:
        self.key_storage: dict[uuid.UUID, bytes] = {}
        self._generate_key_pair()

    def _generate_key_pair(self) -> None:
        self.private_key = rsa.generate_private_key(
            public_exponent=self.PUBLIC_EXPONENT,
            key_size=self.KEY_SIZE,
            backend=default_backend(),
        )
        self.public_key = self.private_key.public_key()

    def serialize_public_key(self) -> str:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    def serialize_private_key(self) -> str:
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")

    def add_public_key(self, user_public_id: uuid.UUID, public_key: str) -> None:
        self.key_storage[user_public_id] = public_key.encode("utf-8")

    def get_public_key(self, user_public_id: uuid.UUID) -> str:
        result = self.key_storage.get(user_public_id)
        if result is None:
            raise NotFoundException("Public key")
        return result.decode("utf-8")
