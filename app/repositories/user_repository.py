from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.models.user import User


class UserRepository:
    def __init__(self, uri: str, db_name: str):
        self.__client = AsyncIOMotorClient(uri)
        self.__db = self.__client[db_name]
        self.__collection = self.__db["users"]

    async def close(self):
        self.__client.close()

    async def create_user(self, user: User) -> None:
        await self.__collection.insert_one(user.model_dump())

    async def get_user(self, username: str) -> Optional[User]:
        user = await self.__collection.find_one({"username": username})
        if user:
            user["id"] = str(user.pop("_id"))
            return User(**user)
        return None

    async def initialize_indexes(self):
        await self.__collection.create_index("username", unique=True)
