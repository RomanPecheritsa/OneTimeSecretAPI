from fastapi import Depends

from app.core.config import SALT
from app.core.db import db_connection
from app.secrets.repository import SecretRepository
from app.secrets.services import SecretService
from app.users.repository import UserRepository
from app.users.services import UserService


async def get_secret_repository() -> SecretRepository:
    """
    Получает экземпляр репозитория для работы с секретами.

    Инициализирует индексы репозитория перед его возвращением.

    :return: Экземпляр репозитория для работы с секретами.
    """
    repo = SecretRepository(db_connection.db)
    await repo.initialize_indexes()
    return repo


async def get_secret_service(repository: SecretRepository = Depends(get_secret_repository)) -> SecretService:
    """
    Получает экземпляр сервиса для работы с секретами.

    Использует репозиторий для взаимодействия с базой данных и инициализирует сервис.

    :param repository: Репозиторий, используемый для доступа к данным о секретах (по умолчанию получаем из get_secret_repository).
    :return: Экземпляр сервиса для работы с секретами.
    """
    return SecretService(SALT, repository)


async def get_user_repository() -> UserRepository:
    """
    Получает экземпляр репозитория для работы с пользователями.

    :return: Экземпляр репозитория для работы с пользователями.
    """
    return UserRepository(db_connection.db)


async def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    """
    Получает экземпляр сервиса для работы с пользователями.

    Использует репозиторий для взаимодействия с базой данных и инициализирует сервис.

    :param repository: Репозиторий, используемый для доступа к данным о пользователях (по умолчанию получаем из get_user_repository).
    :return: Экземпляр сервиса для работы с пользователями.
    """
    return UserService(repository)
