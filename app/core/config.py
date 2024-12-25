import os

from dotenv import load_dotenv

load_dotenv()
SALT = os.getenv("SALT")
MONGODB_URI = os.getenv("MONGODB_URI")
TTL_INDEX_SECONDS = os.getenv("TTL_INDEX_SECONDS")
DATABASE_NAME = os.getenv("DATABASE_NAME")
TEST_DATABASE_NAME = os.getenv("TEST_DATABASE_NAME")
