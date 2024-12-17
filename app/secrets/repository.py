from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from app.core.config import TTL_EXPIRE_SECONDS
from app.secrets.models import Secret


class SecretRepository:
    """
    Репозиторий для работы с коллекцией секретов в базе данных MongoDB.

    :param db: Соединение с базой данных, предоставляющее доступ к коллекции "secrets".
    """

    def __init__(self, db: AsyncIOMotorCollection):
        """
        Инициализация репозитория с коллекцией "secrets".

        :param db: Объект базы данных MongoDB.
        """
        self.__collection = db["secrets"]  # Коллекция секретов

    async def initialize_indexes(self):
        """
        Инициализация индексов для коллекции секретов.

        Создается индекс по полю 'expiration', который автоматически удаляет устаревшие записи по истечению времени.
        """
        existing_indexes = await self.__collection.index_information()
        if "expiration_1" not in existing_indexes:
            await self.__collection.create_index([("expiration", 1)], expireAfterSeconds=int(TTL_EXPIRE_SECONDS))

    async def create_secret(self, secret: Secret) -> None:
        """
        Создание нового секрета в базе данных.

        :param secret: Объект типа `Secret`, содержащий данные для вставки в базу.
        """
        secret_dict = secret.model_dump()  # Преобразование модели в словарь
        await self.__collection.insert_one(secret_dict)

    async def get_secret(self, secret_key: str) -> Optional[str]:
        """
        Получение секрета по его ключу.

        :param secret_key: Уникальный ключ секрета.
        :return: Расшифрованный секрет в случае успеха или `None`, если секрет не найден.
        """
        secret = await self.__collection.find_one({"secret_key": secret_key})
        return secret["secret"] if secret else None

    async def delete_secret(self, secret_key: str) -> None:
        """
        Удаление секрета по ключу.

        :param secret_key: Уникальный ключ секрета.
        """
        await self.__collection.delete_one({"secret_key": secret_key})
