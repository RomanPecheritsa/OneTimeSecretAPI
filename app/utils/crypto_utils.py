from base64 import urlsafe_b64decode, urlsafe_b64encode

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key_from_passphrase(passphrase: bytes, salt: bytes) -> bytes:
    """
    Генерирует криптографический ключ на основе переданной фразы-пароля и соли.

    Этот метод использует алгоритм PBKDF2-HMAC с SHA-256 для извлечения ключа из фразы-пароля
    с использованием соли. Количество итераций установлено на 100000, что повышает безопасность
    в случае атак на основе словарей.

    :param passphrase: кодовая фраза, используемая для генерации ключа.
    :param salt: соль, добавляемая для улучшения безопасности генерации ключа.
    :return: закодированный в base64 криптографический ключ (bytes).
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(passphrase)
    return urlsafe_b64encode(key)


def encrypt(secret: str, key: bytes) -> str:
    """
    Шифрует строку с помощью криптографического ключа.

    Этот метод использует алгоритм шифрования Fernet (симметричное шифрование) для зашифровки
    переданного секрета. Полученный зашифрованный секрет кодируется в base64 для удобства передачи и хранения.

    :param secret: строка, которую необходимо зашифровать.
    :param key: криптографический ключ для шифрования.
    :return: зашифрованный секрет в формате base64 (str).
    """
    f = Fernet(key)
    encrypted_secret = f.encrypt(secret.encode())
    return urlsafe_b64encode(encrypted_secret).decode()


def decrypt(encrypted_secret: str, key: bytes) -> str:
    """
    Дешифрует зашифрованный секрет с использованием криптографического ключа.

    Этот метод использует алгоритм Fernet для дешифровки зашифрованного секрета, который был
    предварительно зашифрован с использованием соответствующего ключа. Возвращает исходную строку.

    :param encrypted_secret: зашифрованная строка в формате base64.
    :param key: криптографический ключ для дешифровки.
    :return: расшифрованный секрет в виде строки (str).
    """
    f = Fernet(key)  # Инициализация объекта Fernet с переданным ключом
    encrypted_secret_bytes = urlsafe_b64decode(encrypted_secret)  # Декодирование зашифрованной строки из base64
    return f.decrypt(encrypted_secret_bytes).decode()  # Дешифровка и преобразование в строку
