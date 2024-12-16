from fastapi import Depends

from app.config import SALT
from app.db import db_connection
from app.repository.secret_repository import SecretRepository
from app.repository.user_repository import UserRepository
from app.services.secret_services import SecretService
from app.services.user_service import UserService


async def get_secret_repository():
    repo = SecretRepository(db_connection.db)
    await repo.initialize_indexes()
    return SecretRepository(db_connection.db)


async def get_secret_service(repository: SecretRepository = Depends(get_secret_repository)):
    return SecretService(SALT, repository)


async def get_user_repository():
    return UserRepository(db_connection.db)


async def get_user_service(repository: UserRepository = Depends(get_user_repository)):
    return UserService(repository)
