from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.core.auth import security
from app.models.user import UserRequest
from app.repositories.user_repository import UserRepository


class UserService:
    """
    Сервис для управления пользователями, включая регистрацию, аутентификацию и работу с паролями.
    """

    def __init__(self, repository: UserRepository):
        """
        Инициализация сервиса пользователей.
        """
        self.repository = repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет, совпадает ли обычный пароль с хешированным паролем.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        """
        Хеширует пароль с использованием алгоритма bcrypt.
        """
        return self.pwd_context.hash(password)

    async def register_user(self, username: str, password: str) -> None:
        """
        Регистрирует нового пользователя.
        """
        if await self.repository.get_user(username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        hashed_password = self.hash_password(password)
        user = UserRequest(username=username, password=hashed_password)
        await self.repository.create_user(user)

    async def authenticate_user(self, username: str, password: str) -> str:
        """
        Аутентифицирует пользователя и генерирует токен доступа.
        """
        user = await self.repository.get_user(username)
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = security.create_access_token(uid=str(user.id))
        return token  # Возврат токена
