from fastapi import APIRouter, Depends

from app.dependencies import get_secret_service
from app.models.secret_model import PassphraseRequest, SecretKeyResponse, SecretRequest, SecretResponse
from app.services.secret_services import SecretService

router = APIRouter()


@router.post("/generate", response_model=SecretKeyResponse)
async def generate_secret(
    request: SecretRequest, service: SecretService = Depends(get_secret_service)
) -> SecretKeyResponse:
    secret_key = await service.generate_secret(request.secret, request.passphrase)
    return SecretKeyResponse(secret_key=secret_key)


@router.post("/secrets/{secret_key}", response_model=SecretResponse)
async def get_secret(
    secret_key: str,
    request: PassphraseRequest,
    service: SecretService = Depends(get_secret_service),
) -> SecretResponse:
    secret = await service.get_secret(secret_key, request.passphrase)
    return SecretResponse(secret=secret)
