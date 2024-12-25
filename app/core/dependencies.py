from app.repositories.secret_repository import SecretRepository
from app.services.secret_service import SecretService


def create_secret_service_and_repository(mongodb_uri, db_name, salt):
    secret_repository = SecretRepository(mongodb_uri, db_name)
    secret_service = SecretService(salt, secret_repository)
    return secret_repository, secret_service
