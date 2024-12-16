from datetime import datetime

from pydantic import BaseModel


class Secret(BaseModel):
    secret_key: str
    secret: str
    expiration: datetime


class SecretRequest(BaseModel):
    secret: str
    passphrase: str


class PassphraseRequest(BaseModel):
    passphrase: str


class SecretKeyResponse(BaseModel):
    secret_key: str


class SecretResponse(BaseModel):
    secret: str
