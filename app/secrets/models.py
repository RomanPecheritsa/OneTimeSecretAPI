from datetime import datetime

from pydantic import BaseModel


class Secret(BaseModel):
    secret_key: str
    secret: str
    expiration: datetime


class SecretRequest(BaseModel):
    secret: str
    passphrase: str

    class Config:
        json_schema_extra = {"example": {"secret": "my_secret", "passphrase": "my_passphrase"}}


class PassphraseRequest(BaseModel):
    passphrase: str

    class Config:
        json_schema_extra = {"example": {"passphrase": "my_passphrase"}}


class SecretKeyResponse(BaseModel):
    secret_key: str

    class Config:
        json_schema_extra = {"example": {"secret_key": "secret_key"}}


class SecretResponse(BaseModel):
    secret: str

    class Config:
        json_schema_extra = {"example": {"secret": "my_secret"}}
