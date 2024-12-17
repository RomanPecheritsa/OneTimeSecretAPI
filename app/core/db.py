from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGODB_NAME, MONGODB_URI


class MongoDBConnection:
    """
    Класс для подключения к MongoDB базе данных с использованием библиотеки AsyncIOMotorClient.
    """

    def __init__(self, uri: str, database_name: str):
        """
        Инициализирует подключение к MongoDB базе данных.

        :param uri: URI для подключения к базе данных MongoDB.
        :param database_name: Название базы данных, к которой будет установлено соединение.
        """
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name]

    async def close(self) -> None:
        """
        Закрывает соединение с MongoDB.
        """
        self.client.close()


db_connection = MongoDBConnection(MONGODB_URI, MONGODB_NAME)
