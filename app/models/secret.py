from datetime import datetime

from pydantic import BaseModel


class Secret(BaseModel):
    """
    Модель для представления секрета с ключом, секретным значением и временем истечения.
    """

    secret_key: str  # Ключ секрета
    secret: str  # Секретное значение
    expiration: datetime  # Время истечения секрета


class SecretRequest(BaseModel):
    """
    Модель для запроса секрета, содержащего секретное значение и кодовую фразу.
    """

    secret: str  # Секретное значение
    passphrase: str  # Кодовая фраза для доступа к секрету


class PassphraseRequest(BaseModel):
    """
    Модель для запроса кодовой фразы.
    """

    passphrase: str  # Кодовая фраза


class SecretKeyResponse(BaseModel):
    """
    Модель для ответа, содержащего ключ секрета.
    """

    secret_key: str  # Ключ секрета


class SecretResponse(BaseModel):
    """
    Модель для ответа, содержащего секретное значение.
    """

    secret: str  # Секретное значение
