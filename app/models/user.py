import re
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, field_validator


class UserRequest(BaseModel):
    """
    Модель запроса для создания пользователя, содержащая имя пользователя и пароль.
    """

    username: str
    password: str

    @field_validator("username")
    def username_min_length(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v

    @field_validator("password")
    def password_complexity(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[\W_]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class User(BaseModel):
    """
    Модель пользователя, включающая идентификатор, имя пользователя и пароль.
    """

    id: Optional[str]
    username: str
    password: str

    class Config:
        """
        Конфигурация для сериализации и десериализации объекта, включая преобразование ObjectId в строку.
        """

        json_encoders = {ObjectId: str}


class MessageResponse(BaseModel):
    """Модель ответа"""

    message: str
