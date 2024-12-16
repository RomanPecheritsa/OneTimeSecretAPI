from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from app.dependencies import get_user_service
from app.models.user_model import TokenResponse, UserRequest, UserResponse
from app.services.user_service import UserService

user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


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


@user_router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
) -> TokenResponse:
    try:
        token = await service.authenticate_user(form_data.username, form_data.password)
        return TokenResponse(access_token=token, token_type="bearer")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
