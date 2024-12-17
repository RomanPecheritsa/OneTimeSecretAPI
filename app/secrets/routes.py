from fastapi import APIRouter, Depends

from app.core.dependencies import get_secret_service
from app.secrets.models import (PassphraseRequest, SecretKeyResponse,
                                SecretRequest, SecretResponse)
from app.secrets.services import SecretService
from app.utils.auth import get_current_user

secret_router = APIRouter()


@secret_router.post("/generate", response_model=SecretKeyResponse)
async def generate_secret(
    request: SecretRequest,
    service: SecretService = Depends(get_secret_service),
    current_user: str = Depends(get_current_user),
) -> SecretKeyResponse:
    secret_key = await service.generate_secret(request.secret, request.passphrase)
    return SecretKeyResponse(secret_key=secret_key)


@secret_router.post("/secrets/{secret_key}", response_model=SecretResponse)
async def get_secret(
    secret_key: str,
    request: PassphraseRequest,
    service: SecretService = Depends(get_secret_service),
    current_user: str = Depends(get_current_user),
) -> SecretResponse:
    secret = await service.get_secret(secret_key, request.passphrase)
    return SecretResponse(secret=secret)
