from datetime import datetime

from pydantic import BaseModel


class Secret(BaseModel):
    """
    Модель для хранения информации о секрете.

    :param secret_key: Уникальный ключ секрета.
    :param secret: Зашифрованный секрет.
    :param expiration: Время истечения действия секрета.
    """

    secret_key: str
    secret: str
    expiration: datetime


class SecretRequest(BaseModel):
    """
    Модель запроса для создания секрета.

    :param secret: Текст секрета, который будет зашифрован.
    :param passphrase: Фраза для шифрования секрета.
    """

    secret: str
    passphrase: str

    class Config:
        json_schema_extra = {"example": {"secret": "my_secret", "passphrase": "my_passphrase"}}


class PassphraseRequest(BaseModel):
    """
    Модель запроса с пасфразой для доступа к секрету.

    :param passphrase: Фраза для расшифровки секрета.
    """

    passphrase: str

    class Config:
        json_schema_extra = {"example": {"passphrase": "my_passphrase"}}


class SecretKeyResponse(BaseModel):
    """
    Модель ответа с ключом секрета.

    :param secret_key: Уникальный ключ секрета.
    """

    secret_key: str

    class Config:
        json_schema_extra = {"example": {"secret_key": "secret_key"}}


class SecretResponse(BaseModel):
    """
    Модель ответа с расшифрованным секретом.

    :param secret: Расшифрованный секрет.
    """

    secret: str

    class Config:
        json_schema_extra = {"example": {"secret": "my_secret"}}
