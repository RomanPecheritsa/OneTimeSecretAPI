from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.models.user import User


class UserRepository:
    """
    Репозиторий для работы с коллекцией пользователей в базе данных MongoDB.

    Этот класс предоставляет методы для создания, получения и очистки пользователей в коллекции.
    Также он инициализирует индекс для уникальности имени пользователя.
    """

    def __init__(self, uri: str, db_name: str):
        """
        Инициализация репозитория для работы с базой данных MongoDB.
        """
        self.__client = AsyncIOMotorClient(uri)
        self.__db = self.__client[db_name]
        self.__collection = self.__db["users"]

    async def close(self):
        """
        Закрывает подключение к базе данных MongoDB.
        """
        self.__client.close()

    async def create_user(self, user: User) -> None:
        """
        Создает нового пользователя в базе данных.
        """
        await self.__collection.insert_one(user.model_dump())

    async def get_user(self, username: str) -> Optional[User]:
        """
        Получает пользователя по имени пользователя (username).
        """
        user = await self.__collection.find_one({"username": username})
        if user:
            user["id"] = str(user.pop("_id"))
            return User(**user)
        return None

    async def initialize_indexes(self):
        """
        Инициализирует индекс на поле "username" с уникальностью для предотвращения дублирования имен пользователей.
        """
        await self.__collection.create_index("username", unique=True)

    async def clear_all(self) -> None:
        """
        Удаляет всех пользователей из коллекции.
        """
        await self.__collection.delete_many({})
