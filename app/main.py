from contextlib import asynccontextmanager

from authx.exceptions import JWTDecodeError
from fastapi import Depends, FastAPI

from app.core.auth import security
from app.core.config import DATABASE_NAME, MONGODB_URI, SALT
from app.core.dependencies import create_secret_service_and_repository, create_user_service_and_repository
from app.exceptions import jwt_decode_error_handler
from app.models.secret import PassphraseRequest, SecretKeyResponse, SecretRequest, SecretResponse
from app.models.user import UserRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    secret_repository, secret_service = create_secret_service_and_repository(
        mongodb_uri=MONGODB_URI, db_name=DATABASE_NAME, salt=SALT
    )
    user_repository, user_service = create_user_service_and_repository(mongodb_uri=MONGODB_URI, db_name=DATABASE_NAME)

    await secret_repository.initialize_indexes()
    await user_repository.initialize_indexes()

    app.state.secret_service = secret_service
    app.state.user_service = user_service

    yield

    await secret_repository.close()
    await user_repository.close()


app = FastAPI(lifespan=lifespan, title="One Time Secret API")

app.add_exception_handler(JWTDecodeError, jwt_decode_error_handler)


@app.post("/register", tags=["Authentication"])
async def register_user(request: UserRequest) -> dict:
    await app.state.user_service.register_user(request.username, request.password)
    return {"message": "User registered successfully"}


@app.post("/login", tags=["Authentication"])
async def login_user(request: UserRequest) -> dict:
    token = await app.state.user_service.authenticate_user(request.username, request.password)
    return {"access_token": token}


@app.post("/generate", response_model=SecretKeyResponse, tags=["Secrets"])
async def generate_secret(
    request: SecretRequest, dependencies=Depends(security.access_token_required)
) -> SecretKeyResponse:
    secret_key = await app.state.secret_service.generate_secret(request.secret, request.passphrase)
    return SecretKeyResponse(secret_key=secret_key)


@app.post("/secrets/{secret_key}", response_model=SecretResponse, tags=["Secrets"])
async def get_secret(
    secret_key: str, request: PassphraseRequest, dependencies=Depends(security.access_token_required)
) -> SecretResponse:
    secret = await app.state.secret_service.get_secret(secret_key, request.passphrase)
    return SecretResponse(secret=secret)
