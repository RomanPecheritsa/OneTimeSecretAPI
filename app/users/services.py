from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


class UserService:
    """
    Сервис для управления пользователями, включая регистрацию и аутентификацию.

    Методы:
    - `register_user`: Регистрация нового пользователя.
    - `authenticate_user`: Аутентификация пользователя с получением токена доступа.
    """

    def __init__(self, repository):
        """
        Инициализация сервиса с репозиторием.

        :param repository: Репозиторий для работы с пользователями.
        """
        self.__repository = repository

    async def register_user(self, username: str, password: str) -> dict:
        """
        Регистрация нового пользователя.

        Проверяет, существует ли уже пользователь с данным именем. Если нет,
        создает нового пользователя.

        :param username: Имя пользователя.
        :param password: Пароль пользователя.
        :return: Данные нового пользователя (включая ID и имя).
        :raises ValueError: Если пользователь с таким именем уже существует.
        """
        existing_user = await self.__repository.get_user_by_username(username)
        if existing_user:
            raise ValueError("User already exists")
        return await self.__repository.create_user(username, password)

    async def authenticate_user(self, username: str, password: str) -> str:
        """
        Аутентификация пользователя.

        Проверяет имя пользователя и пароль. В случае успешной аутентификации
        генерирует и возвращает токен доступа.

        :param username: Имя пользователя.
        :param password: Пароль пользователя.
        :return: Токен доступа.
        :raises ValueError: Если имя пользователя или пароль неверны.
        """
        user = await self.__repository.get_user_by_username(username)
        if not user or not await self.__repository.verify_password(password, user["password"]):
            raise ValueError("Invalid username or password")
        return self.__create_access_token({"sub": user["username"]})

    @staticmethod
    def __create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """
        Генерация токена доступа.

        Создает JWT-токен с указанными данными и временем истечения.

        :param data: Данные, которые должны быть закодированы в токене.
        :param expires_delta: Время жизни токена.
        :return: Закодированный JWT токен.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
