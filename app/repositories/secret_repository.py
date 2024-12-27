from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import TTL_INDEX_SECONDS
from app.models.secret import Secret


class SecretRepository:
    """
    Репозиторий для работы с коллекцией секретов в базе данных MongoDB.

    Этот класс предоставляет методы для создания, получения, удаления и очистки секретов в коллекции.
    Также он инициализирует индекс для автоматического удаления просроченных секретов.
    """

    def __init__(self, uri: str, db_name: str):
        """
        Инициализация репозитория для работы с базой данных MongoDB.
        """
        self.__client = AsyncIOMotorClient(uri)
        self.__db = self.__client[db_name]
        self.__collection = self.__db["secrets"]

    async def initialize_indexes(self):
        """
        Инициализирует индексы в коллекции. Создает индекс на поле `expiration`, если он еще не существует.
        Индекс используется для автоматического удаления секретов после истечения срока их действия.
        """
        existing_indexes = await self.__collection.index_information()
        if "expiration_1" not in existing_indexes:
            await self.__collection.create_index([("expiration", 1)], expireAfterSeconds=int(TTL_INDEX_SECONDS))

    async def close(self):
        """
        Закрывает подключение к базе данных MongoDB.
        """
        self.__client.close()

    async def create(self, secret: Secret) -> None:
        """
        Создает новый секрет в базе данных.
        """
        secret_dict = secret.model_dump()
        await self.__collection.insert_one(secret_dict)

    async def get(self, secret_key: str) -> Optional[str]:
        """
        Получает секрет по его ключу.
        """
        secret = await self.__collection.find_one({"secret_key": secret_key})
        return secret["secret"] if secret else None

    async def delete(self, secret_key: str) -> None:
        """
        Удаляет секрет по его ключу.

        """
        await self.__collection.delete_one({"secret_key": secret_key})

    async def clear_all(self) -> None:
        """
        Удаляет все секреты из коллекции.
        """
        await self.__collection.delete_many({})
