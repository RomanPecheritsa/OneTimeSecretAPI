import re

from pydantic import BaseModel, field_validator


class UserRequest(BaseModel):
    """
    Модель запроса пользователя для регистрации или входа в систему.

    :param username: Имя пользователя.
    :param password: Пароль пользователя, который должен удовлетворять определённым требованиям.
    """

    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Валидатор пароля, проверяющий соответствие нескольких условий:
        - Минимальная длина 8 символов.
        - Наличие хотя бы одной заглавной буквы.
        - Наличие хотя бы одной цифры.
        - Наличие хотя бы одного специального символа.

        :param value: Пароль пользователя.
        :raises ValueError: Если пароль не соответствует условиям.
        :return: Валидированный пароль.
        """
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value

    class Config:
        json_schema_extra = {"example": {"username": "my_username", "password": "mySuperPassword99!"}}


class UserResponse(BaseModel):
    """
    Модель ответа с данными о пользователе.

    :param id: Уникальный идентификатор пользователя.
    :param username: Имя пользователя.
    """

    id: str
    username: str

    class Config:
        json_schema_extra = {"example": {"id": "67613fe0f548ce39642a8644", "username": "my_username"}}


class TokenResponse(BaseModel):
    """
    Модель ответа с данными о токене доступа.

    :param access_token: Токен доступа.
    :param token_type: Тип токена (например, "bearer").
    """

    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {"example": {"access_token": "my_access_token", "token_type": "bearer"}}
