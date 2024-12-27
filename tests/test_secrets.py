from typing import Dict

import pytest
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGODB_URI, TEST_DATABASE_NAME, TTL_INDEX_SECONDS
from app.main import app


@pytest.fixture
def secret_data() -> Dict[str, Dict[str, str]]:
    """
    Фикстура для тестовых данных с различными комбинациями секретных данных.
    """
    return {
        "correct": {"secret": "test_secret", "passphrase": "test_passphrase", "secret_key": "secret_key"},
        "incorrect_passphrase": {"secret": "test_secret", "passphrase": "wrong_passphrase", "secret_key": "secret_key"},
        "incorrect_secret_key": {"secret": "test_secret", "passphrase": "test_passphrase", "secret_key": "invalid_key"},
        "incorrect_both": {"secret": "test_secret", "passphrase": "wrong_passphrase", "secret_key": "invalid_key"},
    }


@pytest.mark.anyio
async def test_generate_secret(
    setup_service: None, secret_data: Dict[str, Dict[str, str]], authenticated_user: str
) -> None:
    """
    Тестирует генерацию секрета.
    Ожидается успешный ответ с созданным ключом секрета.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/generate", json=secret_data["correct"], headers={"Authorization": f"Bearer {authenticated_user}"}
        )
    assert response.status_code == 200
    assert "secret_key" in response.json()


@pytest.mark.anyio
async def test_get_secret(setup_service: None, secret_data: Dict[str, Dict[str, str]], authenticated_user: str) -> None:
    """
    Тестирует получение секрета по правильному ключу и паролю.
    Ожидается успешный ответ с секретом.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        generate_response = await ac.post(
            "/generate", json=secret_data["correct"], headers={"Authorization": f"Bearer {authenticated_user}"}
        )
        secret_key = generate_response.json()["secret_key"]

        response = await ac.post(
            f"/secrets/{secret_key}",
            json={"passphrase": secret_data["correct"]["passphrase"]},
            headers={"Authorization": f"Bearer {authenticated_user}"},
        )
    assert response.status_code == 200
    assert response.json() == {"secret": secret_data["correct"]["secret"]}


@pytest.mark.anyio
async def test_get_secret_with_incorrect_passphrase(
    setup_service: None, secret_data: Dict[str, Dict[str, str]], authenticated_user: str
) -> None:
    """
    Тестирует получение секрета с неправильным паролем.
    Ожидается ошибка с кодом 400 и сообщением "Invalid input data".
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        generate_response = await ac.post(
            "/generate", json=secret_data["correct"], headers={"Authorization": f"Bearer {authenticated_user}"}
        )
        secret_key = generate_response.json()["secret_key"]

        response = await ac.post(
            f"/secrets/{secret_key}",
            json={"passphrase": secret_data["incorrect_passphrase"]["passphrase"]},
            headers={"Authorization": f"Bearer {authenticated_user}"},
        )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid input data"}


@pytest.mark.anyio
async def test_get_secret_with_incorrect_secret_key(
    setup_service: None, secret_data: Dict[str, Dict[str, str]], authenticated_user: str
) -> None:
    """
    Тестирует получение секрета с неправильным ключом.
    Ожидается ошибка с кодом 404 и сообщением "Secret not found".
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/generate", json=secret_data["correct"], headers={"Authorization": f"Bearer {authenticated_user}"}
        )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"/secrets/{secret_data['incorrect_secret_key']['secret_key']}",
            json={"passphrase": secret_data["correct"]["passphrase"]},
            headers={"Authorization": f"Bearer {authenticated_user}"},
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Secret not found"}


@pytest.mark.anyio
async def test_get_secret_with_incorrect_both(
    setup_service: None, secret_data: Dict[str, Dict[str, str]], authenticated_user: str
) -> None:
    """
    Тестирует получение секрета с неправильным ключом и паролем.
    Ожидается ошибка с кодом 404 и сообщением "Secret not found".
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/generate", json=secret_data["correct"], headers={"Authorization": f"Bearer {authenticated_user}"}
        )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"/secrets/{secret_data['incorrect_both']['secret_key']}",
            json={"passphrase": secret_data["incorrect_both"]["passphrase"]},
            headers={"Authorization": f"Bearer {authenticated_user}"},
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Secret not found"}


@pytest.mark.anyio
async def test_generate_get_and_verify_secret_deletion(
    setup_service: None, secret_data: Dict[str, Dict[str, str]], authenticated_user: str
) -> None:
    """
    Тестирует создание секрета, его получение и удаление.
    Ожидается, что после удаления секрета, повторный запрос вернет ошибку 404.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        generate_response = await ac.post(
            "/generate", json=secret_data["correct"], headers={"Authorization": f"Bearer {authenticated_user}"}
        )
        secret_key = generate_response.json()["secret_key"]
        response = await ac.post(
            f"/secrets/{secret_key}",
            json={"passphrase": secret_data["correct"]["passphrase"]},
            headers={"Authorization": f"Bearer {authenticated_user}"},
        )
    assert response.status_code == 200
    assert response.json() == {"secret": secret_data["correct"]["secret"]}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"/secrets/{secret_key}",
            json={"passphrase": secret_data["correct"]["passphrase"]},
            headers={"Authorization": f"Bearer {authenticated_user}"},
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Secret not found"}


@pytest.mark.anyio
async def test_ttl_index_creation() -> None:
    """
    Тестирует создание TTL индекса для коллекции в MongoDB.
    Ожидается, что индекс с полем expiration_1 будет создан с правильным временем жизни.
    """
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[TEST_DATABASE_NAME]
    collection = db["secrets"]

    indexes = await collection.index_information()

    assert "expiration_1" in indexes

    ttl_seconds = indexes["expiration_1"].get("expireAfterSeconds")
    assert ttl_seconds == int(TTL_INDEX_SECONDS)
    client.close()
