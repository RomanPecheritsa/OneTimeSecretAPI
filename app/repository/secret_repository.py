from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from app.config import TTL_EXPIRE_SECONDS
from app.models.secret_model import Secret


class SecretRepository:
    def __init__(self, db: AsyncIOMotorCollection):
        self.__collection = db["secrets"]

    async def initialize_indexes(self):
        existing_indexes = await self.__collection.index_information()
        if "expiration_1" not in existing_indexes:
            await self.__collection.create_index([("expiration", 1)], expireAfterSeconds=int(TTL_EXPIRE_SECONDS))

    async def create_secret(self, secret: Secret) -> None:
        secret_dict = secret.model_dump()
        await self.__collection.insert_one(secret_dict)

    async def get_secret(self, secret_key: str) -> Optional[str]:
        secret = await self.__collection.find_one({"secret_key": secret_key})
        return secret["secret"] if secret else None

    async def delete_secret(self, secret_key: str) -> None:
        await self.__collection.delete_one({"secret_key": secret_key})
