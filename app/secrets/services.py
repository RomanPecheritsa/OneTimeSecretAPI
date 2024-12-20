import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from cryptography.fernet import InvalidToken
from fastapi import HTTPException, status

from app.core.config import TTL_EXPIRE_SECONDS
from app.secrets.models import Secret
from app.utils.crypto_utils import decrypt, encrypt, generate_key_from_passphrase


class SecretService:
    def __init__(self, salt: str, repository) -> None:
        self.salt = salt.encode()
        self.__repository = repository

    async def generate_key(self, passphrase: str) -> bytes:
        return generate_key_from_passphrase(passphrase.encode(), self.salt)

    async def generate_secret(self, secret: str, passphrase: str) -> str:
        key = await self.generate_key(passphrase)
        encrypted_secret = encrypt(secret, key)
        secret_key = str(uuid.uuid4())
        secret_instance = Secret(
            secret_key=secret_key,
            secret=encrypted_secret,
            expiration=datetime.now(timezone.utc) + timedelta(seconds=int(TTL_EXPIRE_SECONDS)),
        )
        await self.__repository.create_secret(secret_instance)
        return secret_key

    async def get_secret(self, secret_key: str, passphrase: str) -> Optional[str]:
        secret = await self.__repository.get_secret(secret_key)
        if secret is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

        key = await self.generate_key(passphrase)
        try:
            decrypted_secret = decrypt(secret, key)
        except InvalidToken:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data")

        await self.__repository.delete_secret(secret_key)
        return decrypted_secret
