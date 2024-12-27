from datetime import datetime

from pydantic import BaseModel


class Secret(BaseModel):
    """
    Модель для представления секрета с ключом, секретным значением и временем истечения.
    """

    secret_key: str
    secret: str
    expiration: datetime


class SecretRequest(BaseModel):
    """
    Модель для запроса секрета, содержащего секретное значение и кодовую фразу.
    """

    secret: str
    passphrase: str


class PassphraseRequest(BaseModel):
    """
    Модель для запроса кодовой фразы.
    """

    passphrase: str


class SecretKeyResponse(BaseModel):
    """
    Модель для ответа, содержащего ключ секрета.
    """

    secret_key: str


class SecretResponse(BaseModel):
    """
    Модель для ответа, содержащего секретное значение.
    """

    secret: str
