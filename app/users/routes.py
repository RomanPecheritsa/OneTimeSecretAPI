from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.core.dependencies import get_user_service
from app.users.models import TokenResponse, UserRequest, UserResponse
from app.users.services import UserService

user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@user_router.post("/register", response_model=UserResponse)
async def register_user(
    request: UserRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = await service.register_user(request.username, request.password)
        return UserResponse(id=str(user["_id"]), username=user["username"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.post("/login", response_model=TokenResponse)
async def login(
    request: UserRequest,
    service: UserService = Depends(get_user_service),
) -> TokenResponse:
    try:
        token = await service.authenticate_user(request.username, request.password)
        return TokenResponse(access_token=token, token_type="bearer")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
