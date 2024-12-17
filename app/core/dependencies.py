from fastapi import Depends

from app.core.config import SALT
from app.core.db import db_connection
from app.secrets.repository import SecretRepository
from app.users.repository import UserRepository
from app.secrets.services import SecretService
from app.users.services import UserService


async def get_secret_repository():
    repo = SecretRepository(db_connection.db)
    await repo.initialize_indexes()
    return repo


async def get_secret_service(repository: SecretRepository = Depends(get_secret_repository)):
    return SecretService(SALT, repository)


async def get_user_repository():
    return UserRepository(db_connection.db)


async def get_user_service(repository: UserRepository = Depends(get_user_repository)):
    return UserService(repository)
