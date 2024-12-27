from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class UserRequest(BaseModel):
    """
    Модель запроса для создания пользователя, содержащая имя пользователя и пароль.
    """

    username: str
    password: str


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
