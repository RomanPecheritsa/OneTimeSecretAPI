from app.repositories.secret_repository import SecretRepository
from app.repositories.user_repository import UserRepository
from app.services.secret_service import SecretService
from app.services.user_service import UserService


def create_secret_service_and_repository(mongodb_uri: str, db_name: str, salt: str) -> tuple:
    """
    Создает репозиторий и сервис для работы с секретами.
    """
    secret_repository = SecretRepository(mongodb_uri, db_name)
    secret_service = SecretService(salt, secret_repository)
    return secret_repository, secret_service


def create_user_service_and_repository(mongodb_uri: str, db_name: str) -> tuple:
    """
    Создает репозиторий и сервис для работы с пользователями.
    """
    user_repository = UserRepository(mongodb_uri, db_name)
    user_service = UserService(user_repository)
    return user_repository, user_service
