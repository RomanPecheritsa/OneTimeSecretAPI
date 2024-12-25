from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import TTL_INDEX_SECONDS
from app.models.secret import Secret


class SecretRepository:
    def __init__(self, uri: str, db_name: str):
        self.__client = AsyncIOMotorClient(uri)
        self.__db = self.__client[db_name]
        self.__collection = self.__db["secrets"]

    async def initialize_indexes(self):
        existing_indexes = await self.__collection.index_information()
        if "expiration_1" not in existing_indexes:
            await self.__collection.create_index([("expiration", 1)], expireAfterSeconds=int(TTL_INDEX_SECONDS))

    async def close(self):
        self.__client.close()

    async def create(self, secret: Secret) -> None:
        secret_dict = secret.model_dump()
        await self.__collection.insert_one(secret_dict)

    async def get(self, secret_key: str) -> Optional[str]:
        secret = await self.__collection.find_one({"secret_key": secret_key})
        return secret["secret"] if secret else None

    async def delete(self, secret_key: str) -> None:
        await self.__collection.delete_one({"secret_key": secret_key})

    async def clear_all(self) -> None:
        await self.__collection.delete_many({})
