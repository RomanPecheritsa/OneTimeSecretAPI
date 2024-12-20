
from dotenv import load_dotenv
import pytest


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    print("Loading environment from .env.test")
    load_dotenv(dotenv_path=".env.test")
