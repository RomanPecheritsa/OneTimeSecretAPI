from fastapi import Depends

from app.config import SALT
from app.db import db_connection
from app.repository.secrets_repository import SecretRepository
from app.services.secret_services import SecretService


async def get_secret_repository():
    return SecretRepository(db_connection.db)


async def get_secret_service(repository: SecretRepository = Depends(get_secret_repository)):
    return SecretService(SALT, repository)
