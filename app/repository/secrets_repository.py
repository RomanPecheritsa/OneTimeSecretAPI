from typing import Optional

from app.config import TTL_EXPIRE_SECONDS
from app.models.secrets import Secret


class SecretRepository:
    def __init__(self, db):
        self.__collection = db["secrets"]
        self.__indexes_initialized = False

    async def initialize_indexes(self):
        if not self.__indexes_initialized:
            existing_indexes = await self.__collection.index_information()
            if "expiration_1" not in existing_indexes:
                await self.__collection.create_index([("expiration", 1)], expireAfterSeconds=TTL_EXPIRE_SECONDS)
            self.__indexes_initialized = True

    async def create(self, secret: Secret) -> None:
        await self.initialize_indexes()
        secret_dict = secret.model_dump()
        await self.__collection.insert_one(secret_dict)

    async def get(self, secret_key: str) -> Optional[str]:
        await self.initialize_indexes()
        secret = await self.__collection.find_one({"secret_key": secret_key})
        return secret["secret"] if secret else None

    async def delete(self, secret_key: str) -> None:
        await self.__collection.delete_one({"secret_key": secret_key})
