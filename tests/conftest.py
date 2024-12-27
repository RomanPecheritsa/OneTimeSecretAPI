import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import MONGODB_URI, SALT, TEST_DATABASE_NAME
from app.core.dependencies import create_secret_service_and_repository, create_user_service_and_repository
from app.main import app


@pytest.fixture(scope="module")
async def setup_service():
    """
    Настройка сервисов и репозиториев для тестирования, инициализация индексов.
    После тестов очищает и закрывает репозитории, удаляет сервисы из состояния приложения.
    """
    test_secret_repository, test_secret_service = create_secret_service_and_repository(
        mongodb_uri=MONGODB_URI, db_name=TEST_DATABASE_NAME, salt=SALT
    )
    test_user_repository, test_user_service = create_user_service_and_repository(
        mongodb_uri=MONGODB_URI, db_name=TEST_DATABASE_NAME
    )
    await test_secret_repository.initialize_indexes()
    await test_user_repository.initialize_indexes()

    app.state.secret_service = test_secret_service
    app.state.user_service = test_user_service

    yield

    await test_secret_repository.clear_all()
    await test_secret_repository.close()

    await test_user_repository.clear_all()
    await test_user_repository.close()
    del app.state.secret_service
    del app.state.user_service


@pytest.fixture
async def authenticated_user() -> str:
    """
    Создает пользователя и выполняет вход в систему, возвращает токен авторизации.
    """
    username = "test_user"
    password = "test_password"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/register", json={"username": username, "password": password})
        response = await ac.post("/login", json={"username": username, "password": password})
        token = response.json().get("access_token")
    return token