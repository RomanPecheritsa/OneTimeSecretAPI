from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext


class UserRepository:
    def __init__(self, db: AsyncIOMotorCollection):
        self.__collection = db["users"]
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_user(self, username: str, password: str) -> dict:
        hashed_password = self.__pwd_context.hash(password)
        user = {"username": username, "password": hashed_password}
        result = await self.__collection.insert_one(user)
        user["_id"] = result.inserted_id
        return user

    async def get_user_by_username(self, username: str) -> dict | None:
        return await self.__collection.find_one({"username": username})

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.__pwd_context.verify(plain_password, hashed_password)
