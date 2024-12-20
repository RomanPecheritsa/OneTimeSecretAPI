from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGODB_NAME, MONGODB_URI


class MongoDBConnection:
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name]

    async def close(self):
        self.client.close()


db_connection = MongoDBConnection(MONGODB_URI, MONGODB_NAME)
