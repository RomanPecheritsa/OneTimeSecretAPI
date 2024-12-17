from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.core.dependencies import get_user_service
from app.users.models import TokenResponse, UserRequest, UserResponse
from app.users.services import UserService

user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@user_router.post(
    "/register",
    response_model=UserResponse,
    responses={
        400: {
            "description": "Bad Request - User already exists",
            "content": {"application/json": {"example": {"detail": "User already exists"}}},
        },
        500: {
            "description": "Internal Server Error",
            "content": {"application/json": {"example": {"detail": "Internal server error"}}},
        },
    },
)
async def register_user(
    request: UserRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Регистрация нового пользователя.

    Регистрирует нового пользователя с предоставленным именем пользователя и паролем.

    :param request: Запрос с именем пользователя и паролем.
    :param service: Сервис для работы с пользователями.
    :return: Ответ с данными пользователя, включая ID и имя пользователя.
    :raises HTTPException: В случае ошибки, например, если пользователь уже существует.
    """
    try:
        user = await service.register_user(request.username, request.password)
        return UserResponse(id=str(user["_id"]), username=user["username"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@user_router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {
            "description": "Unauthorized - Invalid username or password",
            "content": {"application/json": {"example": {"detail": "Invalid username or password"}}},
        },
        500: {
            "description": "Internal Server Error",
            "content": {"application/json": {"example": {"detail": "Internal server error"}}},
        },
    },
)
async def login(
    request: UserRequest,
    service: UserService = Depends(get_user_service),
) -> TokenResponse:
    """
    Авторизация пользователя для получения токена доступа.

    Проверяет имя пользователя и пароль, и, если данные верны, выдает токен доступа.

    :param request: Запрос с именем пользователя и паролем.
    :param service: Сервис для работы с пользователями.
    :return: Ответ с токеном доступа.
    :raises HTTPException: В случае ошибки, например, если имя пользователя или пароль неверны.
    """
    try:
        token = await service.authenticate_user(request.username, request.password)
        return TokenResponse(access_token=token, token_type="bearer")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
