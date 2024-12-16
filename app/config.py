import os

from dotenv import load_dotenv

load_dotenv()

SALT = os.getenv("SALT")
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_NAME = os.getenv("MONGODB_NAME")
TTL_EXPIRE_SECONDS = os.getenv('TTL_EXPIRE_SECONDS')
