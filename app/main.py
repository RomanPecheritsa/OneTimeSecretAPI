from contextlib import asynccontextmanager

from authx.exceptions import JWTDecodeError
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.auth import security
from app.core.config import DATABASE_NAME, MONGODB_URI, SALT
from app.core.dependencies import create_secret_service_and_repository, create_user_service_and_repository
from app.exceptions import jwt_decode_error_handler
from app.models.secret import PassphraseRequest, SecretKeyResponse, SecretRequest, SecretResponse
from app.models.user import MessageResponse, UserRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Асинхронный контекст для инициализации и закрытия сервисов и репозиториев.

    Этот контекст управляет жизненным циклом приложения. Он создает и инициализирует сервисы и репозитории при старте
    приложения, а затем закрывает их при завершении работы приложения.
    """
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", tags=["Authentication"], response_model=MessageResponse)
async def register_user(request: UserRequest) -> dict:
    """
    Регистрация нового пользователя.

    Этот эндпоинт принимает запрос на регистрацию пользователя, хеширует его пароль и сохраняет данные в базе.

    :param request: Данные о пользователе (имя пользователя и пароль).
    :return: Ответ с сообщением об успешной регистрации.
    """
    await app.state.user_service.register_user(request.username, request.password)
    return MessageResponse(message="User registered successfully")


@app.post("/login", tags=["Authentication"])
async def login_user(request: UserRequest) -> dict:
    """
    Аутентификация пользователя.

    Этот эндпоинт проверяет учетные данные пользователя (имя пользователя и пароль) и генерирует токен доступа.

    :param request: Данные для аутентификации пользователя (имя пользователя и пароль).
    :return: Ответ с токеном доступа.
    """
    token = await app.state.user_service.authenticate_user(request.username, request.password)
    return {"access_token": token}


@app.post("/generate", response_model=SecretKeyResponse, tags=["Secrets"])
async def generate_secret(
    request: SecretRequest, dependencies=Depends(security.access_token_required)
) -> SecretKeyResponse:
    """
    Генерация секрета.

    Этот эндпоинт позволяет пользователю с действительным токеном генерировать секрет и получать уникальный ключ.

    :param request: Запрос на генерацию секрета с кодовой фразой.
    :param dependencies: Зависимость для проверки токена доступа.
    :return: Ответ с уникальным ключом для доступа к секрету.
    """
    secret_key = await app.state.secret_service.generate_secret(request.secret, request.passphrase)
    return SecretKeyResponse(secret_key=secret_key)


@app.post("/secrets/{secret_key}", response_model=SecretResponse, tags=["Secrets"])
async def get_secret(
    secret_key: str, request: PassphraseRequest, dependencies=Depends(security.access_token_required)
) -> SecretResponse:
    """
    Получение секрета.

    Этот эндпоинт позволяет пользователю с действительным токеном и правильной кодовой фразой получить секрет,
    используя уникальный ключ.

    :param secret_key: Ключ для доступа к секрету.
    :param request: Запрос с кодовой фразой для расшифровки секрета.
    :param dependencies: Зависимость для проверки токена доступа.
    :return: Ответ с расшифрованным секретом.
    """
    secret = await app.state.secret_service.get_secret(secret_key, request.passphrase)
    return SecretResponse(secret=secret)
