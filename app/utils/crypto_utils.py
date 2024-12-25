from base64 import urlsafe_b64decode, urlsafe_b64encode

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key_from_passphrase(passphrase: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = kdf.derive(passphrase)
    return urlsafe_b64encode(key)


def encrypt(secret: str, key: bytes) -> str:
    f = Fernet(key)
    encrypted_secret = f.encrypt(secret.encode())
    return urlsafe_b64encode(encrypted_secret).decode()


def decrypt(encrypted_secret: str, key: bytes) -> str:
    f = Fernet(key)
    encrypted_secret_bytes = urlsafe_b64decode(encrypted_secret)
    return f.decrypt(encrypted_secret_bytes).decode()
