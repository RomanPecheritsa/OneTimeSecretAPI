from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import DATABASE_NAME, MONGODB_URI, SALT
from app.core.dependencies import create_secret_service_and_repository
from app.models.secret import PassphraseRequest, SecretKeyResponse, SecretRequest, SecretResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    secret_repository, secret_service = create_secret_service_and_repository(
        mongodb_uri=MONGODB_URI,
        db_name=DATABASE_NAME,
        salt=SALT
    )
    await secret_repository.initialize_indexes()
    app.state.secret_service = secret_service

    yield

    await secret_repository.close()


app = FastAPI(lifespan=lifespan)


@app.post("/generate", response_model=SecretKeyResponse)
async def generate_secret(request: SecretRequest) -> SecretKeyResponse:
    secret_key = await app.state.secret_service.generate_secret(request.secret, request.passphrase)
    return SecretKeyResponse(secret_key=secret_key)


@app.post("/secrets/{secret_key}", response_model=SecretResponse)
async def get_secret(secret_key: str, request: PassphraseRequest) -> SecretResponse:
    secret = await app.state.secret_service.get_secret(secret_key, request.passphrase)
    return SecretResponse(secret=secret)
