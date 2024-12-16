from datetime import datetime, timedelta, timezone

import jwt

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


class UserService:
    def __init__(self, repository):
        self.__repository = repository

    async def register_user(self, username: str, password: str) -> dict:
        existing_user = await self.__repository.get_user_by_username(username)
        if existing_user:
            raise ValueError("User already exists")
        return await self.__repository.create_user(username, password)

    async def authenticate_user(self, username: str, password: str) -> str:
        user = await self.__repository.get_user_by_username(username)
        if not user or not await self.__repository.verify_password(password, user["password"]):
            raise ValueError("Invalid username or password")
        return self.create_access_token({"sub": user["username"]})

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
