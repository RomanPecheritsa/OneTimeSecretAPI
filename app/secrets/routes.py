from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.dependencies import get_secret_service
from app.secrets.models import PassphraseRequest, SecretKeyResponse, SecretRequest, SecretResponse
from app.secrets.services import SecretService
from app.utils.auth import get_current_user

secret_router = APIRouter()


@secret_router.post(
    "/generate",
    response_model=SecretKeyResponse,
    responses={
        401: {
            "description": "Unauthorized - User is not authorized",
            "content": {"application/json": {"example": {"detail": "Authorization token is missing or invalid"}}},
        },
        400: {
            "description": "Bad Request - Invalid input data",
            "content": {"application/json": {"example": {"detail": "Invalid secret or passphrase"}}},
        },
        500: {
            "description": "Internal Server Error",
            "content": {"application/json": {"example": {"detail": "Internal server error"}}},
        },
    },
)
async def generate_secret(
    request: SecretRequest,
    service: SecretService = Depends(get_secret_service),
    current_user: str = Depends(get_current_user),
) -> SecretKeyResponse:
    try:
        secret_key = await service.generate_secret(request.secret, request.passphrase)
        return SecretKeyResponse(secret_key=secret_key)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@secret_router.post(
    "/secrets/{secret_key}",
    response_model=SecretResponse,
    responses={
        401: {
            "description": "Unauthorized - User is not authorized",
            "content": {"application/json": {"example": {"detail": "Authorization token is missing or invalid"}}},
        },
        404: {
            "description": "Not Found - Secret not found",
            "content": {"application/json": {"example": {"detail": "Secret with the provided key not found"}}},
        },
        400: {
            "description": "Bad Request - Invalid passphrase",
            "content": {"application/json": {"example": {"detail": "Invalid passphrase"}}},
        },
        500: {
            "description": "Internal Server Error",
            "content": {"application/json": {"example": {"detail": "Internal server error"}}},
        },
    },
)
async def get_secret(
    secret_key: str,
    request: PassphraseRequest,
    service: SecretService = Depends(get_secret_service),
    current_user: str = Depends(get_current_user),
) -> SecretResponse:
    try:
        secret = await service.get_secret(secret_key, request.passphrase)
        return SecretResponse(secret=secret)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
