from typing import Dict

import pytest
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGODB_URI, TEST_DATABASE_NAME, TTL_INDEX_SECONDS, SALT
from app.core.dependencies import create_secret_service_and_repository
from app.main import app


@pytest.fixture(scope="module")
async def setup_service():
    test_secret_repository, test_secret_service = create_secret_service_and_repository(
        mongodb_uri=MONGODB_URI,
        db_name=TEST_DATABASE_NAME,
        salt=SALT
    )
    await test_secret_repository.initialize_indexes()
    app.state.secret_service = test_secret_service

    yield

    await test_secret_repository.clear_all()
    await test_secret_repository.close()
    del app.state.secret_service


@pytest.fixture
def secret_data() -> Dict[str, Dict[str, str]]:
    return {
        "correct": {"secret": "test_secret", "passphrase": "test_passphrase", "secret_key": "secret_key"},
        "incorrect_passphrase": {"secret": "test_secret", "passphrase": "wrong_passphrase", "secret_key": "secret_key"},
        "incorrect_secret_key": {"secret": "test_secret", "passphrase": "test_passphrase", "secret_key": "invalid_key"},
        "incorrect_both": {"secret": "test_secret", "passphrase": "wrong_passphrase", "secret_key": "invalid_key"},
    }


@pytest.mark.anyio
async def test_generate_secret(setup_service: None, secret_data: Dict[str, Dict[str, str]]) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/generate", json=secret_data["correct"])
    assert response.status_code == 200
    assert "secret_key" in response.json()


@pytest.mark.anyio
async def test_get_secret(setup_service: None, secret_data: Dict[str, Dict[str, str]]) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        generate_response = await ac.post("/generate", json=secret_data["correct"])
        secret_key = generate_response.json()["secret_key"]

        response = await ac.post(f"/secrets/{secret_key}", json={"passphrase": secret_data["correct"]["passphrase"]})
    assert response.status_code == 200
    assert response.json() == {"secret": secret_data["correct"]["secret"]}


@pytest.mark.anyio
async def test_get_secret_with_incorrect_passphrase(
    setup_service: None, secret_data: Dict[str, Dict[str, str]]
) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        generate_response = await ac.post("/generate", json=secret_data["correct"])
        secret_key = generate_response.json()["secret_key"]

        response = await ac.post(
            f"/secrets/{secret_key}", json={"passphrase": secret_data["incorrect_passphrase"]["passphrase"]}
        )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid input data"}


@pytest.mark.anyio
async def test_get_secret_with_incorrect_secret_key(
    setup_service: None, secret_data: Dict[str, Dict[str, str]]
) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/generate", json=secret_data["correct"])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"/secrets/{secret_data['incorrect_secret_key']['secret_key']}",
            json={"passphrase": secret_data["correct"]["passphrase"]},
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Secret not found"}


@pytest.mark.anyio
async def test_get_secret_with_incorrect_both(setup_service: None, secret_data: Dict[str, Dict[str, str]]) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/generate", json=secret_data["correct"])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"/secrets/{secret_data['incorrect_both']['secret_key']}",
            json={"passphrase": secret_data["incorrect_both"]["passphrase"]},
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Secret not found"}


@pytest.mark.anyio
async def test_generate_get_and_verify_secret_deletion(
    setup_service: None, secret_data: Dict[str, Dict[str, str]]
) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        generate_response = await ac.post("/generate", json=secret_data["correct"])
        secret_key = generate_response.json()["secret_key"]

        response = await ac.post(f"/secrets/{secret_key}", json={"passphrase": secret_data["correct"]["passphrase"]})
    assert response.status_code == 200
    assert response.json() == {"secret": secret_data["correct"]["secret"]}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(f"/secrets/{secret_key}", json={"passphrase": secret_data["correct"]["passphrase"]})
    assert response.status_code == 404
    assert response.json() == {"detail": "Secret not found"}


@pytest.mark.anyio
async def test_ttl_index_creation():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[TEST_DATABASE_NAME]
    collection = db['secrets']

    indexes = await collection.index_information()

    assert 'expiration_1' in indexes

    ttl_seconds = indexes['expiration_1'].get('expireAfterSeconds')
    assert ttl_seconds == int(TTL_INDEX_SECONDS)
    client.close()

