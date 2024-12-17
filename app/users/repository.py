from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext


class UserRepository:
    """
    Репозиторий для взаимодействия с коллекцией пользователей в базе данных MongoDB.

    :param db: Объект коллекции MongoDB для работы с данными пользователей.
    """

    def __init__(self, db: AsyncIOMotorCollection):
        """
        Инициализация репозитория с подключением к коллекции пользователей.

        :param db: Коллекция MongoDB для работы с пользователями.
        """
        self.__collection = db["users"]
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_user(self, username: str, password: str) -> dict:
        """
        Создание нового пользователя в базе данных с хешированием пароля.

        :param username: Имя пользователя.
        :param password: Пароль пользователя.
        :return: Словарь с данными пользователя, включая его уникальный идентификатор.
        """
        hashed_password = self.__pwd_context.hash(password)
        user = {"username": username, "password": hashed_password}
        result = await self.__collection.insert_one(user)
        user["_id"] = result.inserted_id
        return user

    async def get_user_by_username(self, username: str) -> dict | None:
        """
        Получение пользователя из базы данных по имени пользователя.

        :param username: Имя пользователя для поиска.
        :return: Словарь с данными пользователя или `None`, если пользователь не найден.
        """
        return await self.__collection.find_one({"username": username})

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверка пароля, введенного пользователем, с сохраненным хешированным паролем.

        :param plain_password: Введенный пароль.
        :param hashed_password: Хешированный пароль из базы данных.
        :return: `True`, если пароли совпадают, иначе `False`.
        """
        return self.__pwd_context.verify(plain_password, hashed_password)
