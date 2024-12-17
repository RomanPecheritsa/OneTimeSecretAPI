import re

from pydantic import BaseModel, field_validator


class UserRequest(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, value):
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
    id: str
    username: str

    class Config:
        json_schema_extra = {"example": {"id": "67613fe0f548ce39642a8644", "username": "my_username"}}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {"example": {"access_token": "my_access_token", "token_type": "bearer"}}
