import os

from dotenv import load_dotenv

load_dotenv()

SALT = os.getenv("SALT")
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_NAME = os.getenv("MONGODB_NAME")
TTL_EXPIRE_SECONDS = int(os.getenv("TTL_EXPIRE_SECONDS"))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
