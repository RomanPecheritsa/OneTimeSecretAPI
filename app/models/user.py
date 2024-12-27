from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: Optional[str]
    username: str
    password: str

    class Config:
        json_encoders = {ObjectId: str}
