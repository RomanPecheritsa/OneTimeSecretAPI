import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from cryptography.fernet import InvalidToken
from fastapi import HTTPException, status

from app.core.config import TTL_INDEX_SECONDS
from app.models.secret import Secret
from app.repositories.secret_repository import SecretRepository
from app.utils.crypto_utils import decrypt, encrypt, generate_key_from_passphrase


class SecretService:
    """
    Сервис для управления секретами, который включает генерацию, сохранение, извлечение и удаление зашифрованных данных.
    """

    def __init__(self, salt: str, repository: SecretRepository) -> None:
        """
        Инициализация сервиса для работы с секретами.
        """
        self.salt = salt.encode()
        self.repository = repository

    async def generate_key(self, passphrase: str) -> bytes:
        """
        Генерирует ключ для шифрования/дешифрования на основе кодовой фразы.
        """
        return generate_key_from_passphrase(passphrase.encode(), self.salt)

    async def generate_secret(self, secret: str, passphrase: str) -> str:
        """
        Генерирует зашифрованный секрет и сохраняет его в базе данных.
        """
        key = await self.generate_key(passphrase)
        encrypted_secret = encrypt(secret, key)
        secret_key = str(uuid.uuid4())
        secret_instance = Secret(
            secret_key=secret_key,
            secret=encrypted_secret,
            expiration=datetime.now(timezone.utc) + timedelta(seconds=int(TTL_INDEX_SECONDS)),
        )
        await self.repository.create(secret_instance)
        return secret_key

    async def get_secret(self, secret_key: str, passphrase: str) -> Optional[str]:
        """
        Извлекает зашифрованный секрет из базы данных и расшифровывает его.
        """
        secret = await self.repository.get(secret_key)
        if secret is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

        key = await self.generate_key(passphrase)
        try:
            decrypted_secret = decrypt(secret, key)
        except InvalidToken:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data")

        await self.repository.delete(secret_key)
        return decrypted_secret
